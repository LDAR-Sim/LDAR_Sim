import pytest
from unittest.mock import patch
from src.programs.site_level_method import SiteLevelMethod
from src.scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule

from src.programs.method import Method

from src.sensors.sensor_constant_mapping import SENS_TYPE, SENS_MDL, SENS_QE


@pytest.fixture
def mock_follow_up_schedule(mocker):
    mock_schedule = mocker.Mock(spec=FollowUpMobileSchedule)
    # You can configure the mock as needed for your test
    return mock_schedule


def test_site_level_method_creation(mock_follow_up_schedule):
    # Define properties dictionary for the method
    properties = {
        "follow_up": {
            "interaction_priority": "threshold",
            "delay": 10,
            "proportion": 0.5,
            "threshold": 0.8,
            "instant_threshold": 1.0,
            "redundancy_filter": "some_filter",
        },
        Method.DETEC_ACCESSOR: {SENS_TYPE: "default", SENS_MDL: 1.0, SENS_QE: 0.0},
        "max_workday": 8,
        "consider_daylight": False,
        "weather_envs": {"precip": [], "wind": [], "temp": []},
        "is_follow_up": False,
        "t_bw_sites": {"vals": []},
        "n_crews": 5,
        "reporting_delay": 7,
        "cost": {"per_site": 10, "upfront": 5},
        # Include other properties as needed
    }

    # Patching _estimate_method_crews_required to return 1
    with patch.object(SiteLevelMethod, "_estimate_method_crews_required", return_value=1):
        # Create an instance of SiteLevelMethod
        method_name = "TestMethod"
        consider_weather = True
        sites = []  # Pass the appropriate list of Site objects
        follow_up_schedule = mock_follow_up_schedule
        site_method = SiteLevelMethod(
            method_name, properties, consider_weather, sites, follow_up_schedule
        )

        # Assert that the method is created successfully
        assert isinstance(site_method, SiteLevelMethod)
        assert site_method._name == method_name
        assert site_method._max_work_hours == properties["max_workday"]
        assert site_method._weather == consider_weather
        assert site_method._is_follow_up == False
