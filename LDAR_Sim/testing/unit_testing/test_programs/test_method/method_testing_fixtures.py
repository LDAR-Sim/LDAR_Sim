"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        method_testing_fixtures
Purpose: Contains fixtures for testing Methods

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

import pytest
from datetime import date
from src.weather.daylight_calculator import DaylightCalculatorAve
from src.programs.method import Method
from src.virtual_world.infrastructure import Site
from collections import defaultdict
from scheduling.schedule_dataclasses import SiteSurveyReport
from sensors.default_site_level_sensor import DefaultSiteLevelSensor
from src.sensors.default_sensor import DefaultSensor
from src.virtual_world.emission_types.emission import Emission
from src.scheduling.workplan import Workplan
from src.scheduling.scheduled_survey_planner import ScheduledSurveyPlanner
from file_processing.output_processing.output_utils import CrewDeploymentStats
from constants import param_default_const as pdc


@pytest.fixture
def mocker_fixture(mocker):
    def mock_initialize_sensor(properties):
        return {}

    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    return mocker


def mock_average_t_btw_site(self):
    return 0


def mock_initialize_sensor(self, properties):
    return {}


def mock_get_method_survey_time(method_name, *args, **kwargs):
    return 120


def mock_get_survey_cost(self):
    return 0


def mock_check_weather(self, state, curr_date, site):
    return False


def mock_check_weather_t(self, state, curr_date, site):
    return True


def mock_get_average_method_surveys_required(self, site):
    return 1


def mock_get_travel_time(self):
    return 1


def mock_estimate_method_crews_required(self, crews, sites):
    return 2


def mock_estimate_method_crews_required2(self, crews, sites):
    return 4


def mock_detect_emissions(self, site, meth_name, survey_report):
    survey_report.site_true_rate = 1
    survey_report.survey_level = pdc.Levels.SITE_LEVEL
    survey_report.site_measured_rate = 1.0
    return True


def mock_determine_if_site_survey_can_be_completed(
    self, survey_report, site_survey_time, site_travel_time, crew_time_remaining
):
    return True


def mock_false_survey_site(self, crew, survey_report, site_to_survey, weather, curr_date):
    return SiteSurveyReport(1), 0, False, 0


def mock_survey_site(self, crew, survey_report, site_to_survey, weather, curr_date):
    return (
        SiteSurveyReport(
            site_id=1,
            time_surveyed=120,
            time_surveyed_current_day=120,
            time_spent_to_travel=1,
            survey_complete=True,
            survey_in_progress=False,
            equipment_groups_surveyed=[],
            survey_level="Site_level",
            site_measured_rate=1.0,
            site_true_rate=1.0,
            site_flagged=False,
            survey_completion_date=date(2023, 1, 1),
            survey_start_date=date(2023, 1, 1),
            method="test_method",
        ),
        1,
        True,
        1,
    )


def mock_get_detectable_emissions(method_name):
    return {
        "test_meth": {
            "test_meth": [
                Emission(
                    emission_n=1,
                    rate=1,
                    start_date=date(2023, 1, 1),
                    simulation_sd=date(2023, 1, 2),
                    repairable=True,
                    tech_spat_cov_probs={"test_meth": 1},
                )
            ],
        },
    }


def mock_daylight_calculator_ave_init(self):
    return


@pytest.fixture(name="simple_method_values")
def simple_method_values_fix(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        pdc.Method_Params.N_CREWS: 3,
        pdc.Method_Params.SENSOR: "default",
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
    )


@pytest.fixture(name="simple_method_values2")
def simple_method_values2_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1
    site_mock.get_id = mocker.Mock(side_effect=lambda: site_mock.id)
    mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        pdc.Method_Params.N_CREWS: 0,
        pdc.Method_Params.SENSOR: "default",
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 1,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
    )


@pytest.fixture(name="simple_method_values3")
def simple_method_values3_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1
    site_mock.get_id = mocker.Mock(side_effect=lambda: site_mock.id)
    mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        pdc.Method_Params.SENSOR: "default",
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 1,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: True,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
    )


