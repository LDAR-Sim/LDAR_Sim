from datetime import date
from typing import Tuple
import pytest

from src.virtual_world.nonfugitive_emissions import NonRepairableEmission


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_activate_testing_1")
def mock_simple_nonfugitive_emission_for_activate_testing_1_fix() -> NonRepairableEmission:
    return NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), False, {}, 365)


@pytest.fixture(name="mock_simple_emission_for_get_summary_dict")
def mock_simple_emission_for_get_summary_dict_1_fix() -> (
    Tuple[NonRepairableEmission, dict[str, int]]
):
    return (
        date(*[2020, 1, 1]),
        NonRepairableEmission(
            1,
            1,
            date(*[2018, 1, 1]),
            date(*[2017, 1, 1]),
            False,
            {"M_OGI1": 1, "M_AIR1": 1, "M_OGI2": 0, "M_AIR2": 0},
            365,
        ),
        {
            "Emissions ID": "0000000001",
            "Status": "Inactive",
            "Days Active": 0,
            '"True" Volume Emitted (Kg Methane)': 0.0,
            '"Estimated" Volume Emitted (Kg Methane)': 0.0,
            '"True" Rate (g/s)': 1,
            '"Measured" Rate (g/s)': None,
            "Date Began": date(2018, 1, 1),
            "Initially Detected By": None,
            "Initially Detected Date": None,
            "Tagged": "N/A",
            "Tagged By": "N/A",
            "Recorded": False,
            "Recorded By": None,
            "Repairable": False,
            "Estimated Days Active": 0,
        },
    )


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_expire_testing_1")
def mock_simple_nonfugitive_emission_for_expire_testing_1_fix() -> (
    Tuple[NonRepairableEmission, date]
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret, date(*[2018, 3, 2])


@pytest.fixture(name="mock_nonfugitive_emission_for_update_no_status_change")
def mock_nonfugitive_emission_for_update_no_status_change_fix() -> NonRepairableEmission:
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._active_days = 60
    to_ret._status = "Active"
    return to_ret


@pytest.fixture(name="mock_nonfugitive_emission_for_update_no_status_change_emission_recorded")
def mock_nonfugitive_emission_for_update_no_status_change_emission_recorded_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._active_days = 60
    to_ret._status = "Active"
    to_ret._record = True
    to_ret._recorded_by_company = "Test"
    return to_ret


@pytest.fixture(name="mock_nonfugitive_emission_for_update_will_expire")
def mock_nonfugitive_emission_for_update_will_expire_fix() -> NonRepairableEmission:
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._active_days = 59
    to_ret._status = "Active"
    to_ret._duration = 60
    return to_ret


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_tagged_today_testing_just_tagged")
def mock_simple_nonfugitive_emission_for_tagged_today_testing_just_tagged_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._days_since_tagged = 0
    to_ret._record = True
    to_ret._tagged_by_company = "Test"
    return to_ret


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_tagged_today_testing_not_tagged")
def mock_simple_nonfugitive_emission_for_tagged_today_testing_not_tagged_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._record = False
    return to_ret


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_tagged_today_testing_tagged_by_expire")
def mock_simple_nonfugitive_emission_for_tagged_today_testing_tagged_by_expire_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._days_since_tagged = 0
    to_ret._record = True
    to_ret._tagged_by_company = "expired"
    return to_ret


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_tagged_today_testing_tagged_previously")
def mock_simple_nonfugitive_emission_for_tagged_today_testing_tagged_previously_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._days_since_tagged = 60
    to_ret._record = True
    to_ret._tagged_by_company = "Test"
    return to_ret


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_record_testing_1")
def mock_simple_nonfugitive_emission_for_record_testing_1_fix() -> Tuple[
    NonRepairableEmission,
    Tuple[float, date, int, str, str, int],
]:
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._active_days = 60
    return to_ret, (1, date(*[2017, 6, 1]), 1, "test", "test")


@pytest.fixture(name="mock_simple_nonfugitive_emission_for_record_testing_already_recorded")
def mock_simple_nonfugitive_emission_for_record_testing_already_recorded_fix() -> Tuple[
    NonRepairableEmission,
    Tuple[float, date, int, str, str, int],
]:
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._active_days = 60
    to_ret._record = True
    to_ret._measured_rate = 1
    return to_ret, (1.0, date(*[2017, 6, 1]), 1, "test", "test")


@pytest.fixture(name="mock_nonfugitive_emission_for_update_detection_records_no_prior_detection")
def mock_nonfugitive_emission_for_update_detection_records_no_prior_detection_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    return to_ret


@pytest.fixture(name="mock_nonfugitive_emission_for_update_detection_records_w_prior_detection")
def mock_nonfugitive_emission_for_update_detection_records_w_prior_detection_fix() -> (
    NonRepairableEmission
):
    to_ret = NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 365)
    to_ret._init_detect_by = "test"
    to_ret._init_detect_date = date(*[2018, 1, 2])
    return to_ret
