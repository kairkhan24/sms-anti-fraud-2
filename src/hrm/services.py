import requests
import redis

from django.conf import settings
from django.apps import apps
from sentry_sdk import capture_message

from hrm.models import PhoneNumber
from hrm.selectors import get_phone_number, get_admin_setting

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def create_phone_number(*,
                        recipient_phone: str,
                        admin_setting_name: str = "Standard",
                        is_enable: bool = True
                        ) -> PhoneNumber:
    admin_setting = get_admin_setting(
        name=admin_setting_name,
        raise_exception=False,
    )
    if admin_setting is None:
        admin_setting = get_admin_setting(name='Standard')
    phone_number = PhoneNumber()
    phone_number.phone_number = recipient_phone
    phone_number.setting = admin_setting
    phone_number.is_enable = is_enable
    phone_number.clean()
    phone_number.save()
    return phone_number


def change_phone_number_status(*,
                               phone_number: PhoneNumber,
                               status: bool,
                               ):
    if phone_number.is_enable != status:
        phone_number.is_enable = status
        phone_number.save(update_fields=('is_enable',))


class SmsNotSentException(Exception):
    pass


class MobizonSmsService:
    def send_message(self, recipient_phone, text):
        if not settings.SEND_SMS:
            return

        not_send_sms_phone_numbers = apps.get_model('hrm.AdminSettings').objects.get_not_send_sms_phone_numbers()

        if recipient_phone in not_send_sms_phone_numbers:
            return

        # url = f'{settings.MOBIZON_URL}?recipient={recipient_phone}&text={text}&apiKey={settings.MOBIZON_KEY}&from=easytap'
        url = f'{settings.MOBIZON_URL}?recipient={recipient_phone}&text={text}&apiKey={settings.MOBIZON_KEY}'
        got = requests.get(url)

        message_id = got.json().get('data', {}).get('messageId')
        if not message_id:
            capture_message(f'#sms-fail: {recipient_phone} {text} | {got.json()}')
            raise SmsNotSentException()

        return got.json()
        # return {"simple_dict": True}


mobizon_sms_service = MobizonSmsService()


def send_sms_message(*,
                     recipient_phone: str,
                     text: str):
    phone_number = get_phone_number(
        recipient_phone=recipient_phone,
        raise_exception=False
    )
    if phone_number is None:
        phone_number = create_phone_number(recipient_phone=recipient_phone)

    if not r.get(recipient_phone):
        change_phone_number_status(phone_number=phone_number, status=True)
        mobizon_sms_service.send_message(
            recipient_phone=recipient_phone,
            text=text,
        )
        r.set(recipient_phone, 1, ex=phone_number.setting.period_in_seconds)
    else:
        current_count = int(r.get(recipient_phone))
        expired_period_in_seconds = r.ttl(recipient_phone)
        if current_count >= phone_number.setting.count_per_user:
            change_phone_number_status(phone_number=phone_number, status=False)
        else:
            change_phone_number_status(phone_number=phone_number, status=True)
            mobizon_sms_service.send_message(
                recipient_phone=recipient_phone,
                text=text,
            )
            r.set(recipient_phone, current_count + 1, ex=expired_period_in_seconds)
