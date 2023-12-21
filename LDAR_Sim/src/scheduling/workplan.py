from dataclasses import dataclass, field
from datetime import datetime
from virtual_world.sites import Site


@dataclass
class EmissionDetectionReport:
    site: int
    equipment_group: str
    equipment: str
    measured_rate: float
    true_rate: float
    start_date: datetime
    estimated_start_date: datetime


@dataclass
class SiteSurveyReport:
    site_id: int
    time_surveyed: int = 0
    time_spent_to_travel: int = 0
    survey_complete: bool = False
    survey_in_progress: bool = False
    emissions_detected: list[EmissionDetectionReport] = field(default_factory=list)
    survey_level: str = None
    site_measured_rate: float = 0.0
    site_true_rate: float = 0.0
    site_flagged: bool = False


@dataclass
class CrewDailyReport:
    crew_id: int
    day_time_remaining: int


class Workplan:
    def __init__(self, site_survey_list: list[Site]):
        self._site_survey_list: list[Site] = site_survey_list
        self._init_site_survey_report_placeholder_list()

    def _init_site_survey_report_placeholder_list(self):
        self._site_survey_reports: dict = {}
        for site in self._site_survey_list:
            self._site_survey_list[site.get_id()] = None
