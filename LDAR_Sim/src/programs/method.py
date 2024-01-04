"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        Method
Purpose: Module for methods

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

import math
from queue import PriorityQueue

import numpy as np
from virtual_world.sites import Site
from src.scheduling.workplan import Workplan, CrewDailyReport
from src.scheduling.workplan import EmissionDetectionReport, SiteSurveyReport
from src.scheduling.survey_planner import SurveyPlanner


class Method:
    SURVEY_TIME_ACCESSOR = "time"
    TRAVEL_TIME_ACCESSOR = "t_bw_sites"
    DETEC_ACCESSOR = "sensor"
    CREW_COUNT = "n_crews"
    MAX_WORK_HOURS = "max_workday"
    DAYLIGHT = "consider_daylight"
    WEATHER = "weather_envs"
    FOLLOW_UP_ACCESSOR = "is_follow_up"

    POTENTIAL_CREW_SHORTAGE_MESSAGE = (
        "Warning: LDAR-Sim has detected a potential for crew shortage for the method: {method}"
    )

    # TODO ensure survey times aren't needed for methods
    def __init__(self, name: str, properties: dict, consider_weather: bool, sites: "list[Site]"):
        self._name: str = name
        self._initialize_sensor(properties[self.DETEC_ACCESSOR])
        self._method_workplan: Workplan = Workplan([])
        self._max_work_hours: int = properties[self.MAX_WORK_HOURS]
        self._daylight_sensitive = properties[self.DAYLIGHT]
        self._weather: bool = consider_weather
        self._weather_envs: dict = properties[self.WEATHER]
        self._is_follow_up: bool = properties[self.FOLLOW_UP_ACCESSOR]
        self._travel_times = properties[self.TRAVEL_TIME_ACCESSOR]
        crews: int = properties[self.CREW_COUNT]
        self.initialize_crews(crews, sites)

    def initialize_crews(self, crews, sites: "list[Site]") -> None:
        """Initialize the daily crew reports that the method will use
        This will represent the number of crews available for the given method

        """

        self._crews: int = self._estimate_method_crews_required(crews, sites)

        crew_reports: list[CrewDailyReport] = []
        for crew in range(self._crews):
            crew_reports.append(CrewDailyReport(crew, 0))
        self._crew_reports: list[CrewDailyReport] = crew_reports
        return

    def get_average_method_surveys_required(self, sites: "list[Site]") -> float:
        return np.average([site.get_required_surveys(self._name) for site in sites])

    def _get_average_survey_time_for_method(
        method_name: str, avg_travel_time: float, sites: "list[Site]"
    ) -> float:
        """
        Return:
            Average time in minutes
        """
        return np.average(
            [(site.get_method_survey_time(method_name) + avg_travel_time) for site in sites]
        )

    def _estimate_method_crews_required(
        self,
        crews: int,
        sites: "list[Site]",
    ) -> int:
        # TODO: Review the math that was used to update this
        estimate_req_n_crews: int = 0
        if not self._is_follow_up:
            avg_travel_time: float = self._get_avg_t_bt_sites()
            self._avg_s_time: float = self._get_average_survey_time_for_method(
                self._name, avg_travel_time, sites
            )
            self._average_req_surveys: float = self.get_average_method_surveys_required(
                self._name, sites
            )
            # Subtract average travel time here to account the method needing to return
            # at the end of the day
            daily_work_time: float = (self._max_work_hours * 60) - avg_travel_time
            est_avg_sites_p_day: float = daily_work_time / self._avg_s_time
            avg_days_for_surveys: float = 365 / self._average_req_surveys
            estimate_req_n_crews = math.ceil(
                len(sites) / (est_avg_sites_p_day * avg_days_for_surveys)
            )

        else:
            estimate_req_n_crews = 1
        if crews > 0 and estimate_req_n_crews > crews:
            estimate_req_n_crews = crews
            print(self.POTENTIAL_CREW_SHORTAGE_MESSAGE)
        return estimate_req_n_crews

    def _estimate_average_daily_surveys(
        self,
    ) -> int:
        """
        Return:
            Average maximum daily sites a single crew can survey
        """
        HOUR_TO_MIN: int = 60
        daily_work_time: int = self._max_work_hours * HOUR_TO_MIN
        survey_time: float = self._avg_s_time

        return math.ceil(daily_work_time / survey_time)

    def get_crew_count(self) -> int:
        return self._crews

    def deploy_crews(self, curr_date, state):
        """Deploy crews will send crews out to survey sites based on the provided workplan"""

        priority_queue = PriorityQueue()
        day_time_remaining = self._max_work_hours
        # Initialize the daily available survey time for existing crews
        if self._daylight_sensitive:
            day_time_remaining = self.get_daylight_hours(state, self._max_work_hours, curr_date)
        for crew in self._crew_reports:
            # TODO : if method is daylight sensitive, check for max daylight

            priority_queue.put((-crew.day_time_remaining, crew.crew_id, crew))

        # pop the site with the longest remaining hours to assign the next site
        for site_survey in self._method_workplan._site_survey_list:
            # while there are crews that can work
            if not priority_queue.empty():
                _, _, assigned_crew = priority_queue.get()
                self.survey_site(assigned_crew, site_survey, state, curr_date)
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

    def survey_site(
        self,
        daily_report: CrewDailyReport,
        site: SurveyPlanner,
        survey_report: SiteSurveyReport,
        state,
        curr_date,
    ):
        """The method will attempt to survey the site provided as an argument, detecting emissions
        at it's detection level, either tagging sites for follow-up or flagging leaks,
        and generating an emissions report

        Will also update the CrewDailyReport

        TODO: defaulting this to site level survey
        TODO: need to figure out how to get time between sites
        TODO: if weather does not permit, need to return the survey plan to say it wasn't surveyed.
        Args:
            daily_report (CrewDailyReport): the associated crew's daily report
            (of available work hours)
            site (Site): The site to survey
            state : Dictionary containing information about weather and
        """

        if self._weather:
            # if weather is considered
            workable = self.check_weather(state, curr_date, site.site)
            if workable:
                # TODO: survey site
                survey_time = site.site.get_method_survey_time(self._name)
                # Can finish the whole site
                if daily_report.day_time_remaining - survey_time >= 0:
                    daily_report.day_time_remaining -= survey_time
                    survey_report.survey_complete = True
                    survey_report.survey_in_progress = False
                    survey_report.time_surveyed = survey_time
                # Cannot finish the whole site
                else:
                    survey_report.survey_in_progress = True
                    survey_report.time_surveyed += daily_report.day_time_remaining
                    daily_report.day_time_remaining = 0

            # else:
            # Return the survey report unchanged because no survey was done
        else:
            # TODO: copy same logic from above.
            survey_time = site.site.get_method_survey_time(self._name)
            # Can finish the whole site
            if daily_report.day_time_remaining - survey_time >= 0:
                daily_report.day_time_remaining -= survey_time
                survey_report.survey_complete = True
                survey_report.survey_in_progress = False
                survey_report.time_surveyed = survey_time
            # Cannot finish the whole site
            else:
                survey_report.survey_in_progress = True
                survey_report.time_surveyed += daily_report.day_time_remaining
                daily_report.day_time_remaining = 0
        return survey_report, daily_report

    def _change_workplan(self, survey_list: "list[Site]") -> None:
        self._method_workplan._site_survey_list = survey_list
        return

    def return_workplan(self) -> Workplan:
        return self._method_workplan

    def gen_emissions_report(site: Site, curr_date):
        """Will generate an emissions report of detections at the site.
        If no emissions are detected,will generate a report indicating that was the case.

        Args:
            site (Site): The site for which to generate the emissions report.
        """
        # TODO : estimate start date based on survey plan

        report = EmissionDetectionReport(
            site=site,
            current_date=curr_date,
        )
        return report

    def _initialize_sensor(sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): _description_
        """
        return {}

    def get_daylight_hours(state, max_hours: int, curr_date) -> int:
        """Get the amount of daylight hours"""
        daylight_hours = state["daylight"].get_daylight(curr_date)
        work_hours = daylight_hours
        if max_hours < daylight_hours:
            work_hours = max_hours
        return work_hours

    def check_weather(self, state, curr_date, site: Site) -> bool:
        """
        Check the weather conditions for the given site on the given day

        # TODO : change this such that the matrix is set once for given method
        """
        TEMP = "temp"
        WIND = "wind"
        PREICIP = "precip"

        # TODO change to getters
        lat = site._lat
        long = site._long
        bool_temp: bool = False
        bool_wind: bool = False
        bool_precip: bool = False

        if (
            self._weather_envs[TEMP][0]
            <= state["weather"].temps[curr_date, lat, long]
            <= self._weather_envs[TEMP][1]
        ):
            bool_temp = True
        if (
            self._weather_envs[WIND][0]
            <= state["weather"].winds[curr_date, lat, long]
            <= self._weather_envs[WIND][1]
        ):
            bool_wind = True
        if (
            self._weather_envs[PREICIP][0]
            <= state["weather"].precip[curr_date, lat, long]
            <= self._weather_envs[PREICIP][1]
        ):
            bool_precip = True

        # if weather permits
        if bool_precip and bool_wind and bool_temp:
            return True
        # if weather conditions are not good
        else:
            return False
