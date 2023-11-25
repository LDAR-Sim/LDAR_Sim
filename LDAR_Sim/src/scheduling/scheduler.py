from initialization.sites import Site
from scheduling.schedules import GenericSchedule, create_schedule
from scheduling.survey_planner import SurveyPlanner


class Scheduler:
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
        for method in self._methods:
            for survey_planner in self._survey_planners[method]:
                survey_planner.update()
                if survey_planner.queue_site_for_survey():
                    self._survey_schedules[method].add_to_survey_queue(survey_planner.get_site())
