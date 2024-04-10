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
import sys

from numpy import average
from scheduling.surveying_dataclasses import DetectionRecord
from scheduling.survey_planner import SurveyPlanner
from constants.error_messages import Runtime_Error_Messages as rem


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
            print(rem.INVALID_REDUND_FILTER_ERROR.format(filter=redund_filter, method=method_name))
            sys.exit()
