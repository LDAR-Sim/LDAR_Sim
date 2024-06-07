"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        component_level_method.py
Purpose: The module provides default behaviors for component level methods

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
from queue import PriorityQueue
import sys
from typing import Tuple
from constants.error_messages import Input_Processing_Messages as ipm
from file_processing.output_processing.output_utils import CrewDeploymentStats, TaggingFlaggingStats
from programs.method import Method
from scheduling.schedule_dataclasses import (
    CrewDailyReport,
    SiteSurveyReport,
    TaggingInfo,
)
from scheduling.workplan import Workplan
from sensors.default_component_level_sensor import DefaultComponentLevelSensor
from sensors.OGI_camera_rk import OGICameraRKSensor
from sensors.OGI_camera_zim import OGICameraZimSensor
from sensors.METEC_NoWind_sensor import METECNWComponent
from virtual_world.sites import Site
import constants.param_default_const as pdc


class ComponentLevelMethod(Method):
    MEASUREMENT_SCALE = "component"

    def __init__(self, name, properties, consider_weather, sites):
        super().__init__(name, properties, consider_weather, sites)
        self._emissions_tagged_daily: int = 0

    def update(self, current_date: date) -> TaggingFlaggingStats:
        tags_flags: TaggingFlaggingStats = TaggingFlaggingStats(
            leaks_tagged=self._emissions_tagged_daily
        )
        self._emissions_tagged_daily = 0
        return tags_flags

    def survey_site(
        self,
        crew: CrewDailyReport,
        survey_report: SiteSurveyReport,
        site_to_survey: Site,
        weather,
        curr_date: date,
    ) -> Tuple[SiteSurveyReport, float]:
        survey_report, site_travel_time, last_site_survey, site_visit = super().survey_site(
            crew=crew,
            survey_report=survey_report,
            site_to_survey=site_to_survey,
            weather=weather,
            curr_date=curr_date,
        )
        if survey_report.survey_complete:
            prev_tagging_survey_date: date = site_to_survey.get_latest_tagging_survey_date()
            days_since_last_survey: int = (curr_date - prev_tagging_survey_date).days
            site_to_survey.set_latest_tagging_survey_date(curr_date)
            for equip_group_survey_report in survey_report.equipment_groups_surveyed:
                for emission_detection_report in equip_group_survey_report.emissions_detected:
                    if emission_detection_report.measured_rate > 0:
                        tagging_info = TaggingInfo(
                            measured_rate=emission_detection_report.measured_rate,
                            curr_date=curr_date,
                            t_since_LDAR=days_since_last_survey,
                            company=self._name,
                            crew=crew.crew_id,
                            report_delay=self._reporting_delay,
                        )
                        site_to_survey.tag_emissions_at_component(
                            emission_detection_report.equipment_group,
                            emission_detection_report.component,
                            tagging_info=tagging_info,
                        )
                        self._emissions_tagged_daily += 1
        return survey_report, site_travel_time, last_site_survey, site_visit

    def _initialize_sensor(self, sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): _description_
        """
        # TODO: change to mapping?
        if sensor_info[pdc.Method_Params.TYPE] == "default":
            self._sensor = DefaultComponentLevelSensor(
                sensor_info[pdc.Method_Params.MDL], sensor_info[pdc.Method_Params.QE]
            )
        elif sensor_info[pdc.Method_Params.TYPE] == "OGI_camera_zim":
            self._sensor = OGICameraZimSensor(
                sensor_info[pdc.Method_Params.MDL], sensor_info[pdc.Method_Params.QE]
            )
        elif sensor_info[pdc.Method_Params.TYPE] == "OGI_camera_rk":
            self._sensor = OGICameraRKSensor(
                sensor_info[pdc.Method_Params.MDL], sensor_info[pdc.Method_Params.QE]
            )
        elif sensor_info[pdc.Method_Params.TYPE] == "METEC_no_wind":
            self._sensor = METECNWComponent(
                sensor_info[pdc.Method_Params.MDL], sensor_info[pdc.Method_Params.QE]
            )
        else:
            print(ipm.ERR_MSG_UNKNOWN_SENS_TYPE.format(method=self._name))
            sys.exit()

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
        for crew in self._crew_reports:
            # TODO : if method is daylight sensitive, check for max daylight
            crew.day_time_remaining = day_time_remaining
            priority_queue.put((-crew.day_time_remaining, crew.crew_id, crew))

        # If the cost type for the method is per day, calculate the deployment cost for day
        # based off the number of crews being deployed
        if self.cost_type == self.PER_DAY_COST:
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
                survey_report, travel_time, last_site_survey, site_visited = self.survey_site(
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
                if site_visited:
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

                    if self.cost_type == self.PER_SITE_COST:
                        site_survey_cost = site_to_survey.get_survey_cost(self._name)
                        if site_survey_cost == 0 and self.cost > 0:
                            site_survey_cost = self.cost
                        deploy_stats.deployment_cost += site_survey_cost
            # Update the survey planner. If the survey was not finished, the update will
            # indicate that the particular site needs to be requeued with higher priority
            workplan.add_survey_report(survey_report, survey_plan)
            if survey_report.survey_complete:
                self._site_survey_reports.append(survey_report)
        return deploy_stats
