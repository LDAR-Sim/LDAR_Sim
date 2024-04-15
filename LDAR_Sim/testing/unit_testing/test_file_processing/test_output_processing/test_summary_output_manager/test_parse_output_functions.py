from file_processing.output_processing.summary_output_manager import SummaryOutputManager
from constants import output_file_constants


def mock_summary_output_manager_init(self):
    return


def get_mock_output_config():
    return {
        output_file_constants.SummaryFileNames.TS_SUMMARY: True,
        output_file_constants.SummaryFileNames.EMIS_SUMMARY: True,
    }


def test_parse_output_functions_returns_expected_all_outputs_wanted(mocker):
    mocker.patch.object(SummaryOutputManager, "__init__", mock_summary_output_manager_init)
    output_manager: SummaryOutputManager = SummaryOutputManager()
    expected_outputs = [
        output_file_constants.SummaryFileNames.TS_SUMMARY,
        output_file_constants.SummaryFileNames.EMIS_SUMMARY,
    ]
    outputs_to_make: list[str] = output_manager.parse_output_functions(get_mock_output_config())
    assert outputs_to_make == expected_outputs


def test_parse_output_functions_returns_expected_some_outputs_wanted(mocker):
    mocker.patch.object(SummaryOutputManager, "__init__", mock_summary_output_manager_init)
    output_manager: SummaryOutputManager = SummaryOutputManager()
    output_config = {
        output_file_constants.SummaryFileNames.TS_SUMMARY: False,
        output_file_constants.SummaryFileNames.EMIS_SUMMARY: True,
    }
    expected_outputs = [output_file_constants.SummaryFileNames.EMIS_SUMMARY]
    outputs_to_make: list[str] = output_manager.parse_output_functions(output_config)
    assert outputs_to_make == expected_outputs
