"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        fugitive_emission
Purpose: The fugitive emissions module.

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
from math import ceil
from numpy import random
from typing import Any
from typing_extensions import override
from file_processing.output_processing.output_utils import EmisRepairInfo

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
        self._tagged: bool = False
        self._days_since_tagged: int = 0
        self._tagged_by_company: str = None
        self._tagged_by_crew: str = None
        self._repair_delay: int = repair_delay
        self._repair_cost: float = repair_cost
        # TODO take tagging rep delay out
        self._tagging_rep_delay: int = 0
        self._nrd: int = nrd
        self._repair_date: date = None
        days_active_b4_sim: int = (simulation_sd - start_date).days
        self._days_active_b4_sim = days_active_b4_sim if days_active_b4_sim > 0 else 0

    def check_if_repaired(self, emis_rep_info: EmisRepairInfo) -> bool:
        """
        Checks the days since tagged against the repair delay
        Repairs the emission if possible
        """
        if self._repairable:
            if self._days_since_tagged >= self._repair_delay + self._tagging_rep_delay:
                self._status = "repaired"
                emis_rep_info.leaks_repaired += 1
                emis_rep_info.repair_cost += self.get_repair_cost()
                self._repair_date = self._start_date + timedelta(
                    days=(self._active_days + self._days_active_b4_sim)
                )
                return True
        return False

    def get_init_detect_company(self):
        return self._init_detect_by

    def tagged_today(self) -> bool:
        return (
            self._tagged and (self._days_since_tagged == 0)
        ) and self._tagged_by_company != "natural"

    def get_repair_cost(self) -> float:
        if isinstance(self._repair_cost, (float, int)):
            return self._repair_cost
        elif isinstance(self._repair_cost, list):
            return random.choice(self._repair_cost)

    def get_daily_emissions(self) -> float:
        return self._rate * 86.4

    def natural_repair(self, emis_rep_info: EmisRepairInfo):
        self._tagged = True
        self._tagged_by_company = "natural"
        self._status = "repaired"
        emis_rep_info.leaks_nat_repaired += 1
        emis_rep_info.nat_repair_cost += self.get_repair_cost()
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
        cur_date: date,
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
    def update(self, emis_rep_info: EmisRepairInfo) -> bool:
        is_active: bool = super().update(emis_rep_info)
        if is_active:
            if self._tagged:
                self._days_since_tagged += 1
                if self.check_if_repaired(emis_rep_info):
                    is_active = False
            elif self._active_days + self._days_active_b4_sim >= self._nrd:
                self.natural_repair(emis_rep_info)
                is_active = False
        return is_active

    @override
    def get_summary_dict(self) -> dict[str, Any]:
        summary_dict: dict[str, Any] = super().get_summary_dict()
        summary_dict.update({("Date Repaired", self._repair_date)})
        summary_dict.update({("Tagged", self._tagged)})
        summary_dict.update({("Tagged By", self._tagged_by_company)})
        return summary_dict

    @override
    def activate(self, date: date) -> bool:
        if self._start_date <= date:
            self._status = "Active"
            return True
        else:
            return False
