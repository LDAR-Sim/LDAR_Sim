from queue import Queue
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
        self._crew_reports: list[CrewDailyReport] = self.initialize_daily_crews(
            properties[Method.CREW_COUNT]
        )
        self.max_work_hours = properties[Method.MAX_WORK_HOURS]

    def initialize_daily_crews(self, n_crew) -> None:
        """Initialize the daily crew reports that the method will use
        This will represent the number of crews available
        """
        if n_crew == -1:
            # TODO: figure out how to get estimate n_crew here if n_crew is not set
            crew_reports.append
        else:
            crew_reports: list[CrewDailyReport] = []
            for crew in range(n_crew):
                crew_reports.append(CrewDailyReport(crew, 0))
        self._crew_reports = crew_reports
        return

    def deploy_crews(self):
        """Deploy crews will send crews out to survey sites based on the provided workplan

        Assumes that the weather will be"""
        # TODO: need to know how many crews are available for the method,
        # if n_crews = -1 then use estimate crews unless followup
        for crew in self._crew_reports:
            crew.day_time_remaining = self.max_work_hours
            # TODO : check for daily weather
            # TODO : if method is daylight sensitive, check for max daylight
            # TODO: create temporary queues for each of the "crews"
            # assign the given site to the queue of a single crew

        daily_queue: dict[int, Queue] = {}
        # Assign the sites evenly to each crew
        for i, site_survey in enumerate(self._method_workplan._site_survey_list):
            assigned_crew = i % len(self._crew_reports)
            daily_queue[assigned_crew] = Queue()
            daily_queue[assigned_crew].put(site_survey)

        for crew_id, crew_queue in daily_queue.items:
            while self._crew_reports[crew_id].day_time_remaining > 0:
                # survey as many sites as day time remaining
                self.survey_site()
                # TODO: need ot make sure if survey time remaining of the last site here gets an updated workplan
            if not crew_queue.empty():
                # if the daily queue still has sites need to return updated workplan back to programs
                # to indicate that these particular sites need to be requeued with higher priority
                self._method_workplan  # TODO: update this
        return

    def survey_site(self, daily_report: CrewDailyReport, site: Site):
        """The method will attempt to survey the site provided as an argument, detecting emissions
        at it's detection level, either tagging sites for follow-up or flagging leaks,
        and generating an emissions report

        Will also update the CrewDailyReport
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
