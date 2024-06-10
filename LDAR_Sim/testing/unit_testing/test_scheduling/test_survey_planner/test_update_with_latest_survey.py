"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_update_with_latest_survey.py
Purpose: Module for testing test_update_with_latest_survey for FollowUpSurveyPlanner

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
from src.virtual_world.sites import Site
from scheduling.follow_up_survey_planner import (
    FollowUpSurveyPlanner,
    StationaryFollowUpSurveyPlanner,
)
from scheduling.surveying_dataclasses import DetectionRecord


def test_update_with_latest_survey(mocker):
    """
    Function to test the update_with_latest_survey function in FollowUpSurveyPlanner
    """
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 1)
    follow_up_survey_planner = FollowUpSurveyPlanner(detection_record, detect_date)
    method_name = "test_method"
    redund_filter = FollowUpSurveyPlanner.REDUND_FILTER_RECENT
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 2)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 3)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 4)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 5)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.5)
    detect_date = date(2021, 1, 6)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    new_detection = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 7)
    follow_up_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )
    assert follow_up_survey_planner.rate_at_site == 0.1
    assert follow_up_survey_planner._detected_rates == [0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.1]
    assert follow_up_survey_planner._latest_detection_date == date(2021, 1, 7)


def test_update_with_avrg_survey(mocker):
    """
    Function to test the update_with_latest_survey function in FollowUpSurveyPlanner
    """
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 1)
    follow_up_survey_planner = FollowUpSurveyPlanner(detection_record, detect_date)
    method_name = "test_method"
    redund_filter = FollowUpSurveyPlanner.REDUND_FILTER_AVERAGE
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 2)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 3)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 4)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 5)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.5)
    detect_date = date(2021, 1, 6)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    new_detection = DetectionRecord(site_id=1, site=mocker, rate_detected=0.6)
    detect_date = date(2021, 1, 7)
    follow_up_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )
    follow_up_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )
    assert round(follow_up_survey_planner.rate_at_site, 3) == 0.275
    assert follow_up_survey_planner._detected_rates == [0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.6, 0.6]
    assert follow_up_survey_planner._latest_detection_date == date(2021, 1, 7)


def test_update_with_max_survey(mocker):
    """
    Function to test the update_with_latest_survey function in FollowUpSurveyPlanner
    """
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 1)
    follow_up_survey_planner = FollowUpSurveyPlanner(detection_record, detect_date)
    method_name = "test_method"
    redund_filter = FollowUpSurveyPlanner.REDUND_FILTER_MAX
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 2)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 3)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 4)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 5)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.5)
    detect_date = date(2021, 1, 6)
    follow_up_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    new_detection = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 7)
    follow_up_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )
    assert follow_up_survey_planner.rate_at_site == 0.5
    assert follow_up_survey_planner._detected_rates == [0.1, 0.1, 0.1, 0.1, 0.1, 0.5, 0.1]
    assert follow_up_survey_planner._latest_detection_date == date(2021, 1, 7)


def test_update_with_rolling_survey(mocker):
    """
    Function to test the update_with_latest_survey function in FollowUpSurveyPlanner
    """
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 1)
    stationary_survey_planner = StationaryFollowUpSurveyPlanner(detection_record, detect_date)
    method_name = "test_method"
    redund_filter = "rolling_average"
    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 2)
    stationary_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 3)
    stationary_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 4)
    stationary_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.1)
    detect_date = date(2021, 1, 5)
    stationary_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    detection_record = DetectionRecord(site_id=1, site=mocker, rate_detected=0.5)
    detect_date = date(2021, 1, 6)
    stationary_survey_planner.update_with_latest_survey(
        detection_record, redund_filter, method_name, detect_date
    )

    new_detection = DetectionRecord(site_id=1, site=mocker, rate_detected=0.6)
    detect_date = date(2021, 1, 7)
    stationary_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )

    stationary_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )

    stationary_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )
    stationary_survey_planner.update_with_latest_survey(
        new_detection, redund_filter, method_name, detect_date
    )
    assert stationary_survey_planner._detected_rates == [
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.5,
        0.6,
        0.6,
        0.6,
        0.6,
    ]
    assert stationary_survey_planner._latest_detection_date == date(2021, 1, 7)
    assert round(stationary_survey_planner.rate_at_site, 6) == 0.442857
    assert round(stationary_survey_planner.rate_at_site_long, 5) == 0.34000
