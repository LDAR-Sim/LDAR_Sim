from datetime import date, timedelta
from math import ceil
import sys

from sortedcontainers import SortedList
from scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule
from scheduling.follow_up_survey_planner import FollowUpSurveyPlanner
from scheduling.schedule_dataclasses import SiteSurveyReport
from scheduling.generic_schedule import GenericSchedule
from scheduling.survey_planner import SurveyPlanner
from scheduling.workplan import Workplan
from virtual_world.sites import Site


class MobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

    THRESHOLD_INT_PRIO = "threshold"
    PROPORTION_INT_PRIO = "proportion"
    INVALID_INTERACTION_PRIO_ERROR = (
        "Error: Invalid interaction_priority of {priority} set for method: {method}"
    )

    def __init__(
        self,
        method_name: str,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        est_meth_daily_surveys: int,
        method_avail_crews: int,
        threshold: float,
        proportion: float,
        instant_threshold: float,
        interaction_priority: str,
        redund_filter: str,
        delay: int,
        reporting_delay: int,
        follow_up_schedule: FollowUpMobileSchedule,
    ) -> None:
        super().__init__(
            method_name,
            sites,
            sim_start_date,
            sim_end_date,
            est_meth_daily_surveys,
            method_avail_crews,
        )
        if interaction_priority == self.THRESHOLD_INT_PRIO:
            self._threshold_first: bool = True
        elif interaction_priority == self.PROPORTION_INT_PRIO:
            self._threshold_first: bool = False
        else:
            print(
                self.INVALID_INTERACTION_PRIO_ERROR.format(
                    priority=interaction_priority, method=method_name
                )
            )
            sys.exit()
        self._pending_reports: set[FollowUpSurveyPlanner] = set()
        self._candidates_for_flags: SortedList[FollowUpSurveyPlanner] = SortedList(
            key=lambda x: -x.rate_at_site
        )
        self._site_IDs_in_consideration_for_flag: dict[str, bool] = {
            site.get_id(): False for site in sites
        }
        self._site_IDs_in_follow_up_queue: dict[
            str, bool
        ] = follow_up_schedule.get_site_id_queue_list()
        self._first_candidate_date: date = None
        self._delay: int = delay
        self._reporting_delay: int = reporting_delay
        self._proportion: float = proportion
        self._threshold: float = threshold
        self._inst_threshold: float = instant_threshold
        self._redund_filter: str = redund_filter
        self._follow_up_schedule: FollowUpMobileSchedule = follow_up_schedule
        self._detection_count = 0
        self._survey_reports: dict[str, list[SiteSurveyReport]] = {
            site.get_id(): [] for site in sites
        }
        return

    def update(self, workplan: Workplan, current_date: date) -> None:
        reports, planners = workplan.get_reports()
        reports: dict[str, SiteSurveyReport]
        planners: dict[str, SurveyPlanner]

        for site_id, report in reports.items():
            planner: SurveyPlanner = planners[site_id]
            # If the survey of the site was not completed,
            # it needs to be queued to be surveyed again
            if not report.survey_complete:
                if report.survey_in_progress:
                    self.add_unfinished_to_survey_queue(planner)
                else:
                    self.add_previous_queued_to_survey_queue(planner)
            # Otherwise, the survey was completed and the detection results must be processed
            else:
                # TODO add user configurable follow_up parameter to allow
                # for up to a certain % variation between rates
                in_processing_for_follow_up: bool = (
                    self._site_IDs_in_consideration_for_flag[report.site_id]
                    and self._site_IDs_in_follow_up_queue[report.site_id]
                )
                if not (
                    report.site_measured_rate
                    == self._survey_reports[report.site_id][-1].site_measured_rate
                    and in_processing_for_follow_up
                ):
                    if report.site_measured_rate >= self._threshold:
                        self.add_pending_report(planner.get_site(), report, self._reporting_delay)
                    elif report.site_measured_rate > 0:
                        self._detection_count += 1
                        if self._first_candidate_date is None:
                            self._first_candidate_date = current_date + timedelta(
                                days=self._reporting_delay
                            )
                    self._survey_reports[report.site_id].append(report)
        # Go through the holding list for reports waiting on their
        # reporting delay and move them to candidates,
        # then queue candidates based on follow up work practice specified.
        self.update_candidates_for_flags(current_date)

    def add_pending_report(
        self,
        site: Site,
        report: SiteSurveyReport,
        reporting_delay: int,
    ) -> None:
        survey_plan: FollowUpSurveyPlanner = FollowUpSurveyPlanner(
            site=site, original_survey_report=report, rep_delay=reporting_delay
        )
        self._pending_reports.add(survey_plan)

    def update_candidates_for_flags(self, current_date: date) -> Workplan:
        self.update_pending_rep_state(current_date)

        candidates_empty: bool = bool(self._candidates_for_flags)

        if self._first_candidate_date is None:
            if not candidates_empty:
                self._first_candidate_date = current_date

        if (current_date - self._first_candidate_date).days >= self._delay:
            self._filter_candidates_by_proportion()

            for survey_plan in self._get_candidates():
                self.add_to_survey_queue(survey_plan)

    def update_pending_rep_state(self, current_date: date) -> None:
        # Save a set of the survey plans that are done the reporting delay
        # This lets us use set subtraction to remove all of the these
        # survey plans from the set of survey plans still waiting for their reporting delay
        reports_finished_pending: set[FollowUpSurveyPlanner] = set()
        # Go through all the pending reports and update the date of their survey plan
        # Then check if they should be delivered
        for survey_plan in self._pending_reports():
            survey_plan: FollowUpSurveyPlanner
            survey_plan.update_date(current_date)
            # If the survey plan report should be delivered, Ie: its reporting delay has passed
            if survey_plan.deliver_report():
                # Add the report to the set of ready reports
                reports_finished_pending.add(survey_plan)
                # If the site is already in the list for potential flags, pop it from the list,
                # update it based on the new measurements and the redundancy filter, and either
                # add it back to the list or bypass the list if it now passes the instant threshold.
                if self._site_IDs_in_consideration_for_flag(survey_plan.site_id):
                    existing_plan: FollowUpSurveyPlanner = self._get_plan_from_candidates(
                        survey_plan.site_id
                    )
                    existing_plan.update_with_latest_survey(survey_plan, self._redund_filter)
                    if existing_plan.rate_at_site >= self._inst_threshold:
                        self._follow_up_schedule.add_previous_queued_to_survey_queue(existing_plan)
                    else:
                        self._candidates_for_flags.add(existing_plan)
                # If the site is already queued to get a follow-up,
                # update the queue priority based on new results
                elif self._site_IDs_in_follow_up_queue(survey_plan.site_id):
                    existing_plan: FollowUpSurveyPlanner = (
                        self._follow_up_schedule.get_plan_from_queue(survey_plan.site_id)
                    )
                    if existing_plan.rate_at_site >= self._inst_threshold:
                        self._follow_up_schedule.add_previous_queued_to_survey_queue(existing_plan)
                    else:
                        self._follow_up_schedule.add_to_survey_queue(existing_plan)
                # Otherwise, the site is not already in processing for a follow-up,
                # process as normal
                else:
                    if survey_plan.rate_at_site >= self._inst_threshold:
                        self._follow_up_schedule.add_previous_queued_to_survey_queue(survey_plan)
                    else:
                        self._candidates_for_flags.add(survey_plan)

        self._pending_reports -= reports_finished_pending

    def _get_plan_from_candidates(self, site_id: str) -> FollowUpSurveyPlanner:
        survey_plan: FollowUpSurveyPlanner = next(
            [plan for plan in self._candidates_for_flags if plan.site_id == site_id], None
        )
        self._candidates_for_flags.remove(survey_plan)
        return survey_plan

    def _filter_candidates_by_proportion(self) -> None:
        # If interaction priority is threshold first, simply get the number of
        # candidates to keep by calculating the proportion of the total_candidates
        if self._threshold_first:
            total_candidates: int = len(self._candidates_for_flags)
            candidates_to_keep: int = ceil(float(total_candidates) * self._proportion)
        # Otherwise, all detections must be accounted for, including ones under the threshold
        # Using the detection count this is possible, but it is important to ensure the number of
        # candidates to keep does not exceed the size of the candidate list to avoid runtime errors
        else:
            sites_for_consideration: int = self._detection_count
            sites_to_keep: int = ceil(float(sites_for_consideration * self._proportion))
            candidates_to_keep = min(sites_to_keep, len(self._candidates_for_flags))
        # Trim the list of candidates to the first "candidates_to_keep"
        # elements of the list of candidates. Since the list is sorted by rate,
        # these are the candidates with biggest measured rates.
        self._candidates_for_flags = SortedList(
            self._candidates_for_flags[:candidates_to_keep],
            key=lambda x: -x.rate_at_site,
        )

    def _get_candidates(self) -> SortedList[FollowUpSurveyPlanner]:
        # Returns the candidates list, and resets it, as well as the detection count
        # and the first detection date
        candidates: SortedList[FollowUpSurveyPlanner] = self._candidates_for_flags
        self._candidates_for_flags = SortedList(key=lambda x: -x.rate_at_site)
        self._detection_count = 0
        self._first_candidate_date = None
        return candidates
