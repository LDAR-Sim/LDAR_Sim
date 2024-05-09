from dataclasses import dataclass
from constants import param_default_const


@dataclass
class ValidParametersForSensitivityAnalysis:
    VIRTUAL_WORLD = [
        param_default_const.Virtual_World_Params.WEATHER_FILE,
        param_default_const.Virtual_World_Params.CONSIDER_WEATHER,
        param_default_const.Virtual_World_Params.SITE_TYPE,
        param_default_const.Virtual_World_Params.SITE,
        param_default_const.Virtual_World_Params.EQUIP,
        param_default_const.Virtual_World_Params.SOURCE,
        param_default_const.Virtual_World_Params.REPAIR_COST,
        param_default_const.Virtual_World_Params.REPAIR_DELAY,
        param_default_const.Virtual_World_Params.EMIS_FILE,
        param_default_const.Virtual_World_Params.ERS,
        param_default_const.Virtual_World_Params.LPR,
        param_default_const.Virtual_World_Params.NR_ERS,
        param_default_const.Virtual_World_Params.NR_EPR,
        param_default_const.Virtual_World_Params.MAX_RATE,
        param_default_const.Virtual_World_Params.NRD,
        param_default_const.Virtual_World_Params.DURATION,
        param_default_const.Virtual_World_Params.MULTI_EMIS,
        param_default_const.Virtual_World_Params.MULTI_EMIS_NR,
    ]
    PROGRAMS = [
        param_default_const.Program_Params.TCO2E,
        param_default_const.Program_Params.GWP,
        param_default_const.Program_Params.NATGAS,
        param_default_const.Program_Params.VERIFICATION,
    ]
    METHODS = [
        param_default_const.Method_Params.SENSOR,
        param_default_const.Method_Params.COVERAGE,
        param_default_const.Method_Params.COST,
        param_default_const.Method_Params.N_CREWS,
        param_default_const.Method_Params.CONSIDER_DAYLIGHT,
        param_default_const.Method_Params.RS,
        param_default_const.Method_Params.TIME,
        param_default_const.Method_Params.MAX_WORKDAY,
        param_default_const.Method_Params.SCHEDULING,
        param_default_const.Method_Params.T_BW_SITES,
        param_default_const.Method_Params.WEATHER_ENVS,
        param_default_const.Method_Params.FOLLOW_UP,
    ]


class SensitivityAnalysisMapping:
    SENS_PARAM_LEVEL = "Sensitivity Parameter Level"
    SENS_PERMUTATIONS = "Sensitivity Analysis Permutations"
    METHOD_NAME = "Method Name"
    Method_SENS_PARAMS = "Method Sensitivity Parameters"
    PROGRAM_NAME = "Program Name"
    PROGRAM_SENS_PARAMS = "Program Sensitivity Parameters"
    SENS_PARAM_VARIATIONS = "Sensitivity Parameter Variations"
    PARAM_VARIATIONS = "parameter_variations"
    PARAM_LEVEL = "parameter_level"
    NUM_VARIATIONS = "number_of_variations"
    SENS_SUMMARY_INFO = "Sensitivity Summary Outputs Information"
    SENS_PARAM_MAPPING = {
        SENS_PARAM_LEVEL: PARAM_LEVEL,
        SENS_PERMUTATIONS: NUM_VARIATIONS,
        SENS_PARAM_VARIATIONS: PARAM_VARIATIONS,
        SENS_SUMMARY_INFO: SENS_SUMMARY_INFO,
    }
