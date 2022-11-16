from django.shortcuts import get_object_or_404
from hrm.models import PhoneNumber

from hrm.models import AdminSettings


def get_admin_setting(*,
                      name: str,
                      raise_exception: bool = True,
                      ) -> AdminSettings:
    if raise_exception:
        admin_setting = get_object_or_404(AdminSettings, name=name)
    else:
        admin_setting = AdminSettings.objects.filter(name=name).first()
    return admin_setting


def get_phone_number(*,
                     recipient_phone: str,
                     raise_exception: bool = True,
                     ) -> PhoneNumber:
    if raise_exception:
        phone_number = get_object_or_404(PhoneNumber, phone_number=recipient_phone)
    else:
        phone_number = PhoneNumber.objects.filter(phone_number=recipient_phone).first()
    return phone_number
