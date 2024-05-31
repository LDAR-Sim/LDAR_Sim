"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        stationary_schedule
Purpose: The extended schedule module for stationary types. 

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

from datetime import date
from scheduling.workplan import Workplan
from scheduling.generic_schedule import GenericSchedule
from scheduling.scheduled_survey_planner import StationarySurveyPlanner
from virtual_world.sites import Site
from constants.param_default_const import Deployment_Types as dt


class StationarySchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "stationary" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = dt.STATIONARY

    def __init__(
        self,
        method_name: str,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        est_meth_daily_surveys: int,
        method_avail_crews: int,
    ) -> None:
        super().__init__(
            method_name,
            sites,
            sim_start_date,
            sim_end_date,
            est_meth_daily_surveys,
            method_avail_crews,
        )
        return

    def _set_survey_plans(
        self, sim_start_date, sim_end_date, sites: list[Site]
    ) -> list[StationarySurveyPlanner]:
        survey_plans: list[StationarySurveyPlanner] = []
        for site in sites:
            survey_freq = 365
            deploy_year: int = site._deployment_years[self._method]
            deploy_month: int = site._deployment_months[self._method]
            survey_plans.append(
                StationarySurveyPlanner(
                    site,
                    survey_freq,
                    sim_start_date,
                    sim_end_date,
                    deploy_year,
                    deploy_month,
                )
            )
        return survey_plans

    def get_daily_sites_to_survey(self) -> list[StationarySurveyPlanner]:
        daily_plan: list[StationarySurveyPlanner] = []
        while not self._survey_queue.empty():
            prio, _, survey_plan = self._survey_queue.get()
            daily_plan.append(survey_plan)
        return daily_plan

    def get_workplan(self, current_date) -> Workplan:
        """
        Updates the survey plans,
        Adds necessary sites to the queue
        Returns:
            The list sites that the method should do on the given day
        """
        for survey_plan in self._survey_plans:
            survey_plan.update_date(current_date)
            if survey_plan.queue_site_for_survey():
                self.add_to_survey_queue(survey_plan)
