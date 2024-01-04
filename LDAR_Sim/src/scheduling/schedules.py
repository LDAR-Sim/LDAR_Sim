from datetime import date
from virtual_world.sites import Site
from scheduling.survey_planner import SurveyPlanner
from utils.queue import PriorityQueueWithFIFO

DEPLOY_TYPE_ACCESSOR = "deployment_type"
FOLLOWUP_ACCSSOR = "is_follow_up"
INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE = "Error: LDAR-Sim has detected an invalid method deployment type of: {deploy_type} for method: {method}"


class GenericSchedule:
    """A generic schedule class that provides a survey queue for a give LDAR method so that
    sites can be queued to be surveyed. Schedule classes specific to method types will inherit
    from this class and overwrite it's default behavior where necessary.
    """

    # Default = 3 - where everything initially starts out
    # 2 - Sites which have been popped for the day but were not attended to
    # 1 - Sites that have surveys which have been started but not finished.
    DEFAULT_SURVEY_PRIORITY = 3
    QUEUED_SURVEY_PRIORITY = 2
    UNFINISHED_SURVEY_HIGHEST_PRIORITY = 1

    def __init__(
        self,
        method_name: str,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        est_meth_daily_surveys: int,
        method_avail_crews: int,
    ) -> None:
        self._method: str = method_name
        self._survey_queue = PriorityQueueWithFIFO()
        self._est_meth_daily_surveys: int = est_meth_daily_surveys
        self._method_crews: int = method_avail_crews
        self._survey_plans: list[SurveyPlanner] = self._set_survey_plans(
            sim_start_date, sim_end_date, sites
        )

        return

    def _set_survey_plans(self, sim_start_date, sim_end_date, sites):
        survey_plans: list[SurveyPlanner] = []
        for site in sites:
            # TODO flush out what survey planner needs as inputs for the constructor
            survey_freq: int = site._survey_frequencies[self._method]
            deploy_year: int = site._deployment_years[self._method]
            deploy_month: int = site._deployment_months[self._method]
            survey_plans.append(
                SurveyPlanner(
                    site, survey_freq, sim_start_date, sim_end_date, deploy_year, deploy_month
                )
            )
        return survey_plans

    def add_to_survey_queue(self, survey_plan: SurveyPlanner) -> None:
        """Add the supplied site to the survey queue to surveyed

        Args:
            site (Site): The site to be added to the survey queue
        """
        self._survey_queue.put(GenericSchedule.DEFAULT_SURVEY_PRIORITY, survey_plan)

    def add_unfinished_to_survey_queue(self, survey_plan: SurveyPlanner) -> None:
        """Add the supplied, partial surveyed site to queue

        Args:
            site (Site) : the Site to be added to the survey queue"""
        self._survey_queue.put(GenericSchedule.UNFINISHED_SURVEY_HIGHEST_PRIORITY, survey_plan)

    def add_previous_queued_to_survey_queue(self, survey_plan: SurveyPlanner) -> None:
        """Add the supplied, unattended site back to queue

        Args:
            site (Site) : the Site to be added to the survey queue"""
        self._survey_queue.put(GenericSchedule.QUEUED_SURVEY_PRIORITY, survey_plan)

    def get_daily_sites_to_survey(self) -> "list[SurveyPlanner]":
        """This method will go through the method survey queue and return
        the daily sites that are planned to be surveyed by the given method

        Returns the list of highest priority survey plans, based on the number of crews available
        and the number of sites the average crew can do in a day
        """
        daily_plan: list[SurveyPlanner] = []

        for crew in range(self._method_crews):
            site_count: int = 0
            for site_count in range(self._est_meth_daily_surveys):
                if not self._survey_queue.empty():
                    prio, _, survey_plan = self._survey_queue.get()
                    daily_plan.append(survey_plan)
                else:
                    break

        return daily_plan

    def update_schedule(self, current_date) -> "list[Site]":
        """
        Updates the survey plans,
        Adds necessary sites to the queue
        Returns:
            The list sites that the method should do on the given day
        """
        for survey_plan in self._survey_plans:
            survey_plan.update_date(current_date)
            if survey_plan.queue_site_for_survey():
                self.add_to_survey_queue(survey_plan)
        return self.get_daily_sites_to_survey()


class MobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

    def __init__(self, method_name: str, sites: "list[Site]") -> None:
        super().__init__(method_name, sites)
        return


class StationarySchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "stationary" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "stationary"

    def __init__(self, method_name: str, sites: "list[Site]") -> None:
        super().__init__(method_name, sites)
        return


class FollowUpMobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

    def __init__(self, method_name: str, sites: "list[Site]") -> None:
        super().__init__(method_name, sites)
        return


def create_schedule(method_name: str, method_details: dict, sites) -> GenericSchedule:
    """Will create and return  schedule with the schedule type based on
    the provided method and it's parameters. All schedules inherit from generic schedule
    class and will overwrite it's method with method type specific behavior where required.

    Args:
        method_name (str): The method name that the schedule is being created for.
        method_details (dict): The method parameters, will be used to determine the
        correct schedule type to create.

    Returns:
        GenericSchedule: A schedule object with the correct schedule type for
        the given method deployment type. Should be treated as a generic schedule and will
        enforce the correct behavior through polymorphism.
    """
    method_follow_up: bool = method_details[FOLLOWUP_ACCSSOR]
    method_deployment_type: str = method_details[DEPLOY_TYPE_ACCESSOR]
    if not method_follow_up:
        if method_deployment_type == MobileSchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = MobileSchedule(method_name, sites)
        elif method_deployment_type == StationarySchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = StationarySchedule(method_name, sites)
        else:
            print(
                INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE.format(
                    deploy_type=method_deployment_type, method=method_name
                )
            )
            exit()
    else:
        if method_deployment_type == FollowUpMobileSchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = FollowUpMobileSchedule(method_name, sites)
        else:
            print(
                INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE.format(
                    deploy_type=method_deployment_type, method=method_name
                )
            )
            exit()
    return schedule
