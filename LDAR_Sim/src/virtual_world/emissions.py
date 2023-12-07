from datetime import date
from typing import Any

from numpy.random import binomial


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
        self._tagged: bool = False
        self._days_since_tagged: int = 0
        self._tagged_by_company: str = None
        self._tagged_by_crew: str = None
        self._flagged_by: str = None
        self._init_detect_by: str = None
        self._init_detect_date: date = None
        self._tech_spat_cov_probs: dict[str, float] = tech_spat_cov_probs
        self._tech_spat_covs: dict[str, int] = {}

        if simulation_sd >= start_date:
            self._status = "Active"
        else:
            self._status = "Inactive"

    def update(self):
        """
        Increments duration values
        """
        if self._status == "Active":
            self._active_days += 1

        if self._tagged:
            self._days_since_tagged += 1

    def check_spatial_cov(self, method) -> int:
        if method not in self._tech_spat_covs:
            cov_prob: float = self._tech_spat_cov_probs[method]
            self._tech_spat_covs[method] = binomial(1, cov_prob)
        return self._tech_spat_covs[method]

    def activate() -> str:
        return ""

    def get_emis_vol(self) -> float:
        return self._active_days * self._rate * 86.4

    def get_tagged(self):
        return self._tagged

    def set_tagged(self):
        self._tagged = True

    def set_init_detect_by(self, init_detect_by):
        self._init_detect_by = init_detect_by

    def set_init_detect_date(self, init_detect_date):
        self._init_detect_date = init_detect_date

    def set_tagged_by_company(self, tagged_by_company):
        self._tagged_by_company = tagged_by_company

    def set_measured_rate(self, measured_rate):
        self._measured_rate = measured_rate

    def get_rate(self) -> float:
        return self._rate

    def get_status(self) -> str:
        return self._status

    def get_summary_dict(self) -> dict[str, Any]:
        summary_dict = {}
        summary_dict.update({("Emissions ID", self._emissions_id)})
        summary_dict.update({("Status", self._status)})
        summary_dict.update({("Days Active", self._active_days)})
        summary_dict.update({("Volume Emitted", self.get_emis_vol())})
        summary_dict.update({("Date Began", self._start_date)})
        summary_dict.update({("Initially Detected By", self._init_detect_by)})
        summary_dict.update({("Tagged", self._tagged)})
        summary_dict.update({("Tagged By", self._tagged_by_company)})
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
