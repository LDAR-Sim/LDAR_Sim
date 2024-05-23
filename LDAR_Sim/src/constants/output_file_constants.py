"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        output_constants.py
Purpose: All output related constants.

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

from dataclasses import dataclass


class FileDirectory:
    SUMMARY_PROGRAM_PLOTS_DIRECTORY = "program_summary_plots"


@dataclass
class SummaryOutputVizFileNames:
    TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT = "True_vs_Estimated_Emissions_percent_differences"
    TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT = "True_vs_Estimated_Emissions_relative_differences"
    TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT = (
        "True_and_Estimated_Paired_Emissions_Distribution"
    )
    TRUE_AND_ESTIMATED_PAIRED_PROBIT_PLOT = "True and Estimated Emissions Probit"
    PROGRAM_MITIGATION_BAR_PLOT = "Program Mitigation Comparison"

    def __iter__(self):
        for attr_name, attr_value in vars(self.__class__).items():
            if not callable(attr_value) and not attr_name.startswith("__"):
                yield attr_value


@dataclass
class SummaryVisualizationSettingsMapper:
    class TrueEstimatedProbitSettings:
        SHOW_MARKERS = "Show Markers"

    MAPPINGS = {
        SummaryOutputVizFileNames.TRUE_AND_ESTIMATED_PAIRED_PROBIT_PLOT: {
            TrueEstimatedProbitSettings.SHOW_MARKERS: "show_markers"
        },
    }


@dataclass
class OutputConfigCategories:
    PROGRAM_OUTPUTS = "Program Outputs"
    SUMMARY_OUTPUTS = "Summary Outputs"
    SUMMARY_VISUALIZATIONS = "Summary Visualizations"
    SUMMARY_VISUALIZATION_SETTINGS = "Summary Visualization Settings"

    @dataclass
    class SummaryOutputCatageories:
        SUMMARY_FILES = "Summary Files"
        SUMMARY_STATS = "Summary Stats"


@dataclass
class SummaryFileColumns:
    @dataclass
    class CommonColumns:
        PROGRAM_NAME = "Program Name"
        SIMULATION_NUMBER = "Simulation"


@dataclass
class SummaryVisualizationStatistics:
    PERCENT_DIFFERENCE = "Percent Difference"
    RELATIVE_DIFFERENCE = "Relative Difference"


class PlottingConstants:
    AXIS_COLOR = "black"


class ProbitConstants:
    X_AXIS_LABEL = "Total Annual Emissions (Kg Methane) at all {n_sites} sites"
    Y_AXIS_LABEL = (
        "Probability of observing Total Annual Emissions \n at all {n_sites} sites greater than x"
    )
    TRUE_EMISSIONS_SUFFIX = '"True" Total Emissions'
    ESTIMATED_EMISSIONS_SUFFIX = '"Estimated" Total Emissions'
    Y_SCALE = "quantile"
    X_SCALE = "log"
    MARKER = "d"
    X_LABEL_SIZE = 8
    X_TICK_ROTATION = 45
    BEST_FIT_LINE_STYLE = "--"
    PLOTTING_POSITION_ALPHA = 1.0 / 3.0
    PLOTTING_POSITION_BETA = 1.0 / 3.0
    QUANTILES = [1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 99]


class MitigationBarConstants:
    Y_LABEL = "Program Name"
    X_LABEL = "Median Annual Mitigated Emissions (Kg Methane) at all sites"
    COLOR = "#0277BD"
    HEIGHT = 0.75


class HistogramConstants:
    Y_AXIS_LABEL = "Relative Frequency (%)"
    BINS = 30
    X_AXIS_LABEL_PAIRED = "Annual Emissions of All {n_sites} Sites (Kg Methane)"
    X_AXIS_LABEL_RELATIVE = "Relative Difference between Estimated and True Emissions"
    X_AXIS_LABEL_PERCENT = 'Percent Difference between "Estimated" and "True" Emissions'


class ProgTsConstants:
    TITLE = "{name_str} Emissions Timeseries"
    X_AXIS_TITLE = "Date"
    Y_AXIS_TITLE = "Daily Emissions (kg Methane)"
    FILENAME = "Timeseries"


class ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS:
    TRUE_EMISSIONS_SUFFIX = '"True" Total Emissions (Kg Methane)'
    ESTIMATED_EMISSIONS_SUFFIX = '"Estimated" Total Emissions (Kg Methane)'
    # TODO Look into ways to allow users to chose from a set of bin width options
    HISTOGRAM_BIN_WIDTH = 8.0
    HISTOGRAM_PERCENT_DIFF_BIN_RANGE = (0, 200)


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
    T_ANN_MIT = 'Year {} "True" Mitigated Emissions (Kg Methane)'
    T_ANN_EMIS = 'Year {} "True" Emissions (Kg Methane)'
    EST_ANN_EMIS = 'Year {} "Estimated" Emissions (Kg Methane)'
    REGX_T_ANN_MIT = r'Year \d+ "True" Mitigated Emissions \(Kg Methane\)'
    REGX_T_ANN_EMIS = r'Year \d+ "True" Emissions \(Kg Methane\)'
    REGX_EST_ANN_EMIS = r'Year \d+ "Estimated" Emissions \(Kg Methane\)'
    REGX_EST_FUG_ANN_EMIS = r'Year \d+ "Estimated" Fugitive Emissions \(Kg Methane\)'
    T_TOT_MIT = 'Total "True" Mitigated Emissions (Kg Methane)'
    T_TOTAL_EMIS = 'Total "True" Emissions (Kg Methane)'
    EST_TOTAL_EMIS = 'Total "Estimated" Emissions (Kg Methane)'
    T_TOTAL_MIT_EMIS = 'Total "True" Mitigable Emissions (Kg Methane)'
    T_TOTAL_NON_MIT_EMIS = 'Total "True" Non-Mitigable Emissions (Kg Methane)'
    AVG_T_EMIS_RATE = 'Average "True" Emissions Rate (g/s)'
    T_EMIS_RATE_95 = '95th Percentile "True" Emissions Rate (g/s)'
    T_EMIS_RATE_5 = '5th Percentile "True" Emissions Rate (g/s)'
    T_AVG_EMIS_AMOUNT = 'Average "True" Emissions Amount (Kg Methane)'
    T_EMIS_AMOUNT_95 = '95th Percentile "True" Emissions Amount (Kg Methane)'
    T_EMIS_AMOUNT_5 = '5th Percentile "True" Emissions Amount (Kg Methane)'


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
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOT_MIT,
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
]


class EMIS_DATA_COL_ACCESSORS:
    EMIS_ID = "Emissions ID"
    SITE_ID = "Site ID"
    EQG = "Equipment"
    STATUS = "Status"
    DAYS_ACT = "Days Active"
    EST_DAYS_ACT = "Estimated Days Active"
    T_VOL_EMIT = '"True" Volume Emitted (Kg Methane)'
    EST_VOL_EMIT = '"Estimated" Volume Emitted (Kg Methane)'
    MITIGATED = "Mitigated Emissions (Kg Methane)"
    T_RATE = '"True" Rate (g/s)'
    M_RATE = '"Measured" Rate (g/s)'
    DATE_BEG = "Date Began"
    DATE_REP_EXP = "Date Repaired or Expired"
    THEORY_DATE = "Theoretical End Date"
    INIT_DETECT_BY = "Initially Detected By"
    INIT_DETECT_DATE = "Initially Detected Date"
    TAGGED = "Tagged"
    TAGGED_BY = "Tagged By"
    FLAGGED = "Flagged"
    COMP = "Component"
    RECORDED = "Recorded"
    RECORDED_BY = "Recorded By"
    REPAIRABLE = "Repairable"
    SURVEY_LEVEL = "Survey Level"
    SURVEY_START_DATE = "Survey Start Date"
    SURVEY_COMPLETION_DATE = "Survey Completion Date"
    METHOD = "Method"
    START_DATE = "Start Date"
    END_DATE = "End Date"
    PREV_CONDITION = "Use Previous Condition"
    NEXT_CONDITION = "Use Next Condition"
    NEXT_SURVEY_DATE = "Next Survey Date"


