"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        site_level_method
Purpose: The provides default behaviors for site level methods

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

from datetime import date, timedelta
from math import ceil
from typing import override

from sortedcontainers import SortedList
from file_processing.output_processing.output_utils import TaggingFlaggingStats
from programs.method import Method
from scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule
from scheduling.follow_up_survey_planner import FollowUpSurveyPlanner
from scheduling.surveying_dataclasses import DetectionRecord
from sensors.default_site_level_sensor import DefaultSiteLevelSensor
from sensors.METEC_NoWind_sensor import METECNWSite
from sensors.sensor_constant_mapping import (
    SENS_TYPE,
    SENS_MDL,
    SENS_QE,
    ERR_MSG_UNKNOWN_SENS_TYPE,
)
import sys


class SiteLevelMethod(Method):
    MEASUREMENT_SCALE = "site"

    THRESHOLD_INT_PRIO = "threshold"
    PROPORTION_INT_PRIO = "proportion"
    INVALID_INTERACTION_PRIO_ERROR = (
        "Error: Invalid interaction_priority of {priority} set for method: {method}"
    )

    def __init__(
        self,
        name,
        properties,
        consider_weather,
        sites,
        follow_up_schedule: FollowUpMobileSchedule,
    ) -> None:
        super().__init__(name, properties, consider_weather, sites)
        interaction_priority: str = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
            Method.METHOD_FOLLOW_UP_PROPERTIES_INTERACT_PRIO_ACCESSOR
        ]
        if interaction_priority == self.THRESHOLD_INT_PRIO:
            self._threshold_first: bool = True
        elif interaction_priority == self.PROPORTION_INT_PRIO:
            self._threshold_first: bool = False
        else:
            print(
                self.INVALID_INTERACTION_PRIO_ERROR.format(
                    priority=interaction_priority, method=name
                )
            )
            sys.exit()
        self._candidates_for_flags: SortedList[FollowUpSurveyPlanner] = SortedList(
            key=lambda x: -x.rate_at_site
        )
        self._site_IDs_in_consideration_for_flag: dict[str, bool] = {}
        self._site_IDs_in_follow_up_queue: dict[str, bool] = (
            follow_up_schedule.get_site_id_queue_list()
        )
        self._first_candidate_date: date = None
        self._delay: int = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
            Method.METHOD_FOLLOW_UP_PROPERTIES_DELAY_ACCESSOR
        ]
        self._proportion: float = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
            Method.METHOD_FOLLOW_UP_PROPERTIES_PROP_ACCESSOR
        ]
        self._threshold: float = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
            Method.METHOD_FOLLOW_UP_PROPERTIES_THRESH_ACCESSOR
        ]
        self._inst_threshold: float = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
            Method.METHOD_FOLLOW_UP_PROPERTIES_INST_THRESH_ACCESSOR
        ]
        if self._inst_threshold is None:
            self._inst_threshold = float("inf")
        self._redund_filter: str = properties[Method.METHOD_FOLLOW_UP_PROPERTIES_ACCESSOR][
            Method.METHOD_FOLLOW_UP_PROPERTIES_REDUND_FILTER_ACCESSOR
        ]
        self._follow_up_schedule: FollowUpMobileSchedule = follow_up_schedule
        self._detection_count = 0

    def update(self, current_date: date) -> TaggingFlaggingStats:
        # TODO add user configurable follow_up parameter to allow
        # for up to a certain % variation between rates
        date_to_check: date = current_date - timedelta(days=self._reporting_delay)
        new_detections: list[DetectionRecord] = self._detection_records.get(date_to_check, [])
        for detection_record in new_detections:
            # Check that the site hasn't gotten a survey with a method
            # that can tag leaks since the date the detection was made
            if detection_record.site.get_latest_tagging_survey_date() < date_to_check:
                # If the site is already in the list for potential flags, pop it from the list,
                # update it based on the new measurements and the redundancy filter, and either
                # add it back to the list or bypass the list if it now passes the instant threshold.
                if self._site_IDs_in_consideration_for_flag.get(detection_record.site_id, False):
                    existing_plan: FollowUpSurveyPlanner = self._get_plan_from_candidates(
                        detection_record.site_id
                    )
                    existing_plan.update_with_latest_survey(
                        detection_record, self._redund_filter, self._name, date_to_check
                    )
                    if existing_plan.rate_at_site >= self._inst_threshold:
                        self._follow_up_schedule.add_previous_queued_to_survey_queue(existing_plan)
                    elif existing_plan.rate_at_site >= self._threshold:
                        self._candidates_for_flags.add(existing_plan)
                # If the site is already queued to get a follow-up,
                # update the queue priority based on new results
                elif self._site_IDs_in_follow_up_queue[detection_record.site_id]:
                    existing_plan: FollowUpSurveyPlanner = (
                        self._follow_up_schedule.get_plan_from_queue(detection_record.site_id)
                    )
                    existing_plan.update_with_latest_survey(
                        detection_record, self._redund_filter, self._name, date_to_check
                    )
                    if existing_plan.rate_at_site >= self._inst_threshold:
                        self._follow_up_schedule.add_previous_queued_to_survey_queue(existing_plan)
                    elif existing_plan.rate_at_site >= self._threshold:
                        self._follow_up_schedule.add_to_survey_queue(existing_plan)
                # Otherwise, the site is not already in processing for a follow-up,
                # process as normal
                else:
                    # if above the instant threshold, add to higher priority queue
                    if detection_record.rate_detected >= self._inst_threshold:
                        self._follow_up_schedule.add_previous_queued_to_survey_queue(
                            FollowUpSurveyPlanner(detection_record, date_to_check)
                        )
                    # if the detected rate is non-zero, and above the threshold add to queue
                    elif (
                        detection_record.rate_detected != 0
                        and detection_record.rate_detected >= self._threshold
                    ):
                        self._candidates_for_flags.add(
                            FollowUpSurveyPlanner(detection_record, date_to_check)
                        )
                    # count that there was a detection, but it wasn't above the threshold
                    elif detection_record.rate_detected > 0:
                        self._detection_count += 1

        # Queue candidates based on follow up work practice specified.
        tags_flags: TaggingFlaggingStats = TaggingFlaggingStats(
            sites_flagged=self.update_candidates_for_flags(current_date)
        )
        return tags_flags

    def update_candidates_for_flags(self, current_date: date) -> int:
        n_flags: int = 0

        if self._first_candidate_date is None:
            candidates_not_empty: bool = bool(self._candidates_for_flags)
            if candidates_not_empty:
                self._first_candidate_date = current_date
            else:
                return n_flags
        if (current_date - self._first_candidate_date).days >= self._delay:
            self._filter_candidates_by_proportion()

            for survey_plan in self._get_candidates():
                self._follow_up_schedule.add_to_survey_queue(survey_plan)
                n_flags += 1
        return n_flags

    def _get_plan_from_candidates(self, site_id: str) -> FollowUpSurveyPlanner:
        survey_plan: FollowUpSurveyPlanner = next(
            [plan for plan in self._candidates_for_flags if plan.site_id == site_id],
            None,
        )
        self._candidates_for_flags.remove(survey_plan)
        return survey_plan

    def _filter_candidates_by_proportion(self) -> None:
        # If interaction priority is threshold first, simply get the number of
        # candidates to keep by calculating the proportion of the total_candidates
        if self._threshold_first:
            total_candidates: int = len(self._candidates_for_flags)
            candidates_to_keep: int = ceil(float(total_candidates) * self._proportion)
        # Otherwise, all detections must be accounted for, including ones under the threshold
        # Using the detection count this is possible, but it is important to ensure the number of
        # candidates to keep does not exceed the size of the candidate list to avoid runtime errors
        else:
            sites_for_consideration: int = self._detection_count
            sites_to_keep: int = ceil(float(sites_for_consideration * self._proportion))
            candidates_to_keep = min(sites_to_keep, len(self._candidates_for_flags))
        # Trim the list of candidates to the first "candidates_to_keep"
        # elements of the list of candidates. Since the list is sorted by rate,
        # these are the candidates with biggest measured rates.
        self._candidates_for_flags = SortedList(
            self._candidates_for_flags[:candidates_to_keep],
            key=lambda x: -x.rate_at_site,
        )

    def _get_candidates(self) -> SortedList[FollowUpSurveyPlanner]:
        # Returns the candidates list, and resets it, as well as the detection count
        # and the first detection date
        candidates: SortedList[FollowUpSurveyPlanner] = self._candidates_for_flags
        self._candidates_for_flags = SortedList(key=lambda x: -x.rate_at_site)
        self._detection_count = 0
        self._first_candidate_date = None
        return candidates

    def _initialize_sensor(self, sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): The dictionary of information the user has
            provided to the method about the sensor
        """
        if sensor_info[SENS_TYPE] == "default":
            self._sensor = DefaultSiteLevelSensor(sensor_info[SENS_MDL], sensor_info[SENS_QE])
        elif sensor_info[SENS_TYPE] == "METEC_no_wind":
            self._sensor = METECNWSite(sensor_info[SENS_MDL], sensor_info[SENS_QE])
        else:
            print(ERR_MSG_UNKNOWN_SENS_TYPE.format(method=self._name))
            sys.exit()

    @override
    def get_follow_up_method_name(self) -> str:
        return self._follow_up_schedule._method
