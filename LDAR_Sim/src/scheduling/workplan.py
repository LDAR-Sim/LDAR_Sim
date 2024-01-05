from dataclasses import dataclass, field
from datetime import date
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


@dataclass
class CrewDailyReport:
    crew_id: int
    day_time_remaining: int


class Workplan:
    def __init__(self, site_survey_plan_list: list[SurveyPlanner], date: date):
        self.site_survey_plan_list: list[SurveyPlanner] = site_survey_plan_list
        self.date = date
        self._init_site_survey_report_placeholder_list()

    def _init_site_survey_report_placeholder_list(self):
        self._site_survey_reports: dict = {}
        for survey_plan in self.site_survey_plan_list:
            self._site_survey_reports[survey_plan.get_site().get_id()] = None
