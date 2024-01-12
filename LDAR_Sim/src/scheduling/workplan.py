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
