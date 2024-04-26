from file_processing.output_processing.program_output_helpers import calculate_start_date
import pandas as pd
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def test_calculate_start_date():
    # Create a mock DataFrame for row
    sorted_by_site_summary = pd.DataFrame(
        {
            eca.PREV_CONDITION: [False, False, False, True, True],
            eca.SURVEY_COMPLETION_DATE: pd.date_range(start="1/1/2022", periods=5),
        }
    )

    # Test for proper start date generation
    expected_result = pd.Series(
        [
            pd.Timestamp("2022-01-01"),
            pd.Timestamp("2022-01-01"),
            pd.Timestamp("2022-01-02"),
            pd.Timestamp("2022-01-04"),
            pd.Timestamp("2022-01-05"),
        ]
    )
    actual_result = calculate_start_date(sorted_by_site_summary)
    pd.testing.assert_series_equal(actual_result, expected_result)
