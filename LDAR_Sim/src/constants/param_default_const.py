"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        param_default_const.py
Purpose: To contain constants that are used to represent the default parameters.

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


@dataclass
class Common_Params:
    VERSION = "version"
    PARAM_LEVEL = "parameter_level"
    VAL = "vals"
    FILE = "file"
    METH_SPECIFIC = "Method_Specific_Params"


@dataclass
class Levels:
    SIMULATION = "simulation_settings"
    VIRTUAL = "virtual_world"
    PROGRAM = "programs"
    METHOD = "methods"
    OUTPUTS = "outputs"

    SITE_LEVEL = "site_level"
    EQUIP_LEVEL = "equipment_level"
    COMPONENT_LEVEL = "component_level"


@dataclass
class Deployment_Types:
    MOBILE = "mobile"
    STATIONARY = "stationary"
    ORBIT = "orbital"


@dataclass
class Duration_Method:
    COMPONENT = "component-based"
    MEASUREMENT_CONSERVATIVE = "measurement-based-conservative"


@dataclass
class Virtual_World_Params:
    START_DATE = "start_date"
    END_DATE = "end_date"
    WEATHER_FILE = "weather_file"
    CONSIDER_WEATHER = "consider_weather"
    INFRA = "infrastructure"
    SITE_TYPE = "site_type_file"
    SITE = "sites_file"
    EQUIP = "equipment_group_file"
    SOURCE = "sources_file"
    N_SITES = "site_samples"
    REPAIR = "repairs"
    COST = "cost"
    DELAY = "delay"
    EMISS = "emissions"
    EMISS_FILE = "emissions_file"
    ERS = "ERS"
    LPR = "LPR"
    NR_ERS = "NR_ERS"
    NR_EPR = "NR_EPR"
    MAX_RATE = "max_leak_rate"
    UNITS = "units"
    NRD = "NRd"
    DURATION = "duration"


@dataclass
class Sim_Setting_Params:
    INPUT = "input_directory"
    OUTPUT = "output_directory"
    BASELINE = "baseline_program"
    REFERENCE = "reference_program"
    PROCESS = "n_processes"
    SIMS = "n_simulations"
    PRESEED = "preseed_random"


@dataclass
class Program_Params:
    NAME = "program_name"
    METHODS = "method_labels"
    ECONOMICS = "economics"
    TCO2E = "carbon_price_tonnesCO2e"
    GWP = "GWP_CH4"
    NATGAS = "sale_price_natgas"
    VERIFICATION = "verification_cost"
    DURATION_ESTIMATE = "duration_estimate"
    DURATION_FACTOR = "duration_factor"
    DURATION_METHOD = "duration_method"


@dataclass
class Method_Params:
    NAME = "label"
    MEASUREMENT_SCALE = "measurement_scale"
    DEPLOYMENT_TYPE = "deployment_type"
    SENSOR = "sensor"
    TYPE = "type"
    QE = "QE"
    MDL = "MDL"
    COVERAGE = "coverage"
    SPATIAL = "spatial"
    TEMPORAL = "temporal"
    COST = "cost"
    PER_DAY = "per_day"
    PER_SITE = "per_site"
    UPFRONT = "upfront"
    N_CREWS = "n_crews"
    CONSIDER_DAYLIGHT = "consider_daylight"
    RS = "RS"
    TIME = "time"
    MAX_WORKDAY = "max_workday"
    REPORTING_DELAY = "reporting_delay"
    T_BW_SITES = "t_bw_sites"
    SCHEDULING = "scheduling"
    DEPLOYMENT_MONTHS = "deployment_months"
    DEPLOYMENT_YEARS = "deployment_years"
    WEATHER_ENVS = "weather_envs"
    PRECIP = "precip"
    TEMP = "temp"
    WIND = "wind"
    IS_FOLLOW_UP = "is_follow_up"
    FOLLOW_UP = "follow_up"
    PREFERRED_METHOD = "preferred_method"
    DELAY = "delay"
    INSTANT_THRESHOLD = "instant_threshold"
    INSTANT_THRESHOLD_TYPE = "instant_threshold_type"
    INTERACTION_PRIORITY = "interaction_priority"
    PROPORTION = "proportion"
    REDUNDANCY_FILTER = "redundancy_filter"
    SORT_BY_RATE = "sort_by_rate"
    THRESHOLD = "threshold"


