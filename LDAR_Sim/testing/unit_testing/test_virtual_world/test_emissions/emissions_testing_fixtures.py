"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        emissions_testing_fixtures.py
Purpose: Contains fixtures for testing emissions unit tests

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

from src.virtual_world.emissions import Emission
from src.constants.general_const import Emission_Constants as ec


@pytest.fixture(name="mock_simple_emission_1")
def mock_simple_emission_1_fix() -> Emission:
    return Emission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), False, {})


@pytest.fixture(name="mock_simple_emission_spat_cov_testing_1")
def mock_simple_emission_spat_cov_testing_1_fix() -> Tuple[Emission, dict[str, int]]:
    return (
        Emission(
            1,
            1,
            date(*[2018, 1, 1]),
            date(*[2017, 1, 1]),
            False,
            {"M_OGI1": 1, "M_AIR1": 1, "M_OGI2": 0, "M_AIR2": 0},
        ),
        {"M_OGI1": 1, "M_AIR1": 1, "M_OGI2": 0, "M_AIR2": 0},
    )


@pytest.fixture(name="mock_random_emission_spat_cov_testing_1")
def mock_random_emission_spat_cov_testing_1_fix() -> Tuple[Emission, dict[str, int]]:
    return (
        Emission(
            1,
            1,
            date(*[2018, 1, 1]),
            date(*[2017, 1, 1]),
            False,
            {"M_OGI1": 0.5, "M_AIR1": 0.5, "M_OGI2": 0.9, "M_AIR2": 0.9},
        ),
        {"M_OGI1": 0, "M_AIR1": 1, "M_OGI2": 1, "M_AIR2": 1},
    )


@pytest.fixture(name="mock_simple_emission_for_get_summary_dict")
def mock_simple_emission_for_get_summary_dict_fix() -> Tuple[Emission, dict[str, int]]:
    return (
        Emission(
            1,
            1,
            date(*[2018, 1, 1]),
            date(*[2017, 1, 1]),
            False,
            {"M_OGI1": 1, "M_AIR1": 1, "M_OGI2": 0, "M_AIR2": 0},
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
            "Tagged": "N/A",
            "Tagged By": "N/A",
            "Recorded": "N/A",
            "Recorded By": "N/A",
            "Repairable": False,
        },
    )
