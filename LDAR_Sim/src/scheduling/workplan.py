"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        workplan
Purpose: The workplan module.

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
from typing import Tuple
from scheduling.survey_planner import SurveyPlanner
from scheduling.schedule_dataclasses import SiteSurveyReport


class Workplan:
    def __init__(self, site_survey_plan_list: list[SurveyPlanner], date: date) -> None:
        self.date: date = date
        self.total_travel_time: float = 0
        self._init_site_survey_report_placeholder_list(site_survey_plan_list)

    def _init_site_survey_report_placeholder_list(
        self, site_survey_plan_list: list[SurveyPlanner]
    ) -> None:
        self._site_survey_reports: dict[str, SiteSurveyReport] = {}
        self.site_survey_planners: dict[str, SurveyPlanner] = {}
        for survey_plan in site_survey_plan_list:
            self.site_survey_planners[survey_plan.get_site().get_id()] = survey_plan

    def __reduce__(self):
        # Serialize relevant state information
        args = (self.site_survey_planners, self.date)
        # Return a tuple with the constructor and its arguments
        return (self.__class__._reconstruct, args)

    @classmethod
    def _reconstruct(cls, site_survey_planners, date):
        # Reconstruct the object using the serialized state
        instance = cls.__new__(cls)
        instance.date = date
        instance.site_survey_planners = site_survey_planners
        # Recalculate total travel time or any other necessary initialization
        return instance

    def add_survey_report(
        self, survey_report: SiteSurveyReport, survey_planner: SurveyPlanner
    ) -> None:
        site_id: str = survey_report.site_id
        self._site_survey_reports[site_id] = survey_report
        self.site_survey_planners[site_id] = survey_planner

    def get_reports(
        self,
    ) -> Tuple[dict[str, SiteSurveyReport], dict[str, SurveyPlanner]]:
        return self._site_survey_reports, self.site_survey_planners
