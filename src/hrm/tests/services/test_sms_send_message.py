import pytest
from hrm.services import send_sms_message, SmsNotSentException


def test_sms_send_message(db, admin_setting_fixture):
    with pytest.raises(SmsNotSentException):
        send_sms_message(
            recipient_phone="+755633",
            text="asd"
        )
        assert 1 == 0

