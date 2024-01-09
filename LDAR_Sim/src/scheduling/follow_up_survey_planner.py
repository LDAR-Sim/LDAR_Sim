from datetime import date
from scheduling.workplan import SiteSurveyReport
from virtual_world.sites import Site


class FollowUpSurveyPlanner:
    def __init__(
        self, site: Site, original_survey_report: SiteSurveyReport, rep_delay: int
    ) -> None:
        self._site: Site = site
        self._orig_survey_report: SiteSurveyReport = original_survey_report
        self._current_date: date = original_survey_report.survey_completion_date
        self._reporting_delay: int = rep_delay
        self._queued: bool = False
        self._queue_date: date = None
        self._added_to_candidates = False
        self._candidate_date: date = None

    def update_date(self, current_date: date) -> None:
        self._current_date = current_date

    def deliver_report(self) -> bool:
        if not (self._queued and self._added_to_candidates):
            if (
                self._current_date - self._orig_survey_report.survey_completion_date
            ).days >= self._reporting_delay:
                return True
            else:
                return False
        else:
            raise Exception("Site Survey Report already queued")
