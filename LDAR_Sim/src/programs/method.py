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

from datetime import date
import math
from queue import PriorityQueue
from random import choice
import sys
from typing import Tuple

import numpy as np
from constants.error_messages import ERR_MSG_UNKNOWN_SENS_TYPE
from file_processing.output_processing.output_utils import CrewDeploymentStats, TaggingFlaggingStats
from sensors.default_site_level_sensor import DefaultSiteLevelSensor
from virtual_world.sites import Site
from scheduling.workplan import Workplan
from scheduling.schedule_dataclasses import (
    EmissionDetectionReport,
    SiteSurveyReport,
    CrewDailyReport,
)
from scheduling.surveying_dataclasses import DetectionRecord
from constants.param_default_const import Method_Params as mp

WEATHER_ERROR = "Error: Unrecognized weather type"


class Method:
    TEMP = "temp"
    WIND = "wind"
    PRECIP = "precip"
    # Used to return the weather value
    HOUR = 8

    SURVEY_TIME_ACCESSOR = "time"
    TRAVEL_TIME_ACCESSOR = "t_bw_sites"
    DETEC_ACCESSOR = "sensor"
    CREW_COUNT = "n_crews"
    MAX_WORK_HOURS = "max_workday"
    DAYLIGHT = "consider_daylight"
    WEATHER = "weather_envs"
    FOLLOW_UP_ACCESSOR = "is_follow_up"
    MEASUREMENT_SCALE_ACCESSOR = "measurement_scale"
    REPORTING_DELAY_ACCESSOR = "reporting_delay"
    METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR = "follow_up"
    METHOD_FOLLOW_UP_PROPERTIES_PREF_FU_ACCESSOR = "preferred_method"
    METHOD_FOLLOW_UP_PROPERTIES_INTERACT_PRIO_ACCESSOR = "interaction_priority"
    METHOD_FOLLOW_UP_PROPERTIES_INST_THRESH_ACCESSOR = "instant_threshold"
    METHOD_FOLLOW_UP_PROPERTIES_PROP_ACCESSOR = "proportion"
    METHOD_FOLLOW_UP_PROPERTIES_THRESH_ACCESSOR = "threshold"
    METHOD_FOLLOW_UP_PROPERTIES_DELAY_ACCESSOR = "delay"
    METHOD_FOLLOW_UP_PROPERTIES_REDUND_FILTER_ACCESSOR = "redundancy_filter"

    METHOD_COST_ACESSOR = "cost"
    METHOD_COST_PER_DAY = "per_day"
    METHOD_COST_PER_SITE = "per_site"
    METHOD_COST_UPFRONT = "upfront"

    PER_SITE_COST = "site"
    PER_DAY_COST = "day"

    POTENTIAL_CREW_SHORTAGE_MESSAGE = (
        "Warning: LDAR-Sim has detected a potential for crew shortage for the method: {method}"
    )

    # TODO ensure survey times aren't needed for methods
    def __init__(
        self,
        name: str,
        properties: dict,
        consider_weather: bool,
        sites: "list[Site]",
    ) -> None:
        self._name: str = name
        self._initialize_sensor(properties[self.DETEC_ACCESSOR])
        self._max_work_hours: int = properties[self.MAX_WORK_HOURS]
        self._daylight_sensitive = properties[self.DAYLIGHT]
        self._weather: bool = consider_weather
        self._weather_envs: dict = properties[self.WEATHER]
        self._is_follow_up: bool = properties[self.FOLLOW_UP_ACCESSOR]
        self._travel_times = properties[self.TRAVEL_TIME_ACCESSOR][
            "vals"
        ]  # TODO: update this to not use just vals
        self._reporting_delay: int = properties[self.REPORTING_DELAY_ACCESSOR]
        crews: int = properties[self.CREW_COUNT]
        # TODO Check where these should be saved
        self._site_survey_reports: list[SiteSurveyReport] = []
        self._detection_records: dict[date, list[DetectionRecord]] = {}
        self.initialize_crews(crews, sites)
        self.initialize_cost_tracking(properties[self.METHOD_COST_ACESSOR])

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

    def initialize_cost_tracking(self, cost_properties: dict[str, float]):
        self.upfront_cost = cost_properties[self.METHOD_COST_UPFRONT]
        if cost_properties[self.METHOD_COST_PER_SITE] > 0:
            self.cost_type = self.PER_SITE_COST
            self.cost = cost_properties[self.METHOD_COST_PER_SITE]
        elif cost_properties[self.METHOD_COST_PER_DAY] > 0:
            self.cost_type = self.PER_DAY_COST
            self.cost = cost_properties[self.METHOD_COST_PER_DAY]
        else:
            self.cost_type = self.PER_SITE_COST
            self.cost = -1

    def _initialize_sensor(self, sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): _description_
        """
        if sensor_info[mp.TYPE] == "default":
            self._sensor = DefaultSiteLevelSensor(sensor_info[mp.MDL], sensor_info[mp.QE])
        else:
            print(ERR_MSG_UNKNOWN_SENS_TYPE.format(method=self._name))
            sys.exit()

    def _get_average_method_surveys_required(self, sites: "list[Site]") -> float:
        return np.average([site.get_required_surveys(self._name) for site in sites])

    def _get_average_survey_time_for_method(
        self, method_name: str, avg_travel_time: float, sites: "list[Site]"
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
        # TODO don't use if follow-up and instead move this into the child classes to handle it
        # TODO handle default
        estimate_req_n_crews: int = 0
        avg_travel_time: float = self._get_avg_t_bt_sites()
        self._avg_s_time: float = self._get_average_survey_time_for_method(
            self._name, avg_travel_time, sites
        )
        if not self._is_follow_up:
            self._average_req_surveys: float = self._get_average_method_surveys_required(sites)
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

    def _get_avg_t_bt_sites(self) -> float:
        return np.average(self._travel_times)

    def estimate_average_daily_surveys(
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

    def deploy_crews(self, workplan: Workplan, weather, daylight) -> CrewDeploymentStats:
        """Deploy crews will send crews out to survey sites based on the provided workplan"""
        deploy_stats: CrewDeploymentStats = CrewDeploymentStats()

        priority_queue = PriorityQueue()
        day_time_remaining = self._max_work_hours
        # Initialize the daily available survey time for existing crews
        if self._daylight_sensitive:
            day_time_remaining = self.get_daylight_hours(
                daylight, self._max_work_hours, workplan.date
            )
        day_time_remaining = day_time_remaining * 60  # Convert time from hours to minutes
        # TODO Add logic to not deploy all crews if not necessary?
        for crew in self._crew_reports:
            # TODO : if method is daylight sensitive, check for max daylight
            crew.day_time_remaining = day_time_remaining
            priority_queue.put((-crew.day_time_remaining, crew.crew_id, crew))

        # If the cost type for the method is per day, calculate the deployment cost for day
        # based off the number of crews being deployed
        if self.cost_type == self.METHOD_COST_PER_DAY:
            deploy_stats.deployment_cost = self.cost * len(self._crew_reports)
        # pop the site with the longest remaining hours to assign the next crew
        # while there are crews that can work
        for survey_plan in workplan.site_survey_planners.values():
            # Get the survey report
            survey_report: SiteSurveyReport = survey_plan.get_current_survey_report()
            site_to_survey: Site = survey_plan.get_site()
            if not priority_queue.empty():
                # Get the crew with the most time remaining to work
                _, _, assigned_crew = priority_queue.get()
                assigned_crew: CrewDailyReport

                # Send the crew to attempt to survey the site
                survey_report, travel_time, last_site_survey = self.survey_site(
                    crew=assigned_crew,
                    survey_report=survey_report,
                    site_to_survey=site_to_survey,
                    weather=weather,
                    curr_date=workplan.date,
                )
                survey_report: SiteSurveyReport
                travel_time: float
                last_site_survey: bool
                # Tracking Deployment statistics
                deploy_stats.sites_visited += 1
                deploy_stats.travel_time += travel_time
                deploy_stats.survey_time += survey_report.time_surveyed

                # If this will be last survey of the day, set remaining time
                # to 0 and track travel home time
                if last_site_survey:
                    crew.day_time_remaining = 0
                    workplan.total_travel_time += travel_time
                    deploy_stats.travel_time += travel_time
                    # TODO Make sure this gets update for other travel times as well
                # If the crew still has time left, requeue it to go survey another site
                if assigned_crew.day_time_remaining > 0:
                    # Put the crew back into the queue if there's remaining work hours
                    priority_queue.put(
                        (
                            -assigned_crew.day_time_remaining,
                            assigned_crew.crew_id,
                            assigned_crew,
                        )
                    )
            # Update the survey planner. If the survey was not finished, the update will
            # indicate that the particular site needs to be requeued with higher priority
            workplan.add_survey_report(survey_report, survey_plan)
            if survey_report.survey_complete:
                self._site_survey_reports.append(survey_report)
                detection_record: DetectionRecord = DetectionRecord(
                    site_id=survey_report.site_id,
                    site=survey_plan.get_site(),
                    rate_detected=survey_report.site_measured_rate,
                )
                current_records: list[DetectionRecord] = self._detection_records.get(
                    workplan.date, []
                )
                current_records.append(detection_record)
                self._detection_records[workplan.date] = current_records

                if self.cost_type == self.PER_SITE_COST:
                    site_survey_cost = site_to_survey.get_survey_cost(self._name)
                    if site_survey_cost == 0 and self.cost > 0:
                        site_survey_cost = self.cost
                    deploy_stats.deployment_cost += site_survey_cost
        return deploy_stats

    def update(self, current_date: date) -> TaggingFlaggingStats:
        return None

    def survey_site(
        self,
        crew: CrewDailyReport,
        survey_report: SiteSurveyReport,
        site_to_survey: Site,
        weather,
        curr_date: date,
    ) -> Tuple[SiteSurveyReport, float]:
        """The method will attempt to survey the site provided as an argument, detecting emissions
        at it's detection level, either tagging sites for follow-up or flagging leaks,
        and generating an emissions report

        Will also update the CrewDailyReport

        TODO: defaulting this to site level survey
        Args:
            daily_report (CrewDailyReport): the associated crew's daily report
            (of available work hours)
            site (Site): The site to survey
            weather : Dictionary containing information about weather
        """
        workable: bool = True
        last_site_survey: bool = False
        site_travel_time: float = 0
        if self._weather:
            # if weather is considered
            workable: bool = self.check_weather(weather, curr_date, site_to_survey)

        if workable:
            site_survey_time: float = site_to_survey.get_method_survey_time(self._name)
            site_travel_time: float = self._get_travel_time()

            # Check if the site survey can be completed
            can_complete_survey: bool = self._determine_if_site_survey_can_be_completed(
                survey_report=survey_report,
                site_survey_time=site_survey_time,
                site_travel_time=site_travel_time,
                crew_time_remaining=crew.day_time_remaining,
            )

            # Can finish the whole site
            if can_complete_survey:
                # Set the start and completion data and detect emissions at the site
                if not survey_report.survey_in_progress:
                    survey_report.survey_start_date = curr_date
                    survey_report.method = self._name
                survey_report.survey_completion_date = curr_date
                # Mark the survey as complete and no longer in progress
                survey_report.survey_complete = True
                survey_report.survey_in_progress = False
                # Account for travel time in time calculations
                survey_report.time_spent_to_travel += site_travel_time
                crew.day_time_remaining -= site_travel_time
                # Account for survey time in time calculations,
                # and consider that some of the site may have previously been surveyed
                survey_report.time_surveyed = site_survey_time
                crew.day_time_remaining -= site_survey_time - survey_report.time_surveyed
                if crew.day_time_remaining <= site_travel_time:
                    last_site_survey = True
                self._sensor.detect_emissions(
                    site=site_to_survey,
                    meth_name=self._name,
                    survey_report=survey_report,
                )
            # Cannot finish the whole site but can survey
            # TODO determine reasonable fraction of site that can be surveyed to make it worth going
            elif crew.day_time_remaining > (2 * site_travel_time):
                # Mark the survey as in progress
                survey_report.survey_in_progress = True
                last_site_survey = True
                # Log Survey and travel time
                survey_report.time_spent_to_travel += site_travel_time
                survey_report.time_surveyed += crew.day_time_remaining - (site_travel_time * 2)
                crew.day_time_remaining = site_travel_time
                # Log survey start date
                survey_report.survey_start_date = curr_date
            # Not enough time left to travel to site
            else:
                site_travel_time = 0
                last_site_survey = True

        return survey_report, site_travel_time, last_site_survey

    def _determine_if_site_survey_can_be_completed(
        self,
        survey_report: SiteSurveyReport,
        site_survey_time: float,
        site_travel_time: float,
        crew_time_remaining: float,
    ) -> bool:
        # Account for the possibility of the crew needing to return when considering if the
        # Site can be surveyed in a day.
        # TODO review travel home time logic
        survey_required_time: float = site_survey_time + (site_travel_time * 2)
        actual_required_time: float = survey_required_time - survey_report.time_surveyed
        survey_can_be_completed: bool = crew_time_remaining >= actual_required_time

        return survey_can_be_completed

    def _get_travel_time(self) -> float:
        if isinstance(self._travel_times, (int, float)):
            return self._travel_times
        elif isinstance(self._travel_times, list):
            return choice(self._travel_times)
        else:
            print(f"Error: Unrecognized travel time format for method {self._name}")
            sys.exit()

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

    def get_daylight_hours(self, daylight, max_hours: int, curr_date) -> int:
        """Get the amount of daylight hours"""
        daylight_hours = daylight.get_daylight(curr_date)
        work_hours = daylight_hours
        if max_hours < daylight_hours:
            work_hours = max_hours
        return work_hours

    def get_weather_val(self, weather) -> float:
        # TODO: update this later to consider averaging the hourly weather conditions
        return weather[Method.HOUR]

    def get_weather_segment(
        self, weather, lat, long, timerange
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (
            weather.temps[timerange, lat, long],
            weather.winds[timerange, lat, long],
            weather.precip[timerange, lat, long],
        )

    def check_weather(self, weather, curr_date, site: Site) -> bool:
        """
        Check the weather conditions for the given site on the given day

        # TODO : change this such that the matrix is set once for given method
        """

        # TODO change to getters
        lat = site.get_weather_lat()
        long = site.get_weather_long()
        bool_temp: bool = False
        bool_wind: bool = False
        bool_precip: bool = False
        time = curr_date.timetuple().tm_yday - 1  # 0 indexed.
        timerange = range(time * 24, time * 24 + 24)
        temp_seg, wind_seg, precip_seg = self.get_weather_segment(weather, lat, long, timerange)
        temp_val = self.get_weather_val(temp_seg)
        wind_val = self.get_weather_val(wind_seg)
        precip_val = self.get_weather_val(precip_seg)

        if self._weather_envs[Method.TEMP][0] <= temp_val <= self._weather_envs[Method.TEMP][1]:
            bool_temp = True
        if self._weather_envs[Method.WIND][0] <= wind_val <= self._weather_envs[Method.WIND][1]:
            bool_wind = True
        if (
            self._weather_envs[Method.PRECIP][0]
            <= precip_val
            <= self._weather_envs[Method.PRECIP][1]
        ):
            bool_precip = True

        # if weather permits
        if bool_precip and bool_wind and bool_temp:
            return True
        # if weather conditions are not good
        else:
            return False

    def get_name(self) -> str:
        return self._name
