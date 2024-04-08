from datetime import date
from typing import Tuple
import pytest

from src.virtual_world.emissions import Emission


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
            "Status": "inactive",
            "Days Active": 0,
            "Estimated Days Active": 0,
            '"True" Volume Emitted (Kg Methane)': 0.0,
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
