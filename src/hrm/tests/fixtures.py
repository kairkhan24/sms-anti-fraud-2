import pytest

from hrm.models import AdminSettings, PhoneNumber


@pytest.fixture
def admin_setting_fixture():
    return AdminSettings.objects.create(
        name='Standard',
        period_in_seconds=60,
        count_per_user=5,
    )


@pytest.fixture
def phone_number_fixture(admin_setting_fixture):
    return PhoneNumber.objects.create(
        phone_number='+77771234569',
        is_enable=True,
        setting=admin_setting_fixture
    )
