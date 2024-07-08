"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        schedule_dataclasses
Purpose: Module for holding the different dataclasses used for scheduling

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

from dataclasses import dataclass, field
from datetime import date
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


@dataclass
class EmissionDetectionReport:
    site: str
    equipment_group: str
    component: str
    measured_rate: float
    true_rate: float
    current_date: date = None
    emis_start_date: date = None
    estimated_start_date: date = None

    def to_report_summary(self):
        return {
            eca.COMP: self.component,
            eca.M_RATE: self.measured_rate,
        }


@dataclass
class EquipmentGroupSurveyReport:
    site: str
    equipment_group: str
    measured_rate: float
    true_rate: float
    survey_date: date = None
    emissions_detected: list[EmissionDetectionReport] = field(default_factory=list)

    def to_report_summary(self, expand: bool = False):
        if expand:
            return {
                eca.SITE_ID: self.site,
                eca.EQG: self.equipment_group,
                eca.COMP: [comp.to_report_summary() for comp in self.emissions_detected],
            }
        return {
            eca.SITE_ID: self.site,
            eca.EQG: self.equipment_group,
            eca.M_RATE: self.measured_rate,
        }


@dataclass
class SiteSurveyReport:
    site_id: str
    time_surveyed: int = 0
    time_surveyed_current_day: int = 0
    time_spent_to_travel: int = 0
    survey_complete: bool = False
    survey_in_progress: bool = False
    equipment_groups_surveyed: list[EquipmentGroupSurveyReport] = field(default_factory=list)
    survey_level: str = None
    site_measured_rate: float = 0.0
    site_true_rate: float = 0.0
    site_flagged: bool = False
    survey_completion_date: date = None
    survey_start_date: date = None
    method: str = None

    def to_report_summary(self, expand: bool = False):
        if expand:
            return {
                eca.SITE_ID: self.site_id,
                eca.SURVEY_LEVEL: self.survey_level,
                eca.FLAGGED: self.site_flagged,
                eca.SURVEY_COMPLETION_DATE: self.survey_completion_date,
                eca.SURVEY_START_DATE: self.survey_start_date,
                eca.M_RATE: self.site_measured_rate,
                eca.METHOD: self.method,
                eca.EQG: [eqg.to_report_summary(expand) for eqg in self.equipment_groups_surveyed],
            }
        return {
            eca.SITE_ID: self.site_id,
            eca.SURVEY_LEVEL: self.survey_level,
            eca.M_RATE: self.site_measured_rate,
            eca.FLAGGED: self.site_flagged,
            eca.SURVEY_COMPLETION_DATE: self.survey_completion_date,
            eca.SURVEY_START_DATE: self.survey_start_date,
            eca.METHOD: self.method,
        }


@dataclass
class CrewDailyReport:
    crew_id: int
    day_time_remaining: int
    deployed: bool = False


@dataclass
class TaggingInfo:
    measured_rate: float
    curr_date: date
    t_since_LDAR: int
    company: str
    crew: str
    report_delay: int