@pytest.fixture(name="simple_method_values4")
def simple_method_values4_fix(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        pdc.Method_Params.N_CREWS: 5,
        pdc.Method_Params.SENSOR: "default",
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    survey_report = SiteSurveyReport(site_id=1)
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
        survey_report,
    )


@pytest.fixture(name="simple_method_values5")
def simple_method_values5_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1
    site_mock.get_id = mocker.Mock(side_effect=lambda: site_mock.id)
    mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    properties: dict = {
        pdc.Method_Params.N_CREWS: 5,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    survey_report = SiteSurveyReport(site_id=1)
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        site_mock,
        properties,
        current_date,
        state,
        survey_report,
    )


@pytest.fixture(name="deploy_crews_testing")
def deploy_crews_testing_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1
    site_mock.get_id = mocker.Mock(side_effect=lambda: site_mock.id)
    mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )

    mocker.patch.object(Method, "survey_site", mock_false_survey_site)
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    properties: dict = {
        pdc.Method_Params.N_CREWS: 1,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    weather = create_random_state()
    sites = [site_mock]
    mocker.patch.object(DaylightCalculatorAve, "__init__", mock_daylight_calculator_ave_init)
    daylight: DaylightCalculatorAve = DaylightCalculatorAve()

    survey_plans = [
        ScheduledSurveyPlanner(
            site=site,
            site_annual_rs=6,
            sim_start_date=date(2023, 1, 1),
            sim_end_date=date(2025, 12, 31),
            deployment_years=[2024, 2025],
            deployment_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        for site in sites
    ]
    workplan = Workplan(survey_plans, date=date(2023, 1, 1))
    return (sites, properties, weather, workplan, daylight)


@pytest.fixture(name="deploy_crews_testing2")
def deploy_crews_testing2_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1
    site_mock.get_id = mocker.Mock(side_effect=lambda: site_mock.id)
    mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
    mocker.patch.object(site_mock, "get_survey_cost", mock_get_survey_cost)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_determine_if_site_survey_can_be_completed",
        mock_determine_if_site_survey_can_be_completed,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    mocker.patch.object(Method, "survey_site", mock_survey_site)
    properties: dict = {
        pdc.Method_Params.N_CREWS: 5,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 500,
            pdc.Method_Params.PER_DAY: 0,
        },
    }
    weather = create_random_state()
    sites = [site_mock]
    mocker.patch.object(DaylightCalculatorAve, "__init__", mock_daylight_calculator_ave_init)
    daylight: DaylightCalculatorAve = DaylightCalculatorAve()

    survey_plans = [
        ScheduledSurveyPlanner(
            site=site,
            site_annual_rs=6,
            sim_start_date=date(2023, 1, 1),
            sim_end_date=date(2025, 12, 31),
            deployment_years=[2023, 2024, 2025],
            deployment_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        for site in sites
    ]
    workplan = Workplan(survey_plans, date=date(2023, 1, 1))
    return (sites, properties, weather, workplan, daylight)


def create_random_state():
    state = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for givendate in [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)]:
        for lat in [40, 35]:
            for long in [-75, -110]:
                temp = 20
                wind = 10
                precip = 0.5

                state[givendate][lat][long]["temp"] = temp
                state[givendate][lat][long]["wind"] = wind
                state[givendate][lat][long]["precip"] = precip

    return state


@pytest.fixture(name="deploy_crews_testing3")
def deploy_crews_testing3_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1
    site_mock.get_id = mocker.Mock(side_effect=lambda: site_mock.id)
    mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
    mocker.patch.object(site_mock, "get_survey_cost", mock_get_survey_cost)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_determine_if_site_survey_can_be_completed",
        mock_determine_if_site_survey_can_be_completed,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    mocker.patch.object(Method, "survey_site", mock_survey_site)
    properties: dict = {
        pdc.Method_Params.N_CREWS: 5,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 8,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 0,
            pdc.Method_Params.PER_DAY: 5,
        },
    }
    weather = create_random_state()
    sites = [site_mock]
    mocker.patch.object(DaylightCalculatorAve, "__init__", mock_daylight_calculator_ave_init)
    daylight: DaylightCalculatorAve = DaylightCalculatorAve()

    survey_plans = [
        ScheduledSurveyPlanner(
            site=site,
            site_annual_rs=6,
            sim_start_date=date(2023, 1, 1),
            sim_end_date=date(2025, 12, 31),
            deployment_years=[2023, 2024, 2025],
            deployment_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        for site in sites
    ]
    workplan = Workplan(survey_plans, date=date(2023, 1, 1))
    expected_deployment_stats = CrewDeploymentStats(
        deployment_cost=5.0, sites_visited=1, travel_time=2, survey_time=120
    )
    return (
        sites,
        properties,
        weather,
        workplan,
        daylight,
        expected_deployment_stats,
    )


@pytest.fixture(name="deploy_crews_testing4")
def deploy_crews_testing4_fix(mocker):
    # Initialize a list to hold mock sites
    mock_sites = []

    # Loop to create 4 mock sites
    for i in range(1, 5):
        # Create a mock object for Site with a unique id
        site_mock = mocker.Mock(spec=Site)
        site_mock.id = i
        # Pass the current value of i as a default argument to the lambda function
        site_mock.get_id = mocker.Mock(side_effect=lambda id=i: id)
        mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
        mocker.patch.object(site_mock, "get_survey_cost", mock_get_survey_cost)
        # Add the mock site to the list
        mock_sites.append(site_mock)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_determine_if_site_survey_can_be_completed",
        mock_determine_if_site_survey_can_be_completed,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    properties: dict = {
        pdc.Method_Params.N_CREWS: 1,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 9,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 0,
            pdc.Method_Params.PER_DAY: 5,
        },
    }
    weather = create_random_state()
    mocker.patch.object(DaylightCalculatorAve, "__init__", mock_daylight_calculator_ave_init)
    daylight: DaylightCalculatorAve = DaylightCalculatorAve()

    survey_plans = [
        ScheduledSurveyPlanner(
            site=site,
            site_annual_rs=6,
            sim_start_date=date(2023, 1, 1),
            sim_end_date=date(2025, 12, 31),
            deployment_years=[2023, 2024, 2025],
            deployment_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        for site in mock_sites
    ]
    workplan = Workplan(survey_plans, date=date(2023, 1, 1))
    expected_deployment_stats = CrewDeploymentStats(
        deployment_cost=5.0, sites_visited=4, travel_time=4, survey_time=480
    )
    return (
        mock_sites,
        properties,
        weather,
        workplan,
        daylight,
        expected_deployment_stats,
    )


@pytest.fixture(name="deploy_crews_testing5")
def deploy_crews_testing5_fix(mocker):
    # Initialize a list to hold mock sites
    mock_sites = []

    # Loop to create 8 mock sites
    for i in range(1, 9):
        # Create a mock object for Site with a unique id
        site_mock = mocker.Mock(spec=Site)
        site_mock.id = i
        # Pass the current value of i as a default argument to the lambda function
        site_mock.get_id = mocker.Mock(side_effect=lambda id=i: id)
        mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
        mocker.patch.object(site_mock, "get_survey_cost", mock_get_survey_cost)
        # Add the mock site to the list
        mock_sites.append(site_mock)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_determine_if_site_survey_can_be_completed",
        mock_determine_if_site_survey_can_be_completed,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    mocker.patch.object(
        Method, "_estimate_method_crews_required", mock_estimate_method_crews_required
    )
    properties: dict = {
        pdc.Method_Params.N_CREWS: 2,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 9,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 0,
            pdc.Method_Params.PER_DAY: 5,
        },
    }
    weather = create_random_state()
    mocker.patch.object(DaylightCalculatorAve, "__init__", mock_daylight_calculator_ave_init)
    daylight: DaylightCalculatorAve = DaylightCalculatorAve()

    survey_plans = [
        ScheduledSurveyPlanner(
            site=site,
            site_annual_rs=6,
            sim_start_date=date(2023, 1, 1),
            sim_end_date=date(2025, 12, 31),
            deployment_years=[2023, 2024, 2025],
            deployment_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        for site in mock_sites
    ]
    workplan = Workplan(survey_plans, date=date(2023, 1, 1))
    expected_deployment_stats = CrewDeploymentStats(
        deployment_cost=10.0, sites_visited=8, travel_time=8, survey_time=960
    )
    return (
        mock_sites,
        properties,
        weather,
        workplan,
        daylight,
        expected_deployment_stats,
    )


@pytest.fixture(name="deploy_crews_testing6")
def deploy_crews_testing6_fix(mocker):
    # Initialize a list to hold mock sites
    mock_sites = []

    # Loop to create 3 mock sites
    for i in range(1, 4):
        # Create a mock object for Site with a unique id
        site_mock = mocker.Mock(spec=Site)
        site_mock.id = i
        # Pass the current value of i as a default argument to the lambda function
        site_mock.get_id = mocker.Mock(side_effect=lambda id=i: id)
        mocker.patch.object(site_mock, "get_method_survey_time", mock_get_method_survey_time)
        mocker.patch.object(site_mock, "get_survey_cost", mock_get_survey_cost)
        # Add the mock site to the list
        mock_sites.append(site_mock)
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method, "_estimate_method_crews_required", mock_estimate_method_crews_required2
    )
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_determine_if_site_survey_can_be_completed",
        mock_determine_if_site_survey_can_be_completed,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(site_mock, "get_detectable_emissions", mock_get_detectable_emissions)
    properties: dict = {
        pdc.Method_Params.N_CREWS: 2,
        pdc.Method_Params.SENSOR: {
            pdc.Method_Params.TYPE: "default",
            pdc.Method_Params.MDL: 1,
            pdc.Method_Params.QE: {
                pdc.Method_Params.QUANTIFICATION_PARAMETERS: [0.0, 0.0],
                pdc.Method_Params.Q_TYPE: "default",
            },
        },
        pdc.Method_Params.DEPLOYMENT_TYPE: "mobile",
        pdc.Method_Params.MAX_WORKDAY: 9,
        pdc.Method_Params.CONSIDER_DAYLIGHT: False,
        pdc.Method_Params.T_BW_SITES: {pdc.Common_Params.VAL: [1]},
        pdc.Method_Params.IS_FOLLOW_UP: False,
        pdc.Method_Params.WEATHER_ENVS: {
            pdc.Method_Params.WIND: [0, 10],
            pdc.Method_Params.TEMP: [-30, 30],
            pdc.Method_Params.PRECIP: [0, 1],
        },
        pdc.Method_Params.REPORTING_DELAY: 0,
        pdc.Method_Params.COST: {
            pdc.Method_Params.UPFRONT: 1000,
            pdc.Method_Params.PER_SITE: 0,
            pdc.Method_Params.PER_DAY: 5,
        },
    }
    weather = create_random_state()
    mocker.patch.object(DaylightCalculatorAve, "__init__", mock_daylight_calculator_ave_init)
    daylight: DaylightCalculatorAve = DaylightCalculatorAve()

    survey_plans = [
        ScheduledSurveyPlanner(
            site=site,
            site_annual_rs=6,
            sim_start_date=date(2023, 1, 1),
            sim_end_date=date(2025, 12, 31),
            deployment_years=[2023, 2024, 2025],
            deployment_months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        )
        for site in mock_sites
    ]
    workplan = Workplan(survey_plans, date=date(2023, 1, 1))
    expected_deployment_stats = CrewDeploymentStats(
        deployment_cost=15.0, sites_visited=3, travel_time=3, survey_time=360
    )
    return (
        mock_sites,
        properties,
        weather,
        workplan,
        daylight,
        expected_deployment_stats,
    )
