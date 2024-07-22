"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        Program
Purpose: Module for Program

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

import pandas as pd
from datetime import date, timedelta
from typing import Tuple, Any
from file_processing.output_processing.output_utils import (
    CrewDeploymentStats,
    TaggingFlaggingStats,
    TsMethodData,
)
from programs.equipment_group_level_method import EquipmentGroupLevelMethod
from programs.component_level_method import ComponentLevelMethod
from programs.site_level_method import SiteLevelMethod
from scheduling.schedule_dataclasses import MinimalSurveyReport
from scheduling.scheduling_utils import create_schedule

from virtual_world.sites import Site
from programs.method import Method
from scheduling.generic_schedule import GenericSchedule
from scheduling.workplan import Workplan


import constants.param_default_const as pdc


class Program:
    """An object responsible for scheduling surveys for all sites in the infrastructure.
    Uses other lower level objects to plan and schedule survey times and determine actual
    dynamic schedules based on weather and other impacting variables."""

    PROGRAM_REPORT_EXPANSION_MAPPING = {
        pdc.Duration_Method.COMPONENT: True,
        pdc.Duration_Method.MEASUREMENT_CONSERVATIVE: False,
    }

    def __init__(
        self,
        name: str,
        # TODO do away with state and just track anything we need from state separately.
        # From a quick look, the only things we need from it are weather are daylight hours,
        # which should be tracked on their own
        weather,
        daylight,
        methods: dict[str, dict],
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        consider_weather: bool,
        prog_params: dict[str, Any],
        input_dir: str,
    ) -> None:
        self.name: str = name
        self._input_dir: str = input_dir
        self._survey_schedules: dict[str, GenericSchedule] = {}
        self.method_names: list[str] = [method for method in methods]
        self._init_methods_and_schedules(
            methods, consider_weather, sites, sim_start_date, sim_end_date
        )
        self._current_date: date = sim_start_date
        self.weather = weather
        self.daylight = daylight
        self.duration_factor = prog_params[pdc.Program_Params.DURATION_ESTIMATE][
            pdc.Program_Params.DURATION_FACTOR
        ]
        self.duration_method = prog_params[pdc.Program_Params.DURATION_ESTIMATE][
            pdc.Program_Params.DURATION_METHOD
        ]
        self._component_level_emissions_estimation = Program.PROGRAM_REPORT_EXPANSION_MAPPING[
            self.duration_method
        ]
        self._survey_reports: list[MinimalSurveyReport] = []

    def _init_methods_and_schedules(
        self,
        methods: dict,
        consider_weather: bool,
        sites: list[Site],
        sim_start_date: date,
        sim_end_date: date,
    ) -> None:
        self._methods: list[Method] = []
        follow_up_method_list: list[Method] = []

        follow_up_methods, non_follow_up_methods = self.split_methods(methods)

        for method_name, properties in follow_up_methods.items():
            method_name: str
            properties: dict

            method: Method = ComponentLevelMethod(
                method_name, properties, consider_weather, sites, self._input_dir
            )

            follow_up_method_list.append(method)

            self._survey_schedules[method_name] = create_schedule(
                method_name=method_name,
                method_details=properties,
                sites=sites,
                sim_start_date=sim_start_date,
                sim_end_date=sim_end_date,
                est_meth_daily_surveys=method.estimate_average_daily_surveys(),
                method_avail_crews=method.get_crew_count(),
            )

        for method_name, properties in non_follow_up_methods.items():
            method_name: str

            method: Method = self._gen_method(method_name, properties, consider_weather, sites)

            self._methods.append(method)

            self._survey_schedules[method_name] = create_schedule(
                method_name=method_name,
                method_details=properties,
                sites=sites,
                sim_start_date=sim_start_date,
                sim_end_date=sim_end_date,
                est_meth_daily_surveys=method.estimate_average_daily_surveys(),
                method_avail_crews=method.get_crew_count(),
            )
        self._methods.extend(follow_up_method_list)

    def split_methods(self, methods: dict) -> Tuple[dict, dict]:
        follow_up_methods: dict = {}
        other_methods: dict = {}
        for method, properties in methods.items():
            if properties[pdc.Method_Params.IS_FOLLOW_UP]:
                follow_up_methods[method] = properties
            else:
                other_methods[method] = properties
        return follow_up_methods, other_methods

    def _gen_method(
        self,
        method_name: str,
        properties: dict,
        consider_weather: bool,
        sites: list[Site],
    ) -> Method:
        method_survey_level: str = properties[pdc.Method_Params.MEASUREMENT_SCALE]

        if method_survey_level == SiteLevelMethod.MEASUREMENT_SCALE:
            meth_pref_follow_up = properties[pdc.Method_Params.FOLLOW_UP][
                pdc.Method_Params.PREFERRED_METHOD
            ]

            if isinstance(meth_pref_follow_up, str) and meth_pref_follow_up != "_placeholder_str_":
                follow_up_schedule: GenericSchedule = self._survey_schedules[meth_pref_follow_up]
            else:
                _, follow_up_schedule = next(iter(self._survey_schedules.items()))
                follow_up_schedule: GenericSchedule

            return SiteLevelMethod(
                method_name,
                properties,
                consider_weather,
                sites=sites,
                follow_up_schedule=follow_up_schedule,
                input_dir=self._input_dir,
            )
        elif method_survey_level == EquipmentGroupLevelMethod.MEASUREMENT_SCALE:
            meth_pref_follow_up = properties[pdc.Method_Params.FOLLOW_UP][
                pdc.Method_Params.PREFERRED_METHOD
            ]

            if isinstance(meth_pref_follow_up, str) and meth_pref_follow_up != "_placeholder_str_":
                follow_up_schedule: GenericSchedule = self._survey_schedules[meth_pref_follow_up]
            else:
                _, follow_up_schedule = next(iter(self._survey_schedules.items()))
                follow_up_schedule: GenericSchedule

            return EquipmentGroupLevelMethod(
                method_name,
                properties,
                consider_weather,
                sites=sites,
                follow_up_schedule=follow_up_schedule,
                input_dir=self._input_dir,
            )
        elif method_survey_level == ComponentLevelMethod.MEASUREMENT_SCALE:
            return ComponentLevelMethod(
                method_name, properties, consider_weather, sites, self._input_dir
            )

    def do_daily_program_deployment(self) -> list[TsMethodData]:
        timeseries_methods_data: list[TsMethodData] = []
        # TODO may need to split up methods and follow_up methods
        for method in self._methods:
            method_schedule: GenericSchedule = self._survey_schedules[method.get_name()]
            method_workplan: Workplan = method_schedule.get_workplan(self._current_date)
            deployment_stats: CrewDeploymentStats = method.deploy_crews(
                method_workplan, self.weather, self.daylight
            )
            self._survey_reports.extend(
                method_schedule.update(
                    method_workplan, self._current_date, self._component_level_emissions_estimation
                )
            )
            tags_flags: TaggingFlaggingStats = method.update(self._current_date)
            timeseries_methods_data.append(
                TsMethodData(
                    method_name=method.get_name(),
                    upfront_cost=method.get_upfront_cost(),
                    daily_deployment_cost=deployment_stats.deployment_cost,
                    daily_flags=tags_flags.sites_flagged,
                    daily_tags=tags_flags.leaks_tagged,
                    sites_visited=deployment_stats.sites_visited,
                    travel_time=deployment_stats.travel_time,
                    survey_time=deployment_stats.survey_time,
                )
            )
        return timeseries_methods_data

    def update_date(self) -> None:
        """Increment the current date counter"""
        self._current_date += timedelta(days=1)

    def get_method_names(self) -> list[str]:
        return self.method_names

    def aggregate_method_survey_reports(self) -> pd.DataFrame:
        """Aggregate the survey reports from all methods"""

        data: list[dict] = [report.to_report_summary() for report in self._survey_reports]

        df: pd.DataFrame = pd.DataFrame(data)

        return df
