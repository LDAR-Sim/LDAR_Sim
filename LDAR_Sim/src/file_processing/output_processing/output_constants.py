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
