from scheduling.schedule_dataclasses import SiteSurveyReport
from virtual_world.sites import Site


class SurveyPlanner:
    def __init__(
        self,
        site: Site,
    ) -> None:
        self._site: Site = site
        self._active_survey_report: SiteSurveyReport = None

    def get_site(self) -> Site:
        return self._site

    def get_current_survey_report(self) -> SiteSurveyReport:
        if self._active_survey_report is None:
            self._active_survey_report = SiteSurveyReport(self._site.get_id())
            return self._active_survey_report
        else:
            return self._active_survey_report
