"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        follow_up_survey_planner
Purpose: The extended Survey Planner module, specifically for Follow up surveys.

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
import logging
import sys

from numpy import average, isnan
from scheduling.surveying_dataclasses import DetectionRecord
from scheduling.survey_planner import SurveyPlanner
from constants.error_messages import Runtime_Error_Messages as rem
import constants.param_default_const as pdc
import pandas as pd


class FollowUpSurveyPlanner(SurveyPlanner):
    REDUND_FILTER_RECENT = "recent"
    REDUND_FILTER_MAX = "max"
    REDUND_FILTER_AVERAGE = "average"

    def __init__(self, detection_record: DetectionRecord, detect_date: date) -> None:
        super().__init__(detection_record.site)
        self.rate_at_site: float = detection_record.rate_detected
        self.site_id: str = detection_record.site_id
        self._detected_rates: list[float] = [detection_record.rate_detected]
        self._latest_detection_date: date = detect_date

    def update_with_latest_survey(
        self,
        new_detection: DetectionRecord,
        redund_filter: str,
        method_name: str,
        detect_date: date,
    ) -> None:
        if redund_filter == self.REDUND_FILTER_RECENT:
            self.rate_at_site = new_detection.rate_detected
            self._detected_rates.append(new_detection.rate_detected)
            self._latest_detection_date = detect_date
        elif redund_filter == self.REDUND_FILTER_AVERAGE:
            self._detected_rates.append(new_detection.rate_detected)
            self.rate_at_site = average(self._detected_rates)
            self._latest_detection_date = detect_date
        elif redund_filter == self.REDUND_FILTER_MAX:
            self._detected_rates.append(new_detection.rate_detected)
            self.rate_at_site = max(self._detected_rates)
            self._latest_detection_date = detect_date
        else:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                rem.INVALID_REDUND_FILTER_ERROR.format(filter=redund_filter, method=method_name)
            )
            sys.exit()

    def should_follow_up(self, threshold: float) -> bool:
        return self.rate_at_site >= threshold

    def should_follow_up_long(self, threshold: float) -> bool:
        return False


class StationaryFollowUpSurveyPlanner(FollowUpSurveyPlanner):
    def __init__(
        self,
        detection_record: DetectionRecord,
        detect_date: date,
        small_window: int,
        long_window: int,
    ) -> None:
        super().__init__(detection_record, detect_date)
        self._small_window: int = small_window
        self._long_window: int = long_window
        self.rate_at_site: float = 0
        self.rate_at_site_long: float = 0

    def update_with_latest_survey(
        self,
        new_detection: DetectionRecord,
        redund_filter: str,
        method_name: str,
        detect_date: date,
    ) -> None:
        if redund_filter == pdc.Method_Params.ROLLING_AVRG:
            self._detected_rates.append(new_detection.rate_detected)
            series_detect_rates = pd.Series(self._detected_rates)
            self.rate_at_site = (
                series_detect_rates.rolling(
                    window=self._small_window, min_periods=self._small_window
                )
                .mean()
                .iloc[-1]
            )
            self.rate_at_site_long = (
                series_detect_rates.rolling(window=self._long_window, min_periods=self._long_window)
                .mean()
                .iloc[-1]
            )
            self._latest_detection_date = detect_date
            if isnan(self.rate_at_site):
                self.rate_at_site = 0
            if isnan(self.rate_at_site_long):
                self.rate_at_site_long = 0
        else:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                rem.INVALID_REDUND_FILTER_ERROR.format(filter=redund_filter, method=method_name)
            )
            sys.exit()

    def should_follow_up_long(self, threshold: float) -> bool:
        return self.rate_at_site_long >= threshold
