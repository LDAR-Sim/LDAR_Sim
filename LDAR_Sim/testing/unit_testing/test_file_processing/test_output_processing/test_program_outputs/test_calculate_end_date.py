from file_processing.output_processing.program_output_helpers import calculate_end_date
import pandas as pd
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def test_calculate_end_date():
    # Create a mock DataFrame for row
    sorted_by_site_summary = pd.DataFrame(
        {
            eca.PREV_CONDITION: [True, False, False, True, True],
            eca.NEXT_CONDITION: [True, True, False, False, False],
            eca.SURVEY_COMPLETION_DATE: pd.date_range(start="1/1/2022", periods=5),
        }
    )
    expected = pd.Series(
        [
            pd.Timestamp("2022-01-01"),
            pd.Timestamp("2022-01-02"),
            pd.Timestamp("2022-01-04"),
            pd.Timestamp("2022-01-05"),
            pd.Timestamp("2022-01-05"),
        ]
    )
    # Test when both conditions are True
    result = calculate_end_date(sorted_by_site_summary)
    pd.testing.assert_series_equal(expected, result)
