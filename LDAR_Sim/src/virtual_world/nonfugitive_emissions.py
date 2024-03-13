"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        nonfugitive_emissions
Purpose: The nonfugitive emissions module.

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
from typing import Any

from typing_extensions import override

from numpy import average
from utils import conversion_constants as conv_const
from virtual_world.emissions import Emission
from file_processing.output_processing.output_utils import EmisInfo, EMIS_DATA_COL_ACCESSORS as eca

EXPIRE = "expired"


class NonRepairableEmission(Emission):
    def __init__(
        self,
        emission_n: int,
        rate: float,
        start_date: date,
        simulation_sd: date,
        repairable: bool,
        tech_spat_cov_probs: dict[str, float],
        duration: int,
    ):
        super().__init__(
            emission_n,
            rate,
            start_date,
            simulation_sd,
            repairable,
            tech_spat_cov_probs,
        )
        self._record: bool = False
        self._recorded_by_company: str = None
        self._recorded_by_crew: str = None
        self._expiry_date: date = None
        self._duration: int = duration
        days_active_b4_sim: int = (simulation_sd - start_date).days
        self._days_active_b4_sim = days_active_b4_sim if days_active_b4_sim > 0 else 0
        self._estimated_days_active_after_detection: int = 0

    def __reduce__(self):
        return self._reconstruct_nonfugitive_emission, (self.__dict__,)

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def _reconstruct_nonfugitive_emission(cls, state):
        instance = cls.__new__(cls)
        instance.__setstate__(state)
        return instance

    def get_daily_emissions(self) -> float:
        return self._rate * 86.4

    def expire(self, emis_info: EmisInfo):
        """
        Checks the days since start against the duration
        Ends the emission if possible
        """
        self._recorded_by_company = EXPIRE
        self._status = EXPIRE
        emis_info.emis_expired += 1
        self._expiry_date = self._start_date + timedelta(days=(self._active_days))

    def estimate_start_date(self, cur_date: date, t_since_ldar: int) -> None:
        """Estimates the start date and days activate of the fugitive emission based on
        the time since the last LDAR-SIm and the current date (discovery date)

        Args:
            cur_date (date): The current date in the simulation
            t_since_ldar (int): THe time in days since the site at which the emissions
            was discovered last received LDAR
        """
        # TODO implement user definable duration assumptions
        duration: int = t_since_ldar
        self._estimated_days_active = duration
        self._estimated_date_began = cur_date - timedelta(days=duration)

    def record_emission(
        self,
        measured_rate: float,
        cur_date: date,
        t_since_ldar: int,
        company: str,
        crew_id: str,
    ):
        """Attempts to record an emission. If an emission is not recorded
            This function will record. If it is already record, the
            function will return false.

        Returns:
            [bool]: Is the emission new?
        """
        self._estimated_days_active_after_detection = t_since_ldar

        if self._record:
            # TODO fix this up
            self._measured_rate = average([self._measured_rate, measured_rate])
            self._estimated_days_active += t_since_ldar
            return False

        self._record = True

        self._measured_rate = measured_rate
        self.estimate_start_date(cur_date, t_since_ldar)

        self._recorded_by_company = company
        self._recorded_by_crew = crew_id
        return True

    @override
    def calc_est_emis_vol(self, end_date: date) -> float:
        if self._estimated_date_began is None:
            return 0
        total_estimated_days_active: int = (
            self._estimated_days_active + self._estimated_days_active_after_detection
        )
        if self._estimated_date_began + timedelta(days=total_estimated_days_active) > end_date:
            total_estimated_days_active = (end_date - self._estimated_date_began).days
        self._estimated_days_active = total_estimated_days_active
        return (
            (total_estimated_days_active)
            * (self._measured_rate if self._measured_rate is not None else 0)
            * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
        )

    @override
    def update(self, emis_info: EmisInfo) -> bool:
        is_active: bool = super().update(emis_info)
        if is_active:
            if self._active_days + self._days_active_b4_sim >= self._duration:
                self.expire(emis_info)
                is_active = False
        return is_active

    @override
    def get_summary_dict(self, end_date: date) -> dict[str, Any]:
        estimated_vol_emitted: float = self.calc_est_emis_vol(end_date=end_date)
        summary_dict: dict[str, Any] = super().get_summary_dict()
        summary_dict.update({(eca.RECORDED, self._record)})
        summary_dict.update({(eca.RECORDED_BY, self._recorded_by_company)})
        summary_dict.update({(eca.EST_VOL_EMIT, estimated_vol_emitted)})
        return summary_dict

    @override
    def activate(self, date: date) -> bool:
        if self._start_date <= date:
            self._status = "Active"
            return True
        else:
            return False
