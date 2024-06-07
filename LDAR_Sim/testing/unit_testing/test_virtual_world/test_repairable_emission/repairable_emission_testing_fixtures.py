"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        fugitive_emissions_testing_fixtures.py
Purpose: Contains fixtures for fugitive emission testing unit tests

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

from datetime import date
from typing import Tuple
import pytest

from virtual_world.emission_types.repairable_emission import RepairableEmission
from src.constants.general_const import Emission_Constants as ec


@pytest.fixture(name="mock_simple_fugitive_emission_for_activate_testing_1")
def mock_simple_fugitive_emission_for_activate_testing_1_fix() -> RepairableEmission:
    return RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), False, {}, 14, 200, 365
    )


@pytest.fixture(name="mock_simple_fugitive_emission_for_check_if_repaired_testing_1")
def mock_simple_fugitive_emission_for_check_if_repaired_testing_1_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), False, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret


@pytest.fixture(name="mock_simple_fugitive_emission_for_check_if_repaired_testing_2")
def mock_simple_fugitive_emission_for_check_if_repaired_testing_2_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret, date(*[2018, 3, 2])


@pytest.fixture(name="mock_simple_emission_for_get_summary_dict")
def mock_simple_emission_for_get_summary_dict_1_fix() -> Tuple[RepairableEmission, dict[str, int]]:
    return (
        date(*[2020, 1, 1]),
        RepairableEmission(
            1,
            1,
            date(*[2018, 1, 1]),
            date(*[2017, 1, 1]),
            True,
            {"M_OGI1": 1, "M_AIR1": 1, "M_OGI2": 0, "M_AIR2": 0},
            14,
            200,
            365,
        ),
        {
            "Emissions ID": "0000000001",
            "Status": ec.INACTIVE,
            "Days Active": 0,
            "Estimated Days Active": 0,
            '"True" Volume Emitted (Kg Methane)': 0.0,
            "Mitigated Emissions (Kg Methane)": 0.0,
            '"True" Rate (g/s)': 1,
            '"Measured" Rate (g/s)': None,
            "Date Began": date(2018, 1, 1),
            "Initially Detected By": None,
            "Initially Detected Date": None,
            "Tagged": False,
            "Tagged By": None,
            "Recorded": "N/A",
            "Recorded By": "N/A",
            "Repairable": True,
            "Date Repaired or Expired": None,
            "Theoretical End Date": date(2019, 1, 1),
        },
    )


@pytest.fixture(name="mock_simple_fugitive_emission_for_natural_repair_testing_1")
def mock_simple_fugitive_emission_for_natural_repair_testing_1_fix() -> (
    Tuple[RepairableEmission, date]
):
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret, date(*[2018, 3, 2])


@pytest.fixture(name="mock_simple_fugitive_emission_for_natural_repair_testing_2")
def mock_simple_fugitive_emission_for_natural_repair_testing_2_fix() -> (
    Tuple[RepairableEmission, date]
):
    to_ret = RepairableEmission(
        1, 1, date(*[2016, 12, 31]), date(*[2017, 1, 1]), True, {}, 14, 200, 10
    )
    to_ret._days_since_tagged = 0
    to_ret._active_days = 9
    return to_ret, date(*[2017, 1, 10])


@pytest.fixture(name="mock_simple_fugitive_emission_for_tag_leak_testing_1")
def mock_simple_fugitive_emission_for_tag_leak_testing_1_fix() -> Tuple[
    RepairableEmission,
    Tuple[float, date, int, str, str, int],
]:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 60
    return to_ret, (1, date(*[2017, 6, 1]), 1, "test", "test", 1)


@pytest.fixture(name="mock_simple_fugitive_emission_for_tag_leak_testing_already_tagged")
def mock_simple_fugitive_emission_for_tag_leak_testing_already_tagged_fix() -> Tuple[
    RepairableEmission,
    Tuple[float, date, int, str, str, int],
]:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 60
    to_ret._tagged = True
    return to_ret, (1.0, date(*[2017, 6, 1]), 1, "test", "test", 1)


@pytest.fixture(name="mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged")
def mock_simple_fugitive_emission_for_tagged_today_testing_just_tagged_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 0
    to_ret._tagged = True
    to_ret._tagged_by_company = "Test"
    return to_ret


@pytest.fixture(name="mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged")
def mock_simple_fugitive_emission_for_tagged_today_testing_not_tagged_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._tagged = False
    return to_ret


@pytest.fixture(name="mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously")
def mock_simple_fugitive_emission_for_tagged_today_testing_tagged_previously_fix() -> (
    RepairableEmission
):
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 60
    to_ret._tagged = True
    to_ret._tagged_by_company = "Test"
    return to_ret


@pytest.fixture(name="mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural")
def mock_simple_fugitive_emission_for_tagged_today_testing_tagged_by_natural_fix() -> (
    RepairableEmission
):
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 0
    to_ret._tagged = True
    to_ret._tagged_by_company = ec.NATURAL
    return to_ret


@pytest.fixture(name="mock_fugitive_emission_for_update_detection_records_no_prior_detection")
def mock_fugitive_emission_for_update_detection_records_no_prior_detection_fix() -> (
    RepairableEmission
):
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    return to_ret


@pytest.fixture(name="mock_fugitive_emission_for_update_detection_records_w_prior_detection")
def mock_fugitive_emission_for_update_detection_records_w_prior_detection_fix() -> (
    RepairableEmission
):
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._init_detect_by = "test"
    to_ret._init_detect_date = date(*[2018, 1, 2])
    return to_ret


@pytest.fixture(name="mock_fugitive_emission_for_update_ready_for_nat_repair")
def mock_fugitive_emission_for_update_ready_for_nat_repair_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 364
    to_ret._status = ec.ACTIVE
    return to_ret


@pytest.fixture(name="mock_fugitive_emission_for_update_no_status_change")
def mock_fugitive_emission_for_update_no_status_change_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 60
    to_ret._status = ec.ACTIVE
    return to_ret


@pytest.fixture(name="mock_fugitive_emission_for_update_no_status_change_emission_tagged")
def mock_fugitive_emission_for_update_no_status_change_emission_tagged_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 60
    to_ret._status = ec.ACTIVE
    to_ret._tagged = True
    to_ret._days_since_tagged = 1
    return to_ret


@pytest.fixture(name="mock_fugitive_emission_for_update_newly_repaired")
def mock_fugitive_emission_for_update_newly_repaired_fix() -> RepairableEmission:
    to_ret = RepairableEmission(
        1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 60
    to_ret._status = ec.ACTIVE
    to_ret._tagged = True
    to_ret._days_since_tagged = 13
    return to_ret
