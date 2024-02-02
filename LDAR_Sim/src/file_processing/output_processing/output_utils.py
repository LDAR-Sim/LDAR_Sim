from dataclasses import dataclass
from numpy import NaN


EMIS_SUMMARY_DATA_COLS = [
    "Emissions ID",
    "Status",
    "Days Active",
    "Volume Emitted",
    "True Rate",
    "Measured Rate" "Date Began",
    "Initially Detected By",
    "Initially Detected Date",
    "Tagged",
    "Tagged By",
    "equipment",
]

EMIS_SUMMARY_FINAL_COL_ORDER = [
    "Emissions ID",
    "Site ID",
    "Equipment Group",
    "Equipment",
    "Status",
    "Days Active",
    "Date Began",
    "Date Repaired",
    "Volume Emitted",
    "True Rate",
    "Measured Rate",
    "Initially Detected By",
    "Initially Detected Date",
    "Tagged",
    "Tagged By",
]

TIMESERIES_COLUMNS = [
    "Date",
    "Daily Emissions (Kg Methane)",
    "Daily Cost ($)",
    "Active Leaks",
    "New Leaks",
    "Leaks Repaired",
    "Leaks Naturally Repaired",
    "Leaks Tagged",
    "Daily Repair Cost ($)",
    "Daily Natural Repair Cost ($)",
]


class TIMESERIES_COL_ACCESSORS:
    DATE = "Date"
    EMIS = "Daily Emissions (Kg Methane)"
    COST = "Daily Cost ($)"
    ACT_LEAKS = "Active Leaks"
    NEW_LEAKS = "New Leaks"
    REP_LEAKS = "Leaks Repaired"
    NAT_REP_LEAKS = "Leaks Naturally Repaired"
    TAGGED_LEAKS = "Leaks Tagged"
    REP_COST = "Daily Repair Cost ($)"
    NAT_REP_COST = "Daily Natural Repair Cost ($)"
    METH_DAILY_DEPLOY_COST = "{method} Deployment Cost ($)"
    METH_DAILY_TAGS = "{method} Leaks tagged for repair"
    METH_DAILY_FLAGS = "{method} Sites flagged for Follow-Up"
    METH_DAILY_SITES_VIS = "{method} Sites Visited"
    METH_DAILY_TRAVEL_TIME = "{method} Travel Time (Minutes)"
    METH_DAILY_SURVEY_TIME = "{method} Survey Time (Minutes)"


@dataclass
class TsEmisData:
    daily_emis: float = 0
    active_leaks: int = 0

    def __add__(self, other):
        if isinstance(other, TsEmisData):
            daily_emis = self.daily_emis + other.daily_emis
            active_leaks = self.active_leaks + other.active_leaks
            return TsEmisData(daily_emis=daily_emis, active_leaks=active_leaks)
        else:
            raise ValueError("Unsupported operand type for addition")

    def __iadd__(self, other):
        if isinstance(other, TsEmisData):
            self.daily_emis += other.daily_emis
            self.active_leaks += other.active_leaks
            return self
        else:
            raise ValueError("Unsupported operand type for in-place addition")


@dataclass
class TsMethodData:
    method_name: str
    daily_deployment_cost: float = 0.0
    daily_tags: int = 0
    daily_flags: int = 0
    sites_visited: int = 0
    travel_time: int = 0
    survey_time: int = 0


@dataclass
class TaggingFlaggingStats:
    sites_flagged: int = NaN
    leaks_tagged: int = NaN


@dataclass
class CrewDeploymentStats:
    deployment_cost: float = 0.0
    sites_visited: int = 0
    travel_time: int = 0
    survey_time: int = 0


@dataclass
class EmisRepairInfo:
    leaks_repaired: int = 0
    leaks_nat_repaired: int = 0
    repair_cost: int = 0
    nat_repair_cost: int = 0
