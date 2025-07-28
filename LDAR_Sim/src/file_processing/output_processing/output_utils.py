"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        output_utils.py
Purpose: Contains utility functions and data classes for output processing.

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

from dataclasses import dataclass
from typing import Tuple
import numpy as np
from constants.error_messages import Output_Processing_Messages as om


def percent_difference(a: float, b: float) -> float:
    if a == 0 and b == 0:
        return 0
    return abs(a - b) / ((a + b) / 2) * 100


def relative_difference(aquired_value: float, true_value: float) -> float:
    if true_value == 0:
        return 0
    return (aquired_value - true_value) / true_value * 100


def percentage_formatter(x: float, pos):
    x = x / 100
    return f"{x:.0%}"


def luminance_shift(
    color: Tuple[float, float, float], factor: float = 0.3, lighten: bool = True
) -> Tuple[float, float, float]:
    if not lighten:
        factor = -factor
        return (max(color[0] + factor, 0), max(color[1] + factor, 0), max(color[2] + factor, 0))
    else:
        return (min(color[0] + factor, 1), min(color[1] + factor, 1), min(color[2] + factor, 1))


@dataclass
class TsEmisData:
    daily_emis: float = 0
    daily_emis_mit: float = 0
    daily_emis_non_mit: float = 0
    active_leaks: int = 0

    def __add__(self, other):
        if isinstance(other, TsEmisData):
            daily_emis = self.daily_emis + other.daily_emis
            daily_emis_mit = self.daily_emis_mit + other.daily_emis_mit
            daily_emis_non_mit = self.daily_emis_non_mit + other.daily_emis_non_mit
            active_leaks = self.active_leaks + other.active_leaks
            return TsEmisData(
                daily_emis=daily_emis,
                daily_emis_mit=daily_emis_mit,
                daily_emis_non_mit=daily_emis_non_mit,
                active_leaks=active_leaks,
            )
        else:
            raise ValueError(om.OPERAND_ADDITION_ERROR)

    def __iadd__(self, other):
        if isinstance(other, TsEmisData):
            self.daily_emis += other.daily_emis
            self.daily_emis_mit += other.daily_emis_mit
            self.daily_emis_non_mit += other.daily_emis_non_mit
            self.active_leaks += other.active_leaks
            return self
        else:
            raise ValueError(om.OPERAND_INPLACE_ADDITION_ERROR)


@dataclass
class TsMethodData:
    method_name: str
    upfront_cost: float = 0.0
    daily_deployment_cost: float = 0.0
    daily_tags: int = 0
    daily_flags: int = 0
    sites_visited: int = 0
    travel_time: int = 0
    survey_time: int = 0


@dataclass
class TaggingFlaggingStats:
    sites_flagged: int = np.nan
    leaks_tagged: int = np.nan


@dataclass
class CrewDeploymentStats:
    deployment_cost: float = 0.0
    sites_visited: int = 0
    travel_time: int = 0
    survey_time: int = 0

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CrewDeploymentStats):
            return vars(self) == vars(other)
        return False


@dataclass
class EmisInfo:
    leaks_repaired: int = 0
    leaks_nat_repaired: int = 0
    repair_cost: int = 0
    nat_repair_cost: int = 0
    emis_expired: int = 0
