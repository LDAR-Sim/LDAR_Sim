class ProgTsConstants:
    TITLE = "{name_str} Emissions Timeseries"
    X_AXIS_TITLE = "Date"
    Y_AXIS_TITLE = "Daily Emissions (kg Methane)"
    FILENAME = "Timeseries"


TS_SUMMARY_FILENAME = "daily_summary_stats.csv"
EMIS_SUMMARY_FILENAME = "emissions_summary_stats.csv"
TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT = "True_vs_Estimated_Emissions_percent_differences.png"
TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT = "True_vs_Estimated_Emissions_relative_differences.png"
TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT = (
    "True_and_Estimated_Paired_Emissions_Distribution.png"
)
SUMMARY_PROGRAM_PLOTS_DIRECTORY = "program_summary_plots"


class ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS:
    TRUE_EMISSIONS_SUFFIX = '"True" Total Emissions (Kg Methane)'
    ESTIMATED_EMISSIONS_SUFFIX = '"Estimated" Total Emissions (Kg Methane)'


class TS_SUMMARY_COLUMNS_ACCESSORS:
    PROG_NAME = "Program Name"
    SIM = "Simulation"
    AVG_T_DAILY_EMIS = 'Average "True" Daily Emissions (Kg Methane)'
    AVG_T_MIT_DAILY_EMIS = 'Average "True" Mitigable Daily Emissions (Kg Methane)'
    AVG_T_NON_MIT_DAILY_EMIS = 'Average "True" Non-Mitigable Daily Emissions (Kg Methane)'
    T_DAILY_EMIS_95 = '95th Percentile "True" Daily Emissions (Kg Methane)'
    T_MIT_DAILY_EMIS_95 = '95th Percentile "True" Mitigable Daily Emissions (Kg Methane)'
    T_NON_MIT_DAILY_EMIS_95 = '95th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)'
    T_DAILY_EMIS_5 = '5th Percentile "True" Daily Emissions (Kg Methane)'
    T_MIT_DAILT_EMIS_5 = '5th Percentile "True" Mitigable Daily Emissions (Kg Methane)'
    T_NON_MIT_DAILY_EMIS_5 = '5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)'
    AVG_DAILY_COST = "Average Daily Cost ($)"
    DAILY_COST_95 = "95th Percentile Daily Cost ($)"
    DAILY_COST_5 = "5th Percentile Daily Cost ($)"


class EMIS_SUMMARY_COLUMNS_ACCESSORS:
    PROG_NAME = "Program Name"
    SIM = "Simulation"
    T_TOTAL_EMIS = 'Total "True" Emissions (Kg Methane)'
    EST_TOTAL_EMIS = 'Total "Estimated" Emissions (Kg Methane)'
    T_TOTAL_MIT_EMIS = 'Total "True" Mitigable Emissions (Kg Methane)'
    T_TOTAL_NON_MIT_EMIS = 'Total "True" Non-Mitigable Emissions (Kg Methane)'
    AVG_T_EMIS_RATE = 'Average "True" Emissions Rate (g/s)'
    T_EMIS_RATE_95 = '95th Percentile "True" Emissions Rate (g/s)'
    T_EMIS_RATE_5 = '5th Percentile "True" Emissions Rate (g/s)'
    T_AVG_EMIS_AMOUNT = '"True" Average Emissions Amount (Kg Methane)'
    T_EMIS_AMOUNT_95 = '95th Percentile "True" Emissions Amount (Kg Methane)'
    T_EMIS_AMOUNT_5 = '5th Percentile "True" Emissions Amount (Kg Methane)'
    EST_AVG_EMIS_AMOUNT = '"Estimated" Average Emissions Amount (Kg Methane)'
    EST_EMIS_AMOUNT_95 = '95th Percentile "Estimated" Emissions Amount (Kg Methane)'
    EST_EMIS_AMOUNT_5 = '5th Percentile "Estimated" Emissions Amount (Kg Methane)'


TS_SUMMARY_COLUMNS = [
    TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
    TS_SUMMARY_COLUMNS_ACCESSORS.SIM,
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_DAILY_EMIS,
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_MIT_DAILY_EMIS,
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_NON_MIT_DAILY_EMIS,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_95,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_MIT_DAILY_EMIS_95,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_NON_MIT_DAILY_EMIS_95,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_5,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_MIT_DAILT_EMIS_5,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_NON_MIT_DAILY_EMIS_5,
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_DAILY_COST,
    TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_95,
    TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_5,
]

EMIS_SUMMARY_COLUMNS = [
    EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_MIT_EMIS,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_NON_MIT_EMIS,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_EMIS_RATE,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_95,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_5,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_AVG_EMIS_AMOUNT,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_95,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_5,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_AVG_EMIS_AMOUNT,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_EMIS_AMOUNT_95,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_EMIS_AMOUNT_5,
]
