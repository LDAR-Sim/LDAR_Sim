from dataclasses import dataclass
from constants import param_default_const, output_file_constants


@dataclass
class SensitivityParameterParsingConstants:
    MISSING_SENS_FILE = "Sensitivity info file not found"
    FILE_READ_ERROR = "Error reading sensitivity info file: {filepath}"


@dataclass
class ParameterParsingConstants:
    KEY_NOT_FOUND = "Attribute {key} not found"
    TYPE_MISMATCH = "Type mismatch for attribute {key}"


@dataclass
class ParameterVariationConstants:
    METHOD_RENAMING_STR = "{method_name}_{i}"
    PROGRAM_RENAMING_STR = "{program_name}_{i}"


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
        param_default_const.Virtual_World_Params.PR,
        param_default_const.Virtual_World_Params.MAX_RATE,
        param_default_const.Virtual_World_Params.DURATION,
        param_default_const.Virtual_World_Params.MULTI_EMIS,
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


class SensitivityAnalysisOutputs:
    SENSITIVITY_TRUE_VS_ESTIMATED = "true_estimated_emissions_sensitivity_comparison"
    SENSITIVITY_TRUE_VS_ESTIMATED_PD = (
        "true_estimated_emissions_percent_difference_sensitivity_comparison"
    )
    SENSITIVITY_TRUE_VS_ESTIMATED_VIOLIN = "true_estimated_emissions_violin_sensitivity_comparison"
    SENSITIVITY_VARIATIONS_MAPPING = "sensitivity_variations_mapping"
    SENSITIVITY_TRUE_VS_ESTIMATED_CIS = (
        "true_estimated_emissions_sensitivity_comparison_confidence_intervals"
    )

    class TrueEstimatedEmisionsSens:
        FILE_NAME = "true_estimated_emissions_sensitivity_comparison"
        SENSITIVITY_SET = "Sensitivity Set"
        SIMULATION = "Simulation"
        YEAR = "Year"
        TRUE_EMISSIONS = "True Emissions"
        ESTIMATED_EMISSIONS = "Estimated Emissions"
        PERCENT_DIFFERENCE = "Percent Difference"
        COLUMNS = [
            SENSITIVITY_SET,
            SIMULATION,
            YEAR,
            TRUE_EMISSIONS,
            ESTIMATED_EMISSIONS,
        ]
        DATA_SOURCE_MAPPING = {
            SIMULATION: output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM,
        }
        YEARLY_EMIS_MATCH_REGEX = r"^Year \d+ .* Emissions \(Kg Methane\)$"
        YEAR_EXTRACTION_REGEX = r"^Year (\d+).*"

    class TrueEstimatedEmissionsPercentDiffSensPlot:
        BIN_RANGE = (0, 200)
        X_LABEL = 'Percent Difference between "Estimated" and "True" Emissions'
        Y_LABEL = "Relative Frequency (%)"
        BIN_WIDTH = 10.0

    class TrueEstimatedEmissionsViolinSensPlot:
        TRUE_EMISSIONS_LABEL = "T"
        ESTIMATED_EMISSIONS_LABEL = "E"
        X_LABEL = "Sensitivity Set"
        Y_LABEL = "Annual Emissions (Kg Methane) at all sites"
        TRUE_EMIS_LABEL = '"True" Emissions'
        ESTIMATED_EMIS_LABEL = '"Estimated" Emissions'

    class SensitivityVariationsMapping:
        FIXED_COLUMN_NAMES = ["Sensitivity Permutation"]
        FLEXIBLE_COLUMNS_NAMES = ["Parameter_{x}", "Value_{x}"]

    class SensitivityTrueVsEstimatedCIs:
        def __init__(self, upper_ci, lower_ci):
            self.lower_ci = self.LOWER_CI.format(ci=lower_ci)
            self.upper_ci = self.UPPER_CI.format(ci=upper_ci)

        UPPER_CI_ACCESSOR = "upper_confidence_interval"
        LOWER_CI_ACCESSOR = "lower_confidence_interval"
        SENSITIVITY_SET = "Sensitivity Set"
        LOWER_CI = "{ci}th Percentile Percent Difference between True and Estimated Emissions"
        UPPER_CI = "{ci}th Percentile Percent Difference between True and Estimated Emissions"
        CONFIDENCE_INTERVAL = "Confidence Interval"
        DEFAULT_UPPER_CI = 97.5
        DEFAULT_LOWER_CI = 2.5

        @property
        def COLUMNS(self):
            return [self.SENSITIVITY_SET, self.lower_ci, self.upper_ci]
