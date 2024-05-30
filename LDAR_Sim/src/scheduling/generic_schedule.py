"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        generic_schedule
Purpose: Contains the generic schedule module. This provides a survey queue for a given LDAR
method so that sites can be queued to be surveyed. 

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
from virtual_world.sites import Site
from scheduling.schedule_dataclasses import SiteSurveyReport
from scheduling.scheduled_survey_planner import ScheduledSurveyPlanner
from utils.queue import PriorityQueueWithFIFO


class GenericSchedule:
    """A generic schedule class that provides a survey queue for a give LDAR method so that
    sites can be queued to be surveyed. Schedule classes specific to method types will inherit
    from this class and overwrite it's default behavior where necessary.
    """

    # Default = 3 - where everything initially starts out
    # 2 - Sites which have been popped for the day but were not attended to
    # 1 - Sites that have surveys which have been started but not finished.
    DEFAULT_SURVEY_PRIORITY = 3
    QUEUED_SURVEY_PRIORITY = 2
    UNFINISHED_SURVEY_HIGHEST_PRIORITY = 1

    def __init__(
        self,
        method_name: str,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        est_meth_daily_surveys: int,
        method_avail_crews: int,
    ) -> None:
        self._method: str = method_name
        self._survey_queue = PriorityQueueWithFIFO()
        self._est_meth_daily_surveys: int = est_meth_daily_surveys
        self._method_crews: int = method_avail_crews
        self._survey_plans: list[ScheduledSurveyPlanner] = self._set_survey_plans(
            sim_start_date, sim_end_date, sites
        )

    def _set_survey_plans(
        self, sim_start_date, sim_end_date, sites: list[Site]
    ) -> list[ScheduledSurveyPlanner]:
        survey_plans: list[ScheduledSurveyPlanner] = []
        for site in sites:
            # TODO flush out what survey planner needs as inputs for the constructor
            survey_freq: int = site._survey_frequencies[self._method]
            # TODO: make sure this is in the correct place....
            deploy_meth: bool = site.check_site_deployable(self._method)
            if survey_freq is None or not deploy_meth:
                survey_freq = 0
            deploy_year: int = site._deployment_years[self._method]
            deploy_month: int = site._deployment_months[self._method]
            survey_plans.append(
                ScheduledSurveyPlanner(
                    site,
                    survey_freq,
                    sim_start_date,
                    sim_end_date,
                    deploy_year,
                    deploy_month,
                )
            )
        return survey_plans

    def add_to_survey_queue(self, survey_plan: ScheduledSurveyPlanner) -> None:
        """Add the supplied site to the survey queue to surveyed

        Args:
            site (Site): The site to be added to the survey queue
        """
        self._survey_queue.put(GenericSchedule.DEFAULT_SURVEY_PRIORITY, survey_plan)

    def add_unfinished_to_survey_queue(self, survey_plan: ScheduledSurveyPlanner) -> None:
        """Add the supplied, partial surveyed site to queue

        Args:
            site (Site) : the Site to be added to the survey queue"""
        self._survey_queue.put(GenericSchedule.UNFINISHED_SURVEY_HIGHEST_PRIORITY, survey_plan)

    def add_previous_queued_to_survey_queue(self, survey_plan: ScheduledSurveyPlanner) -> None:
        """Add the supplied, unattended site back to queue

        Args:
            site (Site) : the Site to be added to the survey queue"""
        self._survey_queue.put(GenericSchedule.QUEUED_SURVEY_PRIORITY, survey_plan)

    def get_daily_sites_to_survey(self) -> "list[ScheduledSurveyPlanner]":
        """This method will go through the method survey queue and return
        the daily sites that are planned to be surveyed by the given method

        Returns the list of highest priority survey plans, based on the number of crews available
        and the number of sites the average crew can do in a day
        """
        daily_plan: list[ScheduledSurveyPlanner] = []

        for crew in range(self._method_crews):
            site_count: int = 0
            for site_count in range(self._est_meth_daily_surveys):
                if not self._survey_queue.empty():
                    prio, _, survey_plan = self._survey_queue.get()
                    daily_plan.append(survey_plan)
                else:
                    break

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
        sites_to_survey: list[ScheduledSurveyPlanner] = self.get_daily_sites_to_survey()
        return Workplan(site_survey_plan_list=sites_to_survey, date=current_date)

    def update(self, workplan: Workplan, current_date: date) -> None:
        reports, planners = workplan.get_reports()
        reports: dict[str, SiteSurveyReport]
        planners: dict[str, ScheduledSurveyPlanner]

        for site_id, report in reports.items():
            planner: ScheduledSurveyPlanner = planners[site_id]

            if not report.survey_complete:
                if report.survey_in_progress:
                    self.add_unfinished_to_survey_queue(planner)
                else:
                    self.add_previous_queued_to_survey_queue(planner)
            else:
                planner.add_to_surveys_done(current_date)
