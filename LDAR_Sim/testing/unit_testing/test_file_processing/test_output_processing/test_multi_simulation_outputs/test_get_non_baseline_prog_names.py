import pandas as pd
from src.file_processing.output_processing.multi_simulation_visualizations import (
    get_non_baseline_prog_names,
)
from src.constants import output_file_constants


def test_get_non_baseline_prog_names():
    # Define a sample DataFrame
    emis_summary_info = pd.DataFrame(
        {
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME: [
                "prog1",
                "prog2",
                "prog3",
                "prog4",
                "prog5",
                "prog6",
            ],
            "other_column": [1, 2, 3, 4, 5, 6],
        }
    )

    # Define the baseline program
    baseline_program = "prog1"

    # Call the function with the test data
    result = get_non_baseline_prog_names(emis_summary_info, baseline_program)

    # Define the expected result
    expected_result = ["prog2", "prog3", "prog4", "prog5", "prog6"]

    # Assert that the function output is as expected
    assert result == expected_result
