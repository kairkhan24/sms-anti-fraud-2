from hrm.models import AdminSettings
from hrm.selectors import get_admin_setting
from hrm.tests.fixtures import admin_setting_fixture


def test_get_admin_fixture(db, admin_setting_fixture):
    admin_setting_name = admin_setting_fixture.name
    admin_setting = get_admin_setting(name=admin_setting_name)
    assert isinstance(admin_setting, AdminSettings), "Not instance for AdminSettings model"
    assert admin_setting_fixture.id == admin_setting.id, "AdminSetting not found"
