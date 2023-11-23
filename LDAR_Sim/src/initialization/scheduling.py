import queue

from initialization.sites import Site


DEPLOY_TYPE_ACCESSOR = "deployment_type"
INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE = (
    "LDAR-Sim has detected an invalid method deployment type of: {deploy_type} for method: {method}"
)


class GenericSchedule:
    DEFAULT_SURVEY_PRIORITY = 3

    def __init__(self, method_name: str) -> None:
        self._method: str = method_name
        self._survey_queue = queue.PriorityQueue()
        return

    def add_to_survey_queue(self, site: Site) -> None:
        self._survey_queue.put((GenericSchedule.DEFAULT_SURVEY_PRIORITY, site))


class MobileSchedule(GenericSchedule):
    DEPLOY_TYPE_CODE = "mobile"

    def __init__(self, method_name: str) -> None:
        super.__init__(method_name)
        return


class StationarySchedule(GenericSchedule):
    DEPLOY_TYPE_CODE = "stationary"

    def __init__(self, method_name: str) -> None:
        super.__init__(method_name)
        return


def create_schedule(method_name: str, method_details: dict) -> GenericSchedule:
    method_deployment_type: str = method_details[DEPLOY_TYPE_ACCESSOR]
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
    return schedule
