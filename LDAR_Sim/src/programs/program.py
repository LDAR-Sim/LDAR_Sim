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

from virtual_world.sites import Site
from programs.method import Method
from scheduling.schedules import GenericSchedule, create_schedule
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
        self._init_methods_and_schedules(
            methods, consider_weather, sites, sim_start_date, sim_end_date
        )
        self._survey_schedules: dict[str, GenericSchedule] = {}
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
        for method_name, properties in methods.items():
            method_name: str
            properties: dict

            method = Method(method_name, properties, consider_weather)

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

    def do_daily_program_deployment(self) -> None:
        for method in self._methods:
            method_schedule: GenericSchedule = self._survey_schedules[method.get_name()]
            method_workplan: Workplan = method_schedule.get_workplan(self._current_date)
            method.deploy_crews(method_workplan)
            method_schedule.update(method_workplan)

        self.update_date()

    # # TODO define a method workplan object that they can use to track progress on
    # # surveying sites for a day
    # def get_method_workplan(self, method : str) -> Workplan:
    #     """Determine daily workplans for the given method for the day.
    #     The workplans will help methods track with sites to survey and report progress.

    #     Returns:
    #         Workplan: An object containing the list of sites to attempt to survey for the day
    #         that can be updated to report survey progress and discovered leaks.
    #     """
    #     for meth in self._methods:
    #         if meth._name == method:
    #             return meth.return_workplan()

    #     return

    def update_date(self) -> None:
        """Increment the current date counter"""
        self._current_date += timedelta(days=1)

    def update_schedule_based_on_workplan_results(self):
        """
        Call updates on the schedules for the next day based on the
        workplan returned by the method after a days work
        """
        for method in self._methods:
            workplan = method.return_workplan()
            for site in workplan._site_survey_reports:
                if site.survey_in_progress:
                    return
                    # TODO : add in progress survey with high prio to relevant method schedule
                elif not site.survey_complete:
                    return
                #     # TODO: add just queued survey back to schdule with med prio

                else:
                    return
                #     # TODO: adjust the site such that it's no longer flagged as queued
                #     #self._survey_schedules[method._name].
                #     # survey_planner.unflag_for_queue()
