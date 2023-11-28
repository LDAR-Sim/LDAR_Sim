from initialization.sites import Site
from scheduling.schedules import GenericSchedule, create_schedule
from scheduling.survey_planner import SurveyPlanner


class Scheduler:
    """An object responsible for scheduling surveys for all sites in the infrastructure.
    Uses other lower level objects to plan and schedule survey times and determine actual
    dynamic schedules based on weather and other impacting variables."""

    def __init__(self, methods: dict, sites: list[Site]) -> None:
        self._methods: list[str] = [method for method in methods]
        self._survey_schedules: dict[str, GenericSchedule] = {}
        for method, method_params in methods.items():
            self._survey_schedules[method] = create_schedule(
                method_name=method, method_details=method_params
            )
        self._survey_planners: dict[str, list[SurveyPlanner]] = {}
        for method in methods:
            method_survey_plans: list[SurveyPlanner] = []
            for site in sites:
                # TODO flush out what survey planner needs as inputs for the constructor
                method_survey_plans.append(SurveyPlanner(site))
            self._survey_planners[method] = method_survey_plans

    def update_scheduling(self) -> None:
        """Update the state of all survey plans and queue sites to the surveyed as
        required by survey planner determinations"""
        for method in self._methods:
            for survey_planner in self._survey_planners[method]:
                survey_planner.update()
                if survey_planner.queue_site_for_survey():
                    self._survey_schedules[method].add_to_survey_queue(survey_planner.get_site())

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

    def init_method_scheduling(self, methods: dict) -> None:
        """Initialize method scheduling for all methods to be simulated.
        This will setup logic to schedule methods to go survey sites based
        on their number of available crews, time to sites, time to survey, etc.

        Args:
            methods (dict): A dictionary of all the methods to initialize for survey scheduling.
        """
        return
