import copy
from constants import output_file_constants
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper


def mock_summary_mapping_init(self):
    self.summary_mapping = {}


def get_mock_output_config_data():
    output_config = {
        "Timeseries Summary": {
            'Average "True" Daily Emissions (Kg Methane)': True,
            'Average "True" Mitigable Daily Emissions (Kg Methane)': True,
            'Average "True" Non-Mitigable Daily Emissions (Kg Methane)': True,
            '95th Percentile "True" Daily Emissions (Kg Methane)': True,
            '95th Percentile "True" Mitigable Daily Emissions (Kg Methane)': True,
            '95th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)': True,
            '5th Percentile "True" Daily Emissions (Kg Methane)': True,
            '5th Percentile "True" Mitigable Daily Emissions (Kg Methane)': True,
            '5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)': True,
            "Average Daily Cost ($)": True,
            "95th Percentile Daily Cost ($)": True,
            "5th Percentile Daily Cost ($)": True,
        },
        "Emissions Summary": {
            'Total "True" Emissions (Kg Methane)': True,
            'Total "Estimated" Emissions (Kg Methane)': True,
            'Total "True" Mitigable Emissions (Kg Methane)': True,
            'Total "True" Non-Mitigable Emissions (Kg Methane)': True,
            'Average "True" Emissions Rate (g/s)': True,
            '95th Percentile "True" Emissions Rate (g/s)': True,
            '5th Percentile "True" Emissions Rate (g/s)': True,
            'Average "True" Emissions Amount (Kg Methane)': True,
            '95th Percentile "True" Emissions Amount (Kg Methane)': True,
            '5th Percentile "True" Emissions Amount (Kg Methane)': True,
        },
    }
    return output_config


def test_set_summary_mapping_sets_correct_mapping_for_timeseries_summary(mocker):
    summary_file = output_file_constants.SummaryFileNames.TS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    expected_mapping = SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file]
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping


def test_set_summary_mapping_sets_correct_mapping_for_emissions_summary(mocker):
    summary_file = output_file_constants.SummaryFileNames.EMIS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    expected_mapping = SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file]
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping


def test_set_summary_mapping_sets_correct_mapping_for_timeseries_summary_not_all_mappings(mocker):
    summary_file = output_file_constants.SummaryFileNames.TS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    output_config['5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)'] = False
    expected_mapping = copy.deepcopy(SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file])
    expected_mapping.pop('5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)')
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping


def test_set_summary_mapping_sets_correct_mapping_for_emissions_summary_not_all_mappings(mocker):
    summary_file = output_file_constants.SummaryFileNames.EMIS_SUMMARY
    output_config = get_mock_output_config_data()[summary_file]
    output_config['Total "True" Emissions (Kg Methane)'] = False
    expected_mapping = copy.deepcopy(SummaryOutputMapper.SUMMARY_MAPPINGS[summary_file])
    expected_mapping.pop('Total "True" Emissions (Kg Methane)')
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.set_summary_mapping(summary_file, output_config)
    assert output_mapper.get_summary_mappings(summary_file) == expected_mapping
