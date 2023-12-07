from datetime import date, timedelta
from math import ceil
from typing import Any, Literal
from typing_extensions import override

from virtual_world.emissions import Emission


class FugitiveEmission(Emission):
    def __init__(
        self,
        emission_n: int,
        rate: float,
        start_date: date,
        simulation_sd: date,
        repairable: bool,
        tech_spat_cov_probs: dict[str, float],
        repair_delay: int,
        repair_cost: float,
        nrd: int,
    ):
        super().__init__(
            emission_n,
            rate,
            start_date,
            simulation_sd,
            repairable,
            tech_spat_cov_probs,
        )
        self._repair_delay: int = repair_delay
        self._repair_cost: float = repair_cost
        self._tagging_rep_delay: int = 0
        self._nrd: int = nrd
        self._repair_date: date = None
        days_active_b4_sim: int = (simulation_sd - start_date).days
        self._days_active_b4_sim = days_active_b4_sim if days_active_b4_sim > 0 else 0

    def check_if_repaired(self):
        """
        Checks the days since tagged against the repair delay
        Repairs the emission if possible
        """
        if self._repairable:
            if self._days_since_tagged >= self._repair_delay + self._tagging_rep_delay:
                self._status = "repaired"
                self._repair_date = self._start_date + timedelta(days=(self._active_days))

    def get_init_detect_company(self):
        return self._init_detect_by

    def tagged_today(self) -> bool:
        return (
            self._tagged and (self._days_since_tagged == 0)
        ) and self._tagged_by_company != "natural"

    def update_detection_records(self, company, detect_date):
        if self._init_detect_by is None:
            self._init_detect_by = company
            self._init_detect_date = detect_date

    def get_repair_cost(self) -> float:
        return self._repair_cost

    def get_daily_emissions(self) -> float:
        return self._rate * 86.4

    def natural_repair(self):
        self._tagged = True
        self._tagged_by_company = "natural"
        self._status = "repaired"
        self._repair_date = self._start_date + timedelta(days=(self._active_days))

    # TODO potentially move this into company later
    def estimate_start_date(self, cur_date: date, t_since_ldar: int) -> None:
        """Estimates the start date and days activate of the fugitive emission based on
        the time since the last LDAR-SIm and the current date (discovery date)

        Args:
            cur_date (date): The current date in the simulation
            t_since_ldar (int): THe time in days since the site at which the emissions
            was discovered last received LDAR
        """
        half_duration: int = ceil((t_since_ldar / 2))
        self._estimated_days_active = half_duration
        self._estimated_date_began = cur_date - timedelta(days=half_duration)

    def tag_leak(
        self,
        measured_rate: float,
        cur_date: datetime,
        t_since_ldar: int,
        company: str,
        crew_id: str,
        tagging_rep_delay: int,
    ):
        """Attempts to tag a leak. If a leak is not tagged
            This function will tag. If it is already tagged, the
            function will return false.

        Returns:
            [bool]: Is the leak new?
        """
        if self._tagged:
            return False

        # Add these leaks to the 'tag pool'
        self._tagged = True

        self._measured_rate = measured_rate
        self.estimate_start_date(cur_date, t_since_ldar)

        self._tagged_by_company = company
        self._tagged_by_crew = crew_id
        self._tagging_rep_delay = tagging_rep_delay
        return True

    @override
    def update(self):
        super().update()
        if self._active_days + self._days_active_b4_sim >= self._nrd:
            self.natural_repair()
            return "nat_repaired"
        if self._tagged:
            self.check_if_repaired()
            if self._status == "repaired":
                return "repaired"
        return "no_status_change"

    @override
    def get_summary_dict(self) -> dict[str, Any]:
        summary_dict: dict[str, Any] = super().get_summary_dict()
        summary_dict.update({("Date Repaired", self._repair_date)})
        return summary_dict

    @override
    def activate(self, date: date) -> Literal["Already_Active", "Newly_Active", "Inactive"]:
        activated: str = "Inactive"
        if self._status == "Active":
            activated = "Already_Active"
        elif self._start_date <= date:
            self._status = "Active"
            activated = "Newly_Active"
        return activated
