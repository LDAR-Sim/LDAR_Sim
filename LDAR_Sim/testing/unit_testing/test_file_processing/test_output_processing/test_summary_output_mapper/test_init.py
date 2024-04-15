from constants import output_file_constants
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper


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


def test_summary_output_mapper_init():
    mock_output_config = get_mock_output_config_data()
    mock_sim_years = [2020, 2021, 2022]
    output_mapper: SummaryOutputMapper = SummaryOutputMapper(mock_output_config, mock_sim_years)
    expected_yearly_mapping_keys = [
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2020),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2020),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2021),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2021),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2022),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2022),
    ]
    expected_emis_mapping_keys = list(
        SummaryOutputMapper.SUMMARY_MAPPINGS[
            output_file_constants.SummaryFileNames.EMIS_SUMMARY
        ].keys()
    )
    expected_emis_mapping_keys.extend(expected_yearly_mapping_keys)
    expected_timeseries_mapping_keys = list(
        SummaryOutputMapper.SUMMARY_MAPPINGS[
            output_file_constants.SummaryFileNames.TS_SUMMARY
        ].keys()
    )
    assert set(
        output_mapper.get_summary_mappings(
            output_file_constants.SummaryFileNames.EMIS_SUMMARY
        ).keys()
    ) == set(expected_emis_mapping_keys)
    assert set(
        output_mapper.get_summary_mappings(output_file_constants.SummaryFileNames.TS_SUMMARY).keys()
    ) == set(expected_timeseries_mapping_keys)
