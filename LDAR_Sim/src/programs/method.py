from queue import PriorityQueue
from virtual_world.sites import Site
from src.scheduling.workplan import Workplan, CrewDailyReport
from src.scheduling.workplan import EmissionDetectionReport, SiteSurveyReport


class Method:
    SURVEY_TIME_ACCESSOR = "time"
    TRAVEL_TIME_ACCESSOR = "t_bw_sites"
    DETEC_ACCESSOR = "sensor"
    CREW_COUNT = "n_crews"
    MAX_WORK_HOURS = "max_workday"

    # TODO ensure survey times aren't needed for methods
    def __init__(self, name: str, properties: dict):
        self._name: str = name
        self._initialize_sensor(properties[Method.DETEC_ACCESSOR])
        self._method_workplan: Workplan = Workplan([])
        self._crew_reports: list[CrewDailyReport] = self.initialize_crews(
            properties[Method.CREW_COUNT]
        )
        self.max_work_hours = properties[Method.MAX_WORK_HOURS]

    def initialize_crews(self, n_crew) -> None:
        """Initialize the daily crew reports that the method will use
        This will represent the number of crews available for the given method

        """
        crew_reports: list[CrewDailyReport] = []
        for crew in range(n_crew):
            crew_reports.append(CrewDailyReport(crew, 0))
        self._crew_reports = crew_reports
        return

    def deploy_crews(self):
        """Deploy crews will send crews out to survey sites based on the provided workplan"""

        priority_queue = PriorityQueue()
        # Initialize the daily available survey time for existing crews
        for crew in self._crew_reports:
            # TODO : if method is daylight sensitive, check for max daylight
            priority_queue.put((-crew.day_time_remaining, crew.crew_id, crew))

        # pop the site with the longest remaining hours to assign the next site
        for site_survey in self._method_workplan._site_survey_list:
            # while there are crews that can work
            if not priority_queue.empty():
                _, _, assigned_crew = priority_queue.get()
                self.survey_site(assigned_crew, site_survey)
                if assigned_crew.day_time_remaining > 0:
                    # Put the crew back into the queue if there's remaining work hours
                    priority_queue.put(
                        (-assigned_crew.day_time_remaining, assigned_crew.crew_id, assigned_crew)
                    )
            # if there are no crews available for work
            else:
                # Update the site_survey
                # to indicate that these particular sites need to be requeued with higher priority
                site_survey.update
        return

    def survey_site(self, daily_report: CrewDailyReport, site: SurveyPlanner):
        """The method will attempt to survey the site provided as an argument, detecting emissions
        at it's detection level, either tagging sites for follow-up or flagging leaks,
        and generating an emissions report

        Will also update the CrewDailyReport
        TODO: need to check for weather if crew can survey this site.
        TODO: if weather does not permit, need to return the survey plan to say it wasn't surveyed.
        Args:
            daily_report (CrewDailyReport): the associated crew's daily report (of available work hours)
            site (Site): The site to survey
        """

        return

    def _change_workplan(self, survey_list: list[Site]) -> None:
        self._method_workplan._site_survey_list = survey_list
        return

    def return_workplan(self) -> Workplan:
        return self._method_workplan

    def gen_emissions_report(site: Site):
        """Will generate an emissions report of detections at the site.
        If no emissions are detected,will generate a report indicating that was the case.

        Args:
            site (Site): The site for which to generate the emissions report.
        """

        return

    def _initialize_sensor(sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): _description_
        """
        return
