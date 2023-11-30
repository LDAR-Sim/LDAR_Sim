from initialization.sites import Site
from programs.method import Method
from scheduling.schedules import GenericSchedule, create_schedule
from scheduling.workplan import Workplan


class Program:
    """An object responsible for scheduling surveys for all sites in the infrastructure.
    Uses other lower level objects to plan and schedule survey times and determine actual
    dynamic schedules based on weather and other impacting variables."""

    def __init__(self, methods: dict, sites: list[Site]) -> None:
        self._methods: list[Method] = [
            Method(method, properties) for method, properties in methods.items()
        ]
        self._survey_schedules: dict[str, GenericSchedule] = {}
        self.init_method_scheduling(methods=methods, sites=sites)

    def update_scheduling(self) -> None:
        """Update the state of all survey plans and queue sites to the surveyed as
        required by survey planner determinations"""
        for survey_schedule in self._survey_schedules:
            survey_schedule.update_schedule()

    # TODO define a method workplan object that they can use to track progress on
    # surveying sites for a day
    def get_method_workplan(self, method: str) -> Workplan:
        """Determine daily workplans for the given method for the day.
        The workplans will help methods track with sites to survey and report progress.

        Returns:
            Workplan: An object containing the list of sites to attempt to survey for the day
            that can be updated to report survey progress and discovered leaks.
        """
        return

    def init_method_scheduling(self, methods: dict, sites: list[Site]) -> None:
        """Initialize method scheduling for all methods to be simulated.
        This will setup logic to schedule methods to go survey sites based
        on their number of available crews, time to sites, time to survey, etc.

        Args:
            methods (dict): A dictionary of all the methods to initialize for survey scheduling.
        """
        for method, method_params in methods.items():
            self._survey_schedules[method] = create_schedule(
                method_name=method, method_details=method_params, sites=sites
            )

    def do_daily_method_deployment(self) -> None:
        """Deploy all methods that are part of the program to
        do their scheduled surveys for the day"""
        return
