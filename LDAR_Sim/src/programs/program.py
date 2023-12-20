from datetime import date, timedelta
from virtual_world.sites import Site
from programs.method import Method
from scheduling.survey_planner import SurveyPlanner
from scheduling.schedules import GenericSchedule, create_schedule
from scheduling.workplan import Workplan


class Program:
    """An object responsible for scheduling surveys for all sites in the infrastructure.
    Uses other lower level objects to plan and schedule survey times and determine actual
    dynamic schedules based on weather and other impacting variables."""

    def __init__(self, methods: dict, sites: list[Site],
        sim_start_date: date, sim_end_date: date) -> None:
        self._methods: list[Method] = [
            Method(method, properties) for method, properties in methods.items()
        ]
        self._survey_schedules: dict[str, GenericSchedule] = {}
        self._current_date : date = sim_start_date
        self.init_method_scheduling(methods=methods, sites=sites)


    def do_daily_method_deployment(self) -> None:
        """Deploy all methods that are part of the program to
        do their scheduled surveys for the day"""
        for method in self._methods:
            method.deploy_crews

        self.update_scheduling()

        return

    def update_scheduling(self) -> None:
        """Update the state of all survey plans and queue sites to the surveyed as
        required by survey planner determinations"""
        self.update_date()
        for survey_schedule in self._survey_schedules:
            daily_sites : list[Workplan] = survey_schedule.update_schedule(self._current_date)
            # TODO: update the workplan object with the new daily site list
        self.update_schedule_based_on_workplan_results()


    # # TODO define a method workplan object that they can use to track progress on
    # # surveying sites for a day
    # def get_method_workplan(self, method : str) -> Workplan:
    #     """Determine daily workplans for the given method for the day.
    #     The workplans will help methods track with sites to survey and report progress.

    #     Returns:
    #         Workplan: An object containing the list of sites to attempt to survey for the day
    #         that can be updated to report survey progress and discovered leaks.
    #     """
    #     for meth in self._methods:
    #         if meth._name == method:
    #             return meth.return_workplan()

    #     return 

    def update_date(self) -> None:
        """Increment the current date counter
        """
        self._current_date += timedelta(days=1)

    def update_schedule_based_on_workplan_results(self):
        """
        Call updates on the schedules for the next day based on the
        workplan returned by the method after a days work
        """
        for method in self._methods:
            workplan = method.return_workplan()
            for site in workplan._site_survey_reports:
                if site.survey_in_progress:
                    #TODO : add in progress survey with high prio to relevant method schedule
                elif not site.survey_complete:
                    # TODO: add just queued survey back to schdule with med prio
                    
                else:
                    # TODO: adjust the site such that it's no longer flagged as queued
                    #self._survey_schedules[method._name].
                    # survey_planner.unflag_for_queue()


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