@dataclass
class Output_Params:
    PROGRAM_OUTPUTS = "Program Outputs"
    PROGRAM_EMISSIONS = "Program Emissions"
    PROGRAM_TIMESERIES = "Program Timeseries"
    SUMMARY_OUTPUTS = "Summary Outputs"
    SUMMARY_OUTPUT_SETTINGS = "Summary Output Settings"
    SUMMARY_FILES = "Summary Files"
    TIMESERIES_SUMMARY = "Timeseries Summary"
    EMISSIONS_SUMMARY = "Emissions Summary"
    SUMMARY_STATS = "Summary Stats"
    AVERAGE_DAILY_EMISSIONS = 'Average "True" Daily Emissions (Kg Methane)'
    AVERAGE_MITIGABLE_DAILY_EMISSIONS = 'Average "True" Mitigable Daily Emissions (Kg Methane)'
    AVERAGE_NON_MITIGABLE_DAILY_EMISSIONS = (
        'Average "True" Non-Mitigable Daily Emissions (Kg Methane)'
    )
    PERCENTILE_95_DAILY_EMISSIONS = '95th Percentile "True" Daily Emissions (Kg Methane)'
    PERCENTILE_95_MITIGABLE_DAILY_EMISSIONS = (
        '95th Percentile "True" Mitigable Daily Emissions (Kg Methane)'
    )
    PERCENTILE_95_NON_MITIGABLE_DAILY_EMISSIONS = (
        '95th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)'
    )
    PERCENTILE_5_DAILY_EMISSIONS = '5th Percentile "True" Daily Emissions (Kg Methane)'
    PERCENTILE_5_MITIGABLE_DAILY_EMISSIONS = (
        '5th Percentile "True" Mitigable Daily Emissions (Kg Methane)'
    )
    PERCENTILE_5_NON_MITIGABLE_DAILY_EMISSIONS = (
        '5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)'
    )
    AVERAGE_DAILY_COST = "Average Daily Cost ($)"
    PERCENTILE_95_DAILY_COST = "95th Percentile Daily Cost ($)"
    PERCENTILE_5_DAILY_COST = "5th Percentile Daily Cost ($)"
    EMISSIONS_SUMMARY_TOTAL_TRUE = 'Total "True" Emissions (Kg Methane)'
    EMISSIONS_SUMMARY_TOTAL_ESTIMATED = 'Total "Estimated" Emissions (Kg Methane)'
    EMISSIONS_SUMMARY_TOTAL_MITIGABLE = 'Total "True" Mitigable Emissions (Kg Methane)'
    EMISSIONS_SUMMARY_TOTAL_NON_MITIGABLE = 'Total "True" Non-Mitigable Emissions (Kg Methane)'
    EMISSIONS_SUMMARY_AVERAGE_RATE = 'Average "True" Emissions Rate (g/s)'
    EMISSIONS_SUMMARY_PERCENTILE_95_RATE = '95th Percentile "True" Emissions Rate (g/s)'
    EMISSIONS_SUMMARY_PERCENTILE_5_RATE = '5th Percentile "True" Emissions Rate (g/s)'
    EMISSIONS_SUMMARY_AVERAGE_AMOUNT = 'Average "True" Emissions Amount (Kg Methane)'
    EMISSIONS_SUMMARY_PERCENTILE_95_AMOUNT = '95th Percentile "True" Emissions Amount (Kg Methane)'
    EMISSIONS_SUMMARY_PERCENTILE_5_AMOUNT = '5th Percentile "True" Emissions Amount (Kg Methane)'
    SHOW_MARKERS = "Show Markers"