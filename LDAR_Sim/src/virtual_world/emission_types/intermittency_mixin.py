"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        intermittent_mixin.py
Purpose: Contains intermittency functionality for emissions.

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

from constants.general_const import Conversion_Constants as cc
from file_processing.output_processing.output_utils import EmisInfo
from typing_extensions import override


class IntermittencyMixin:
    def __init__(
        self,
        active_duration: int,
        inactive_duration: int,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )
        self._active_duration: int = active_duration
        self._inactive_duration: int = inactive_duration
        self._days_emitting: int = 0
        self._non_emitting_period_day_count: int = 0
        self._emitting_period_day_count: int = 0
        self._emitting: bool = False

    @override
    def update(self, emis_rep_info: EmisInfo) -> bool:
        is_active: bool = super().update(emis_rep_info)
        if is_active:
            if self._emitting:
                self._days_emitting += 1
                self._emitting_period_day_count += 1
                if self._emitting_period_day_count >= self._active_duration:
                    self._emitting = False
                    self._emitting_period_day_count = 0
            else:
                self._non_emitting_period_day_count += 1
                if self._non_emitting_period_day_count >= self._inactive_duration:
                    self._emitting = True
                    self._non_emitting_period_day_count = 0
        return is_active

    @override
    def calc_true_emis_vol(self) -> float:
        return self._days_emitting * self._rate * cc.GRAMS_PER_SECOND_TO_KG_PER_DAY

    @override
    def activate(self, date: date) -> bool:
        active: bool = super().activate(date)
        if active:
            self._emitting = True
        return active

    @override
    def is_emitting(self) -> bool:
        return self._emitting

    @override
    def get_days_emitting(self) -> int:
        return self._days_emitting
