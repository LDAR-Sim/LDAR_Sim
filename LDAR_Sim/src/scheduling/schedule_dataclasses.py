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


@dataclass
class EmissionDetectionReport:
    site: str
    equipment_group: str
    equipment: str
    measured_rate: float
    true_rate: float
    current_date: date = None
    emis_start_date: date = None
    estimated_start_date: date = None


@dataclass
class EquipmentGroupSurveyReport:
    site: str
    equipment_group: str
    measured_rate: float
    true_rate: float
    survey_date: date = None
    emissions_detected: list[EmissionDetectionReport] = field(default_factory=list)


@dataclass
class SiteSurveyReport:
    site_id: str
    time_surveyed: int = 0
    time_spent_to_travel: int = 0
    survey_complete: bool = False
    survey_in_progress: bool = False
    equipment_groups_surveyed: list[EquipmentGroupSurveyReport] = field(
        default_factory=list
    )
    survey_level: str = None
    site_measured_rate: float = 0.0
    site_true_rate: float = 0.0
    site_flagged: bool = False
    survey_completion_date: date = None
    survey_start_date: date = None
    method: str = None


@dataclass
class CrewDailyReport:
    crew_id: int
    day_time_remaining: int


@dataclass
class TaggingInfo:
    measured_rate: float
    curr_date: date
    t_since_LDAR: int
    company: str
    crew: str
    report_delay: int
