from hrm.services import change_phone_number_status
from hrm.tests.fixtures import phone_number_fixture


def test_change_phone_number_status(db, phone_number_fixture):
    expected_status = False
    change_phone_number_status(
        phone_number=phone_number_fixture,
        status=expected_status
    )
    assert phone_number_fixture.is_enable == expected_status, "Status not changed."
