"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        mobile_schedule
Purpose: The extended scheduling module, to provide scheduling functionality for
methods classified as "mobile". 

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
from scheduling.schedule_dataclasses import SiteSurveyReport
from scheduling.generic_schedule import GenericSchedule
from scheduling.scheduled_survey_planner import ScheduledSurveyPlanner
from scheduling.workplan import Workplan
from virtual_world.sites import Site


class MobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

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

    def update(self, workplan: Workplan, current_date: date) -> None:
        reports, planners = workplan.get_reports()
        reports: dict[str, SiteSurveyReport]
        planners: dict[str, ScheduledSurveyPlanner]

        for site_id, report in reports.items():
            planner: ScheduledSurveyPlanner = planners[site_id]
            # If the survey of the site was not completed,
            # it needs to be queued to be surveyed again
            if not report.survey_complete:
                if report.survey_in_progress:
                    self.add_unfinished_to_survey_queue(planner)
                else:
                    self.add_previous_queued_to_survey_queue(planner)
