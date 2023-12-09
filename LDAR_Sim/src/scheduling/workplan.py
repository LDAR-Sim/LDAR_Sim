from dataclasses import dataclass
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
    time_surveyed: int
    time_spent_to_travel: int
    survey_complete: bool
    survey_in_progress: bool
    net_site_emissions_rate: float
    emissions_detected: list[EmissionDetectionReport]
    survey_level: str


class Workplan:
    def __init__(self, site_survey_list: list[Site]):
        self._site_survey_list: list[Site] = site_survey_list
        self._init_site_survey_report_placeholder_list()

    def _init_site_survey_report_placeholder_list(self):
        self._site_survey_reports: dict = {}
        for site in self._site_survey_list:
            self._site_survey_list[site.get_id()] = None
