import pandas as pd
from constants import output_file_constants
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper


def mock_summary_mapping_init(self):
    self.summary_mapping = {}


def test_add_yearly_mappings_set_expected_mappings(mocker):
    summary_file = output_file_constants.SummaryFileNames.EMIS_SUMMARY
    simulation_years = [2017, 2018, 2019]
    expected_keys = [
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2017),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2017),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2018),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2018),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2019),
        output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2019),
    ]
    mocker.patch.object(SummaryOutputMapper, "__init__", mock_summary_mapping_init)
    output_mapper: SummaryOutputMapper = SummaryOutputMapper()
    output_mapper.add_yearly_mappings(summary_file, simulation_years)
    assert set(output_mapper.get_summary_mappings(summary_file).keys()) == set(expected_keys)
    fake_date = pd.DataFrame()
    for func in output_mapper.get_summary_mappings(summary_file).values():
        assert func(fake_date) == 0
