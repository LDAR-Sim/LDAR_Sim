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
from file_processing.output_processing.output_utils import EmisInfo
from constants.general_const import Conversion_Constants as cc, Emission_Constants as ec
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


class Emission:
    EMIS_SUMMARY_DTYPES = {
        eca.EMIS_ID: "object",
        eca.STATUS: "object",
        eca.DAYS_ACT: "int32",
        eca.T_VOL_EMIT: "float64",
        eca.EST_VOL_EMIT: "float64",
        eca.T_RATE: "float64",
        eca.M_RATE: "float64",
        eca.DATE_BEG: "datetime64",
        eca.INIT_DETECT_BY: "object",
        eca.INIT_DETECT_DATE: "datetime64",
        eca.TAGGED: "bool",
        eca.TAGGED_BY: "object",
        eca.DATE_REP_EXP: "datetime64",
    }

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
        self._status = ec.INACTIVE

    def __reduce__(self):
        return (self.__class__._reconstruct_emissions, (self.__dict__,))

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def _reconstruct_emissions(cls, state):
        emission = cls.__new__(cls)
        emission.__setstate__(state)
        return emission

    def update(self, emis_rep_info: EmisInfo) -> bool:
        """
        Increments duration values
        """
        if self._status == ec.ACTIVE:
            self._active_days += 1
            return True
        else:
            return False

    def check_spatial_cov(self, method) -> int:
        name_str: str = f"{method} Spatial Coverage"
        if name_str not in self._tech_spat_covs:
            cov_prob: float = self._tech_spat_cov_probs[method]
            self._tech_spat_covs[name_str] = binomial(1, cov_prob)
        return self._tech_spat_covs[name_str]

    def activate() -> bool:
        return False

    def calc_true_emis_vol(self) -> float:
        return self._active_days * self._rate * cc.GRAMS_PER_SECOND_TO_KG_PER_DAY

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
        return self._rate * cc.GRAMS_PER_SECOND_TO_KG_PER_DAY

    def get_summary_dict(self) -> dict[str, Any]:
        summary_dict = {}
        summary_dict.update({(eca.EMIS_ID, self._emissions_id)})
        summary_dict.update({(eca.STATUS, self._status)})
        summary_dict.update({(eca.DAYS_ACT, self._active_days)})
        summary_dict.update({(eca.EST_DAYS_ACT, self._estimated_days_active)})
        summary_dict.update({(eca.T_VOL_EMIT, self.calc_true_emis_vol())})
        summary_dict.update({(eca.T_RATE, self._rate)})
        summary_dict.update({(eca.M_RATE, self._measured_rate)})
        summary_dict.update({(eca.DATE_BEG, self._start_date)})
        summary_dict.update({(eca.INIT_DETECT_BY, self._init_detect_by)})
        summary_dict.update({(eca.INIT_DETECT_DATE, self._init_detect_date)})
        summary_dict.update({(eca.TAGGED, "N/A")})
        summary_dict.update({(eca.TAGGED_BY, "N/A")})
        summary_dict.update({(eca.RECORDED, "N/A")})
        summary_dict.update({(eca.RECORDED_BY, "N/A")})
        summary_dict.update(self._tech_spat_covs)
        summary_dict.update({(eca.REPAIRABLE, self._repairable)})
        return summary_dict
