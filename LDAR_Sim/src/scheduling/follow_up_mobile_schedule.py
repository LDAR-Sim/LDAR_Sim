from datetime import date
from scheduling.follow_up_survey_planner import FollowUpSurveyPlanner
from scheduling.generic_schedule import GenericSchedule
from utils.queue import PriorityQueueWithFIFO
from virtual_world.sites import Site


class FollowUpMobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

    def __init__(
        self,
        method_name: str,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        est_meth_daily_surveys: int,
        method_avail_crews: int,
    ) -> None:
        super().__init__(
            method_name,
            sites,
            sim_start_date,
            sim_end_date,
            est_meth_daily_surveys,
            method_avail_crews,
        )
        self._site_IDs_in_queue: dict[str, bool] = {site.get_id(): False for site in sites}
        return

    def get_site_id_queue_list(self) -> dict[str, bool]:
        return self._site_IDs_in_queue

    def get_plan_from_queue(self, site_id: str) -> FollowUpSurveyPlanner:
        new_queue: PriorityQueueWithFIFO = PriorityQueueWithFIFO()
        target_plan: FollowUpSurveyPlanner = None
        while not self._survey_queue.empty():
            prio, _, plan = self._survey_queue.get()
            prio: int
            plan: FollowUpSurveyPlanner
            if plan.site_id == site_id:
                target_plan = plan
            else:
                new_queue.put(prio, plan)
        self._survey_queue: PriorityQueueWithFIFO = new_queue
        return target_plan
