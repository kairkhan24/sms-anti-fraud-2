import pytest
from django.db import IntegrityError

from hrm.models import PhoneNumber
from hrm.services import create_phone_number
from hrm.tests.fixtures import admin_setting_fixture, phone_number_fixture


def test_create_phone_number(db, admin_setting_fixture):
    assert PhoneNumber.objects.count() == 0, "There is object for this model"
    data = {
        "recipient_phone": "+77023693636",
        "is_enable": True,
        "admin_setting_name": admin_setting_fixture.name
    }
    phone_number = create_phone_number(
        recipient_phone=data['recipient_phone'],
        is_enable=data['is_enable'],
        admin_setting_name=data['admin_setting_name'],
    )
    assert PhoneNumber.objects.count() == 1, "Phone number not created."
    assert phone_number.phone_number == data['recipient_phone'], "Incorrect phone number"
    assert phone_number.is_enable == data['is_enable'], "Incorrect status"


def test_create_phone_number_with_unique_value(db, admin_setting_fixture, phone_number_fixture):
    existing_phone_number = phone_number_fixture.phone_number

    data = {
        "recipient_phone": existing_phone_number,
        "is_enable": True,
        "admin_setting_name": admin_setting_fixture.name
    }
    with pytest.raises(IntegrityError):
        phone_number = create_phone_number(
            recipient_phone=data['recipient_phone'],
            is_enable=data['is_enable'],
            admin_setting_name=data['admin_setting_name'],
        )
