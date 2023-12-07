"""Fixtures for testing utils.attribution methods"""

import pytest
from datetime import date

from src.time_counter import TimeCounter


@pytest.fixture(name="mock_leak_for_update_tag_testing_1")
def mock_leak_for_update_tag_testing_1_fix():
    return {"tagged": True, "date_tagged": date(2017, 1, 1)}


@pytest.fixture(name="mock_leak_for_update_tag_testing_2")
def mock_leak_for_update_tag_testing_2_fix():
    return {"tagged": False}


@pytest.fixture(name="mock_company_for_update_tag_testing_1")
def mock_company_for_update_tag_testing_1_fix():
    return "natural"


@pytest.fixture(name="mock_TimeCounter_for_update_tag_testing_1")
def mock_TimeCounter_for_update_tag_testing_1_fix(mocker):
    mock_tc = mocker.Mock(TimeCounter)
    mock_tc.current_date = date(2017, 1, 1)
    mock_tc.current_timestep = 1
    return mock_tc


@pytest.fixture(name="mock_timeseries_for_update_tag_testing_1")
def mock_timeseries_for_update_tag_testing_1_fix():
    return {"natural_n_tags": [0, 0]}


@pytest.fixture(name="mock_site_for_update_tag_testing_1")
def mock_site_for_update_tag_testing_1_fix():
    return {"currently_flagged": False, "flagged_by": None}
