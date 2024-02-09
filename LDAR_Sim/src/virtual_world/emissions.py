"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        emissions
Purpose: The emissions module.

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
from typing import Any

from numpy.random import binomial
from file_processing.output_processing.output_utils import (
    EmisRepairInfo,
    EMIS_DATA_COL_ACCESSORS as eca,
)

from utils.conversion_constants import GRAMS_PER_SECOND_TO_KG_PER_DAY


class Emission:
    def __init__(
        self,
        emission_n: int,
        rate: float,
        start_date: date,
        simulation_sd: date,
        repairable: bool,
        tech_spat_cov_probs: dict[str, float],
    ) -> None:
        self._emissions_id: str = f"{str(emission_n).zfill(10)}"
        self._rate: float = rate
        self._start_date: date = start_date
        self._repairable: bool = repairable

        self._estimated_date_began: date = None
        self._estimated_days_active: int = 0
        self._active_days: int = 0
        self._measured_rate: float = None
        self._flagged_by: str = None
        self._init_detect_by: str = None
        self._init_detect_date: date = None
        self._tech_spat_cov_probs: dict[str, float] = tech_spat_cov_probs
        self._tech_spat_covs: dict[str, int] = {}
        self._status = "Inactive"

    def update(self, emis_rep_info: EmisRepairInfo) -> bool:
        """
        Increments duration values
        """
        if self._status == "Active":
            self._active_days += 1
            return True
        else:
            return False

    def check_spatial_cov(self, method) -> int:
        if method not in self._tech_spat_covs:
            name_str: str = f"{method} Spatial Coverage"
            cov_prob: float = self._tech_spat_cov_probs[method]
            self._tech_spat_covs[name_str] = binomial(1, cov_prob)
        return self._tech_spat_covs[name_str]

    def activate() -> bool:
        return False

    def get_emis_vol(self) -> float:
        return self._active_days * self._rate * GRAMS_PER_SECOND_TO_KG_PER_DAY

    def update_detection_records(self, company: str, detect_date: date):
        if self._init_detect_by is None:
            self.set_init_detect_by(company)
            self.set_init_detect_date(detect_date)

    def set_init_detect_by(self, init_detect_by):
        self._init_detect_by = init_detect_by

    def set_init_detect_date(self, init_detect_date):
        self._init_detect_date = init_detect_date

    def set_measured_rate(self, measured_rate):
        self._measured_rate = measured_rate

    def get_rate(self) -> float:
        return self._rate

    def get_status(self) -> str:
        return self._status

    def get_daily_emis(self) -> float:
        return self._rate * GRAMS_PER_SECOND_TO_KG_PER_DAY

    def get_summary_dict(self) -> dict[str, Any]:
        summary_dict = {}
        summary_dict.update({(eca.EMIS_ID, self._emissions_id)})
        summary_dict.update({(eca.STATUS, self._status)})
        summary_dict.update({(eca.DAYS_ACT, self._active_days)})
        summary_dict.update({(eca.T_VOL_EMIT, self.get_emis_vol())})
        summary_dict.update({(eca.T_RATE, self._rate)})
        summary_dict.update({(eca.M_RATE, self._measured_rate)})
        summary_dict.update({(eca.DATE_BEG, self._start_date)})
        summary_dict.update({(eca.INIT_DETECT_BY, self._init_detect_by)})
        summary_dict.update({(eca.INIT_DETECT_DATE, self._init_detect_date)})
        summary_dict.update({(eca.TAGGED, "N/A")})
        summary_dict.update({(eca.TAGGED_BY, "N/A")})
        summary_dict.update(self._tech_spat_covs)
        return summary_dict


class NonRepairableEmission(Emission):
    def __init__(self, emission_n, source_id, rate, start_date, simulation_sd, repairable):
        super().__init__(
            emission_n,
            rate,
            start_date,
            simulation_sd,
            repairable,
        )
