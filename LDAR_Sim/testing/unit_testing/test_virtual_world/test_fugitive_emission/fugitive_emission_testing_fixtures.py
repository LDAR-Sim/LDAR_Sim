from datetime import datetime
from typing import Tuple

# from typing import Tuple
import pytest

from virtual_world.fugitive_emission import FugitiveEmission


@pytest.fixture(name="mock_simple_fugitive_emission_for_activate_testing_1")
def mock_simple_fugitive_emission_for_activate_testing_1_fix() -> FugitiveEmission:
    return FugitiveEmission(
        1, 1, datetime(*[2018, 1, 1]), datetime(*[2017, 1, 1]), False, {}, 14, 200, 365
    )


@pytest.fixture(name="mock_simple_fugitive_emission_for_check_if_repaired_testing_1")
def mock_simple_fugitive_emission_for_check_if_repaired_testing_1_fix() -> FugitiveEmission:
    to_ret = FugitiveEmission(
        1, 1, datetime(*[2018, 1, 1]), datetime(*[2017, 1, 1]), False, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret


@pytest.fixture(name="mock_simple_fugitive_emission_for_check_if_repaired_testing_2")
def mock_simple_fugitive_emission_for_check_if_repaired_testing_2_fix() -> FugitiveEmission:
    to_ret = FugitiveEmission(
        1, 1, datetime(*[2018, 1, 1]), datetime(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret, datetime(*[2018, 3, 2])


@pytest.fixture(name="mock_simple_emission_for_get_summary_dict")
def mock_simple_emission_for_get_summary_dict_1_fix() -> Tuple[FugitiveEmission, dict[str, int]]:
    return (
        FugitiveEmission(
            1,
            1,
            datetime(*[2018, 1, 1]),
            datetime(*[2017, 1, 1]),
            False,
            {"M_OGI1": 1, "M_AIR1": 1, "M_OGI2": 0, "M_AIR2": 0},
            14,
            200,
            365,
        ),
        {
            "Date Began": datetime(2018, 1, 1, 0, 0),
            "Days Active": 0,
            "Emissions ID": "0000000001",
            "Initially Detected By": None,
            "Status": "Inactive",
            "Tagged": False,
            "Tagged By": None,
            "Volume Emitted": 0.0,
            "Date Repaired": None,
        },
    )


@pytest.fixture(name="mock_simple_fugitive_emission_for_natural_repair_testing_1")
def mock_simple_fugitive_emission_for_natural_repair_testing_1_fix() -> (
    Tuple[FugitiveEmission, datetime]
):
    to_ret = FugitiveEmission(
        1, 1, datetime(*[2018, 1, 1]), datetime(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._days_since_tagged = 30
    to_ret._active_days = 60
    return to_ret, datetime(*[2018, 3, 2])


@pytest.fixture(name="mock_simple_fugitive_emission_for_tag_leak_testing_1")
def mock_simple_fugitive_emission_for_tag_leak_testing_1_fix() -> Tuple[FugitiveEmission, datetime]:
    to_ret = FugitiveEmission(
        1, 1, datetime(*[2018, 1, 1]), datetime(*[2017, 1, 1]), True, {}, 14, 200, 365
    )
    to_ret._active_days = 60
    return to_ret, datetime(*[2018, 3, 2])
