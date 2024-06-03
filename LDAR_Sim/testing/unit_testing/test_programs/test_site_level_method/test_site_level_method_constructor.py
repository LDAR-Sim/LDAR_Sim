import pytest
from unittest.mock import patch
from src.programs.site_level_method import SiteLevelMethod
from src.scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule


from src.constants import param_default_const as pdc


@pytest.fixture
def mock_follow_up_schedule(mocker):
    mock_schedule = mocker.Mock(spec=FollowUpMobileSchedule)
    # You can configure the mock as needed for your test
    return mock_schedule


def test_site_level_method_creation(mock_follow_up_schedule):
    # Define properties dictionary for the method
    properties = {
        pdc.Method_Params.FOLLOW_UP: {
            pdc.Method_Params.INTERACTION_PRIORITY: "threshold",
            pdc.Method_Params.DELAY: 10,
            pdc.Method_Params.PROPORTION: 0.5,
            pdc.Method_Params.THRESHOLD: 0.8,
            pdc.Method_Params.INSTANT_THRESHOLD: 1.0,
            pdc.Method_Params.REDUNDANCY_FILTER: "some_filter",
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1.0,
            pdc.Method_Params.QE: 0.0,
        },
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.PRECIP: [],
            pdc.Method_Params.WIND: [],
            pdc.Method_Params.TEMP: [],
        },
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: []},
        pdc.Method_Params.N_CREWS: 5,
        pdc.Method_Params.REPORTING_DELAY: 7,
        pdc.Method_Params.COST: {pdc.Method_Params.PER_SITE: 10, pdc.Method_Params.UPFRONT: 5},
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
        assert site_method._is_follow_up is False
