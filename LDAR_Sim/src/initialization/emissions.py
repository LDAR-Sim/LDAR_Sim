import datetime
from math import floor
from typing import Any
from typing_extensions import override
from numpy.random import binomial


class Emission:
    def __init__(
        self,
        emission_n,
        site_id,
        rate,
        start_date,
        simulation_sd,
        repairable,
        equipment_group,
        source_id
    ):
        self._emissions_id: str = f'{site_id}_{str(emission_n).zfill(10)}' if source_id is None\
            else f'{site_id}_{source_id}_{str(emission_n).zfill(10)}'
        self._site_id: str = site_id
        self._source_id: str = source_id
        self._rate: float = rate
        self._start_date: datetime = start_date
        self._repairable: bool = repairable
        self._equipment_group: int = equipment_group

        self._estimate_date_began: datetime = None
        self._estimated_days_active: int = 0
        self._active_days: int = 0
        self._measured_rate: float = None
        self._tagged: bool = False
        self._days_since_tagged: int = 0
        self._tagged_by_company: str = None
        self._tagged_by_crew: str = None
        self._flagged_by: str = None
        self._init_detect_by: str = None
        self._init_detect_date: datetime = None
        self._tech_spat_covs: dict[str, int] = {}

        if simulation_sd >= start_date:
            self._status = 'Active'
        else:
            self._status = 'Inactive'

    def update_emissions(self):
        """
        Increments duration values
        """
        if self._status == "Active":
            self._active_days += 1

        if self._tagged:
            self._days_since_tagged += 1

    def check_spatial_cov(self, method, cov) -> int:
        if method not in self._tech_spat_covs:
            self._tech_spat_covs[method] = binomial(1, cov)
        return self._tech_spat_covs[method]

    def get_emis_vol(self) -> float:
        return (self._active_days * self._rate * 86.4)

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
    def __init__(self, emission_n, site_id, rate, start_date, simulation_sd,
                 repairable, source_id):
        super().__init__(
            emission_n,
            site_id,
            rate,
            start_date,
            simulation_sd,
            repairable,
            source_id,
        )


class FugitiveEmission(Emission):

    def __init__(
        self,
        emission_n,
        site_id,
        rate,
        start_date,
        simulation_sd,
        repairable,
        equipment_group,
        repair_delay,
        repair_cost,
        nrd,
        source_id=None
    ):
        super().__init__(
            emission_n,
            site_id,
            rate,
            start_date,
            simulation_sd,
            repairable,
            equipment_group,
            source_id
        )
        self._repair_delay: int = repair_delay
        self._repair_cost: float = repair_cost
        self._tagging_rep_delay: int = 0
        self._nrd = nrd
        self._repair_date = None
        days_active_b4_sim = (simulation_sd - start_date).days
        self._days_active_b4_sim = days_active_b4_sim if days_active_b4_sim > 0 else 0

    def check_if_repaired(self):
        """
        Checks the days since tagged against the repair delay
        Repairs the emission if possible
        """
        if self._repairable:
            if self._days_since_tagged >= self._repair_delay + self._tagging_rep_delay:
                self._status = 'repaired'
                self._repair_date = self._start_date + datetime.timedelta(days=(self._active_days))

    def get_init_detect_company(self):
        return self._init_detect_by

    def tagged_today(self) -> bool:
        return (
            (self._tagged and
                (self._days_since_tagged == 0)
             ) and self._tagged_by_company != 'natural'
        )

    def update_detection_records(self, company, detect_date):
        if self._init_detect_by is None:
            self._init_detect_by = company
            self._init_detect_date = detect_date

    def get_repair_cost(self) -> float:
        return self._repair_cost

    def get_daily_emissions(self) -> float:
        return (self._rate * 86.4)

    def natural_repair(self):
        self._tagged = True
        self._tagged_by_company = 'natural'
        self._status = 'repaired'
        self._repair_date = self._start_date + datetime.timedelta(days=(self._active_days))

    # TODO potentially move this into company later
    def estimate_start_date(self, cur_ts, t_since_ldar):
        self._estimated_date_began = floor(cur_ts - (t_since_ldar / 2))

    def tag_leak(
            self,
            measured_rate,
            cur_ts,
            t_since_ldar,
            company,
            crew_id,
            tagging_rep_delay
    ):
        """ Attempts to tag a leak. If a leak is not tagged
            This function will tag. If it is already tagged, the
            function will return false.

        Args:
            measured_rate (int): Rate of leak in g/s
            est_start_date (int): estimated time series start date of the leak
            company (str): Company responsible for detecting leak
            crew_id (int, optional): [int]. Defaults to 1. crew responsible for detecting

        Returns:
            [bool]: Is the leak new?
        """
        if self._tagged:
            return False

        # Add these leaks to the 'tag pool'
        self._tagged = True

        self._measured_rate = measured_rate
        self.estimate_start_date(cur_ts, t_since_ldar)

        self._tagged_by_company = company
        self._tagged_by_crew = crew_id
        self._tagging_rep_delay = tagging_rep_delay
        return True

    @override
    def update_emissions(self):
        super().update_emissions()
        if self._active_days + self._days_active_b4_sim >= self._nrd:
            self.natural_repair()
            return "nat_repaired"
        if self._tagged:
            self.check_if_repaired()
            return "repaired"
        return "no_status_change"

    def get_equip_grp(self) -> int:
        return self._equipment_group

    @override
    def get_summary_dict(self) -> dict[str, Any]:
        summary_dict: dict[str, Any] = super().get_summary_dict()
        summary_dict.update({("Date Repaired", self._repair_date)})
        return summary_dict

    def activate(self) -> None:
        self._status = "Active"
