from dataclasses import dataclass


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
    "Daily Cost",
    "Active Leaks",
    "New Leaks",
    "Leaks Repaired",
    "Leaks Naturally Repaired",
    "Leaks Tagged",
    "Daily Repair Cost",
    "Daily Natural Repair Cost",
    "Daily Verification Cost",
]


class TIMESERIES_COL_ACCESSORS:
    DATE = "Date"
    EMIS = "Daily Emissions (Kg Methane)"
    COST = "Daily Cost"
    ACT_LEAKS = "Active Leaks"
    NEW_LEAKS = "New Leaks"
    REP_LEAKS = "Leaks Repaired"
    NAT_REP_LEAKS = "Leaks Naturally Repaired"
    TAGGED_LEAKS = "Leaks Tagged"
    REP_COST = "Daily Repair Cost"
    NAT_REP_COST = "Daily Natural Repair Cost"
    VERF_COST = "Daily Verification Cost"


@dataclass
class TsEmisData:
    daily_emis: float = 0
    active_leaks: int = 0
    repaired_leaks: int = 0

    def __add__(self, other):
        if isinstance(other, TsEmisData):
            daily_emis = self.daily_emis + other.daily_emis
            active_leaks = self.active_leaks + other.active_leaks
            repaired_leaks = self.repaired_leaks + other.repaired_leaks
            return TsEmisData(
                daily_emis=daily_emis, active_leaks=active_leaks, repaired_leaks=repaired_leaks
            )
        else:
            raise ValueError("Unsupported operand type for addition")

    def __iadd__(self, other):
        if isinstance(other, TsEmisData):
            self.daily_emis += other.daily_emis
            self.active_leaks += other.active_leaks
            self.repaired_leaks += other.repaired_leaks
            return self
        else:
            raise ValueError("Unsupported operand type for in-place addition")


@dataclass
class TsMethodData:
    method_name: str
    daily_cost: float = 0