EMIS_ESTIMATION_OUTPUT_COLUMNS = [
    EMIS_DATA_COL_ACCESSORS.SITE_ID,
    EMIS_DATA_COL_ACCESSORS.SURVEY_LEVEL,
    EMIS_DATA_COL_ACCESSORS.METHOD,
    EMIS_DATA_COL_ACCESSORS.START_DATE,
    EMIS_DATA_COL_ACCESSORS.END_DATE,
    EMIS_DATA_COL_ACCESSORS.M_RATE,
    EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
]
EST_FUG_OUTPUT_COLUMNS = [
    EMIS_DATA_COL_ACCESSORS.SITE_ID,
    EMIS_DATA_COL_ACCESSORS.M_RATE,
    EMIS_DATA_COL_ACCESSORS.START_DATE,
    EMIS_DATA_COL_ACCESSORS.END_DATE,
    EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
]

EMIS_COMP_ESTIMATION_OUTPUT_COLUMNS = [
    EMIS_DATA_COL_ACCESSORS.SITE_ID,
    EMIS_DATA_COL_ACCESSORS.EQG,
    EMIS_DATA_COL_ACCESSORS.COMP,
    EMIS_DATA_COL_ACCESSORS.SURVEY_LEVEL,
    EMIS_DATA_COL_ACCESSORS.SURVEY_COMPLETION_DATE,
    EMIS_DATA_COL_ACCESSORS.METHOD,
    EMIS_DATA_COL_ACCESSORS.START_DATE,
    EMIS_DATA_COL_ACCESSORS.END_DATE,
    EMIS_DATA_COL_ACCESSORS.M_RATE,
    EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
]

EMIS_INFO_COLUMNS_TO_KEEP_FOR_DURATION_ESTIMATION = [
    EMIS_DATA_COL_ACCESSORS.SITE_ID,
    EMIS_DATA_COL_ACCESSORS.EMIS_ID,
    EMIS_DATA_COL_ACCESSORS.DATE_REP_EXP,
    EMIS_DATA_COL_ACCESSORS.M_RATE,
]

EMIS_DATA_FINAL_COL_ORDER = [
    EMIS_DATA_COL_ACCESSORS.EMIS_ID,
    EMIS_DATA_COL_ACCESSORS.SITE_ID,
    EMIS_DATA_COL_ACCESSORS.EQG,
    EMIS_DATA_COL_ACCESSORS.COMP,
    EMIS_DATA_COL_ACCESSORS.STATUS,
    EMIS_DATA_COL_ACCESSORS.DAYS_ACT,
    EMIS_DATA_COL_ACCESSORS.EST_DAYS_ACT,
    EMIS_DATA_COL_ACCESSORS.DATE_BEG,
    EMIS_DATA_COL_ACCESSORS.DATE_REP_EXP,
    EMIS_DATA_COL_ACCESSORS.THEORY_DATE,
    EMIS_DATA_COL_ACCESSORS.MITIGATED,
    EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
    EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
    EMIS_DATA_COL_ACCESSORS.T_RATE,
    EMIS_DATA_COL_ACCESSORS.M_RATE,
    EMIS_DATA_COL_ACCESSORS.INIT_DETECT_BY,
    EMIS_DATA_COL_ACCESSORS.INIT_DETECT_DATE,
    EMIS_DATA_COL_ACCESSORS.TAGGED,
    EMIS_DATA_COL_ACCESSORS.TAGGED_BY,
    EMIS_DATA_COL_ACCESSORS.RECORDED,
    EMIS_DATA_COL_ACCESSORS.RECORDED_BY,
    EMIS_DATA_COL_ACCESSORS.REPAIRABLE,
]

TIMESERIES_COLUMNS = [
    "Date",
    "Daily Emissions (Kg Methane)",
    "Daily Mitigable Emissions (Kg Methane)",
    "Daily Non-Mitigable Emissions (Kg Methane)",
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
    EMIS_MIT = "Daily Mitigable Emissions (Kg Methane)"
    EMIS_NON_MIT = "Daily Non-Mitigable Emissions (Kg Methane)"
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
