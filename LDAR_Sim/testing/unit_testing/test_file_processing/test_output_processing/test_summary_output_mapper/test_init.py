from constants import output_file_constants, param_default_const, file_name_constants
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper


def get_mock_output_config_data():
    output_config = {
        param_default_const.Output_Params.TIMESERIES_SUMMARY: {
            param_default_const.Output_Params.AVERAGE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.AVERAGE_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.AVERAGE_NON_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_95_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_95_MITIGABLE_DAILY_EMISSIONS: True,
            (param_default_const.Output_Params).PERCENTILE_95_NON_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_5_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_5_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.PERCENTILE_5_NON_MITIGABLE_DAILY_EMISSIONS: True,
            param_default_const.Output_Params.AVERAGE_DAILY_COST: True,
            param_default_const.Output_Params.PERCENTILE_95_DAILY_COST: True,
            param_default_const.Output_Params.PERCENTILE_5_DAILY_COST: True,
            param_default_const.Output_Params.TOTAL_COST: True,
        },
        param_default_const.Output_Params.EMISSIONS_SUMMARY: {
            param_default_const.Output_Params.EMISSIONS_SUMMARY_TOT_MITIGATION: True,
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


def test_summary_output_mapper_init():
    mock_output_config = get_mock_output_config_data()
    mock_sim_years = [2020, 2021, 2022]
    output_mapper: SummaryOutputMapper = SummaryOutputMapper(mock_output_config, mock_sim_years)
    expected_yearly_mapping_keys = [
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_MIT.format(2020),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_MIT.format(2021),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_MIT.format(2022),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2020),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2021),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2022),
    ]
    expected_emis_mapping_keys = list(
        SummaryOutputMapper.SUMMARY_MAPPINGS[
            file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
        ].keys()
    )
    expected_emis_mapping_keys.extend(expected_yearly_mapping_keys)
    expected_timeseries_mapping_keys = list(
        SummaryOutputMapper.SUMMARY_MAPPINGS[
            file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
        ].keys()
    )
    assert set(
        output_mapper.get_summary_mappings(
            file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
        ).keys()
    ) == set(expected_emis_mapping_keys)
    assert set(
        output_mapper.get_summary_mappings(
            file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
        ).keys()
    ) == set(expected_timeseries_mapping_keys)
