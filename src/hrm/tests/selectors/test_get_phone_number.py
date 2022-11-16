from hrm.models import PhoneNumber
from hrm.selectors import get_phone_number
from hrm.tests.fixtures import phone_number_fixture


def test_phone_number(db, phone_number_fixture):
    phone_number_recipient_phone = phone_number_fixture.phone_number
    phone_number = get_phone_number(recipient_phone=phone_number_recipient_phone)
    assert isinstance(phone_number, PhoneNumber), "Not instance for PhoneNumber model"
    assert phone_number_fixture.id == phone_number.id, "PhoneNumber not found"
