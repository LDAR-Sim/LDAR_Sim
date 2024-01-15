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
from datetime import date, timedelta
from typing import Tuple
from programs.equipment_group_level_method import EquipmentGroupLevelMethod
from programs.equipment_level_method import EquipmentLevelMethod
from programs.site_level_method import SiteLevelMethod
from scheduling.scheduling_utils import create_schedule

from virtual_world.sites import Site
from programs.method import Method
from scheduling.generic_schedule import GenericSchedule
from scheduling.workplan import Workplan


class Program:
    """An object responsible for scheduling surveys for all sites in the infrastructure.
    Uses other lower level objects to plan and schedule survey times and determine actual
    dynamic schedules based on weather and other impacting variables."""

    def __init__(
        self,
        # TODO do away with state and just track anything we need from state separately.
        # From a quick look, the only things we need from it are weather are daylight hours,
        # which should be tracked on their own
        state,
        methods: dict,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        consider_weather: bool,
    ) -> None:
        self._survey_schedules: dict[str, GenericSchedule] = {}
        self._init_methods_and_schedules(
            methods, consider_weather, sites, sim_start_date, sim_end_date
        )
        self._current_date: date = sim_start_date
        self.state = state

    def _init_methods_and_schedules(
        self,
        methods: dict,
        consider_weather: bool,
        sites: list[Site],
        sim_start_date: date,
        sim_end_date: date,
    ) -> None:
        self._methods: list[Method] = []

        follow_up_methods, non_follow_up_methods = self.split_methods(methods)

        for method_name, properties in follow_up_methods.items():
            method_name: str
            properties: dict

            method: Method = EquipmentLevelMethod(method_name, properties, consider_weather, sites)

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

    def split_methods(self, methods: dict) -> Tuple[dict, dict]:
        follow_up_methods: dict = {}
        other_methods: dict = {}
        for method, properties in methods.items():
            if properties[Method.FOLLOW_UP_ACCESSOR]:
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
        method_survey_level: str = properties[Method.MEASUREMENT_SCALE_ACCESSOR]

        if method_survey_level == SiteLevelMethod.MEASUREMENT_SCALE:
            meth_pref_follow_up = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
                Method.METHOD_FOLLOW_UP_PROPERTIES_PREF_FU_ACCESSOR
            ]

            if isinstance(meth_pref_follow_up, str) and meth_pref_follow_up != "_placeholder_str_":
                follow_up_schedule: GenericSchedule = self._survey_schedules[meth_pref_follow_up]
            else:
                follow_up_schedule: GenericSchedule = next(iter(self._survey_schedules.items()))

            return SiteLevelMethod(
                method_name,
                properties,
                consider_weather,
                follow_up_schedule=follow_up_schedule,
            )
        elif method_survey_level == EquipmentGroupLevelMethod.MEASUREMENT_SCALE:
            meth_pref_follow_up = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
                Method.METHOD_FOLLOW_UP_PROPERTIES_PREF_FU_ACCESSOR
            ]

            if isinstance(meth_pref_follow_up, str) and meth_pref_follow_up != "_placeholder_str_":
                follow_up_schedule: GenericSchedule = self._survey_schedules[meth_pref_follow_up]
            else:
                follow_up_schedule: GenericSchedule = next(iter(self._survey_schedules.items()))

            return EquipmentGroupLevelMethod(
                method_name,
                properties,
                consider_weather,
                follow_up_schedule=follow_up_schedule,
            )
        elif method_survey_level == EquipmentLevelMethod.MEASUREMENT_SCALE:
            return EquipmentLevelMethod(method_name, properties, consider_weather, sites)

    def do_daily_program_deployment(self) -> None:
        # TODO may need to split up methods and follow_up methods
        for method in self._methods:
            method_schedule: GenericSchedule = self._survey_schedules[method.get_name()]
            method_workplan: Workplan = method_schedule.get_workplan(self._current_date)
            method.deploy_crews(method_workplan, self.state["weather"])
            method_schedule.update(method_workplan, self._current_date)

    def update_date(self) -> None:
        """Increment the current date counter"""
        self._current_date += timedelta(days=1)
