import queue

from initialization.sites import Site


DEPLOY_TYPE_ACCESSOR = "deployment_type"
FOLLOWUP_ACCSSOR = "is_follow_up"
INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE = (
    "LDAR-Sim has detected an invalid method deployment type of: {deploy_type} for method: {method}"
)


class GenericSchedule:
    """A generic schedule class that provides a survey queue for a give LDAR method so that
    sites can be queued to be surveyed. Schedule classes specific to method types will inherit
    from this class and overwrite it's default behavior where necessary.
    """

    # TODO what are the different priority cases
    DEFAULT_SURVEY_PRIORITY = 3

    def __init__(self, method_name: str) -> None:
        self._method: str = method_name
        self._survey_queue = queue.PriorityQueue()
        return

    def add_to_survey_queue(self, site: Site) -> None:
        """Add the supplied site to the survey queue to surveyed

        Args:
            site (Site): The site to be added to the survey queue
        """
        self._survey_queue.put((GenericSchedule.DEFAULT_SURVEY_PRIORITY, site))

    def get_daily_sites_to_survey() -> None:
        """This method will go through the method survey queue and return
        the daily sites that are planned to be surveyed by the given method."""
        # TODO Implement
        return


class MobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

    def __init__(self, method_name: str) -> None:
        super().__init__(method_name)
        return


class StationarySchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "stationary" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "stationary"

    def __init__(self, method_name: str) -> None:
        super().__init__(method_name)
        return


class FollowUpMobileSchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "mobile" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "mobile"

    def __init__(self, method_name: str) -> None:
        super().__init__(method_name)
        return


def create_schedule(method_name: str, method_details: dict) -> GenericSchedule:
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
            schedule: GenericSchedule = MobileSchedule(method_name)
        elif method_deployment_type == StationarySchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = StationarySchedule(method_name)
        else:
            print(
                INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE.format(
                    deploy_type=method_deployment_type, method=method_name
                )
            )
            exit()
    else:
        if method_deployment_type == FollowUpMobileSchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = FollowUpMobileSchedule(method_name)
        else:
            print(
                INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE.format(
                    deploy_type=method_deployment_type, method=method_name
                )
            )
            exit()
    return schedule
