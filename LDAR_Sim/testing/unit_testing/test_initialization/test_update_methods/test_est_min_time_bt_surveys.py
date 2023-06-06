"""Test file to unit test update_methods.py est_min_time_bt_surveys functionality"""
from src.initialization.update_methods import est_min_time_bt_surveys
import pytest
from typing import Any, Dict


@pytest.fixture
def site_and_M_RS_for_testing() -> Dict[str, Any]:
    return {
        "M_RS": "OGI_RS",
        "site":
        {
            "OGI_RS": 4
        }
    }


def test_041_est_min_time_bt_surveys_basic_case(site_and_M_RS_for_testing):
    """Testing est_min_time_bt_survey correctly return a number of days equal to
    half the survey period for a simple test case, rounded down

    Args:
        site_and_M_RS_for_testing (dict[str, Any]):
        Pytest fixture providing paired M_RS and fake site
    """
    assert est_min_time_bt_surveys(
        site_and_M_RS_for_testing["M_RS"], 12, site_and_M_RS_for_testing["site"]) == 45


def test_041_est_min_time_bt_surveys_half_months(site_and_M_RS_for_testing):
    """Testing est_min_time_bt_survey correctly return a number of days equal to
    half the survey period for less than the full months, rounded down

    Args:
        site_and_M_RS_for_testing (dict[str, Any]):
        Pytest fixture providing paired M_RS and fake site
    """
    assert est_min_time_bt_surveys(
        site_and_M_RS_for_testing["M_RS"], 6, site_and_M_RS_for_testing["site"]) == 22
