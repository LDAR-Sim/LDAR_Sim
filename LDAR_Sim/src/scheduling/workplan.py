from dataclasses import dataclass, field
from datetime import date
from typing import Tuple
from scheduling.survey_planner import SurveyPlanner


@dataclass
class EmissionDetectionReport:
    site: str
    equipment_group: str
    equipment: str
    measured_rate: float
    true_rate: float
    current_date: date = None
    emis_start_date: date = None
    estimated_start_date: date = None


@dataclass
class EquipmentGroupSurveyReport:
    site: str
    equipment_group: str
    measured_rate: float
    true_rate: float
    survey_date: date = None
    emissions_detected: list[EmissionDetectionReport] = field(default_factory=list)


@dataclass
class SiteSurveyReport:
    site_id: str
    time_surveyed: int = 0
    time_spent_to_travel: int = 0
    survey_complete: bool = False
    survey_in_progress: bool = False
    equipment_groups_surveyed: list[EquipmentGroupSurveyReport] = field(default_factory=list)
    survey_level: str = None
    site_measured_rate: float = 0.0
    site_true_rate: float = 0.0
    site_flagged: bool = False
    survey_completion_date: date = None
    survey_start_date: date = None


@dataclass
class CrewDailyReport:
    crew_id: int
    day_time_remaining: int


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
            self._site_survey_reports[survey_plan.get_site().get_id()] = survey_plan

    def add_survey_report(
        self, survey_report: SiteSurveyReport, survey_planner: SurveyPlanner
    ) -> None:
        site_id: str = survey_report.site_id
        self._site_survey_reports.update(site_id, survey_report)
        self.site_survey_planners[site_id] = survey_planner

    def get_reports(self) -> Tuple[dict[str, SiteSurveyReport], dict[str, SurveyPlanner]]:
        return self._site_survey_reports, self._site_survey_planners
