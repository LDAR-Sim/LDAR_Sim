"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        survey_site_testing_resources.py
Purpose: Module for setup for testing survey_site for Methods

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

from typing import Tuple
from pytest_mock import MockerFixture
from scheduling.schedule_dataclasses import CrewDailyReport
from virtual_world.infrastructure import Site
from programs.method import Method
from sensors.default_sensor import DefaultSensor
from constants import param_default_const as pdc


def mock_site_initialization(self, site_properties: dict):
    for property, value in site_properties.items():
        setattr(self, property, value)


def mock_method_initialization(self, name: str, method_properties: dict, mock_sensor):
    self._name = name
    self._weather = False
    self._sensor = mock_sensor
    for property, value in method_properties.items():
        setattr(self, f"_{property}", value)


def setup_mock_objects_for_survey_report_testing(
    mocker: MockerFixture, site_properties: dict, method_properties: dict, crew_time: int
) -> Tuple[Site, Method, CrewDailyReport]:

    mocker.patch.object(Site, "__init__", mock_site_initialization)
    mocker.patch.object(
        Site, "get_method_survey_time", return_value=site_properties[pdc.Method_Params.TIME]
    )
    mock_site: Site = Site(site_properties)

    mocker.patch.object(Method, "__init__", mock_method_initialization)
    mock_sensor: DefaultSensor = mocker.Mock()
    mock_sensor.detect_emissions.return_value = True
    method: Method = Method("test_method", method_properties, mock_sensor)

    daily_report = CrewDailyReport(1, crew_time)

    return mock_site, method, daily_report
