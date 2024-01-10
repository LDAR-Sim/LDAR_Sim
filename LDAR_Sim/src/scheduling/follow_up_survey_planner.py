from datetime import date
import sys

from numpy import average
from scheduling.schedule_dataclasses import SiteSurveyReport
from virtual_world.sites import Site


class FollowUpSurveyPlanner:
    REDUND_FILTER_RECENT = "recent"
    REDUND_FILTER_MAX = "max"
    REDUND_FILTER_AVERAGE = "average"

    INVALID_REDUND_FILTER_ERROR = "Error: Invalid Redundancy filter: {filter} for method: {method}"

    def __init__(
        self, site: Site, original_survey_report: SiteSurveyReport, rep_delay: int
    ) -> None:
        self.rate_at_site: float = original_survey_report.site_measured_rate
        self._site: Site = site
        self.site_id: str = site.get_id()
        self._orig_survey_report: SiteSurveyReport = original_survey_report
        self._current_date: date = original_survey_report.survey_completion_date
        self._reporting_delay: int = rep_delay
        self._other_survey_reports: list[SiteSurveyReport] = []

    def update_date(self, current_date: date) -> None:
        self._current_date = current_date

    def deliver_report(self) -> bool:
        if (
            self._current_date - self._orig_survey_report.survey_completion_date
        ).days >= self._reporting_delay:
            return True
        else:
            return False

    def update_with_latest_survey(self, new_report: SiteSurveyReport, redund_filter: str) -> None:
        if redund_filter == self.REDUND_FILTER_RECENT:
            self.rate_at_site = new_report.site_measured_rate
            self._other_survey_reports.append(new_report)
        elif redund_filter == self.REDUND_FILTER_AVERAGE:
            site_rates: list[float] = [
                report.site_measured_rate for report in self._other_survey_reports
            ]
            site_rates.append(self._orig_survey_report.site_measured_rate)
            self.rate_at_site = average(site_rates)
            self._other_survey_reports.append(new_report)
        elif redund_filter == self.REDUND_FILTER_MAX:
            site_rates: list[float] = [
                report.site_measured_rate for report in self._other_survey_reports
            ]
            site_rates.append(self._orig_survey_report.site_measured_rate)
            self.rate_at_site = max(site_rates)
            self._other_survey_reports.append(new_report)
        else:
            print(
                self.INVALID_REDUND_FILTER_ERROR.format(
                    filter=redund_filter, method=new_report.method
                )
            )
            sys.exit()
