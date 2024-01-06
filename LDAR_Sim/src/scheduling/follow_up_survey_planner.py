from datetime import date, timedelta
from scheduling.workplan import SiteSurveyReport
from virtual_world.sites import Site


class FollowUpSurveyPlanner:
    def __init__(
        self,
        site: Site,
        original_survey_report: SiteSurveyReport,
        sim_start_date: date,
    ) -> None:
        self._site: Site = site
        self._current_date: date = sim_start_date - timedelta(days=1)
        self._orig_survey_report: SiteSurveyReport = original_survey_report
