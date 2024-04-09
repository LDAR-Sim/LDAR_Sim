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


class Common_Params:
    VERSION = "version"
    PARAM_LEVEL = "parameter_level"
    VAL = "vals"
    FILE = "file"
    METH_SPECIFIC = "Method_Specific_Params"


class Levels:
    SIMULATION = "simulation_settings"
    VIRTUAL = "virtual_world"
    PROGRAM = "programs"
    METHOD = "methods"


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


class Sim_Setting_Params:
    INPUT = "input_directory"
    OUTPUT = "output_directory"
    BASELINE = "baseline_program"
    REFERENCE = "reference_program"
    PROCESS = "n_processes"
    SIMS = "n_simulations"
    PRESEED = "preseed_random"
    OUTPUTS = "outputs"
    SITE_VISITS = "site_visits"
    LEAKS = "leaks"
    SITES = "sites"
    TIMESERIES = "timeseries"
    PLOTS = "plots"
    BATCH_REPORTING = "batch_reporting"
    MAKE_PLOTS = "make_plots"
    WRITE_DATA = "write_data"


class Program_Params:
    NAME = "program_name"
    METHODS = "method_labels"
    ECONOMICS = "economics"
    TCO2E = "carbon_price_tonnesCO2e"
    CCUS = "cost_CCUS"
    GWP = "GWP_CH4"
    NATGAS = "sale_price_natgas"
    VERIFICATION = "verification_cost"


class Method_Params:
    NAME = "label"
    MEASUREMENT_SCALE = "measurement_scale"
    DEPLOYMENT_TYPE = "deployment_type"
    SENSOR = "sensor"
    TYPE = "type"
    QE = "QE"
    MDL = "MDL"
    MOD_LOC = "mod_loc"
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
    LDAR_CREW_INIT_LOCATION = "LDAR_crew_init_location"
    HOME_BASES_FILES = "home_bases_files"
    ROUTE_PLANNING = "route_planning"
    TRAVEL_SPEEDS = "travel_speeds"
    MIN_TIME_BT_SURVEYS = "min_time_bt_surveys"
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
    MIN_FOLLOWUPS = "min_followups"
    MIN_FOLLOWUP_TYPE = "min_followup_type"
    MIN_FOLLOWUP_DAYS_TO_END = "min_followup_days_to_end"
    PROPORTION = "proportion"
    REDUNDANCY_FILTER = "redundancy_filter"
    SORT_BY_RATE = "sort_by_rate"
    THRESHOLD = "threshold"
    THRESHOLD_TYPE = "threshold_type"
