import copy
from constants import param_default_const, file_name_constants
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper


def mock_summary_mapping_init(self):
    self.summary_mapping = {}


def get_mock_output_config_data():
    output_config = {
        param_default_const.Output_Params.TIMESERIES_SUMMARY: {
            param_default_const.Output_Params.AVERAGE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.AVERAGE_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.AVERAGE_NON_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_95_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_95_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_95_NON_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_5_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_5_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_5_NON_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.AVERAGE_DAILY_COST: True,
            param_default_const.Output_Params.PERCENTILE_95_DAILY_COST: True,
            param_default_const.Output_Params.PERCENTILE_5_DAILY_COST: True,
        },
        param_default_const.Output_Params.EMISSIONS_SUMMARY: {
            param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_TRUE: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_ESTIMATED: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_MITIGABLE: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_NON_MITIGABLE: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_AVERAGE_RATE: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_95_RATE: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_5_RATE: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_AVERAGE_AMOUNT: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_95_AMOUNT: True,
            param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_5_AMOUNT: True,
        },
    }
    return output_config


def test_set_summary_mapping_sets_correct_mapping_for_timeseries_summary(mocker):
    summary_file = file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    expected_mapping = SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file]
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping


def test_set_summary_mapping_sets_correct_mapping_for_emissions_summary(mocker):
    summary_file = file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    expected_mapping = SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file]
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping


def test_set_summary_mapping_sets_correct_mapping_for_timeseries_summary_not_all_mappings(mocker):
    summary_file = file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    output_config['5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)'] = False
    expected_mapping = copy.deepcopy(SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file])
    expected_mapping.pop('5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)')
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping


def test_set_summary_mapping_sets_correct_mapping_for_emissions_summary_not_all_mappings(mocker):
    summary_file = file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    output_config['Total "True" Emissions (Kg Methane)'] = False
    expected_mapping = copy.deepcopy(SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file])
    expected_mapping.pop('Total "True" Emissions (Kg Methane)')
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping
