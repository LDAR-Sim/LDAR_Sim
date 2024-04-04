import pandas as pd
import numpy as np
import pytest
from src.file_processing.output_processing.multi_simulation_visualizations import (
    gen_annual_emissions_summary_list,
)
from LDAR_Sim.src.constants import output_constants


def test_gen_annual_emissions_summary_list_one_year():
    # Define a sample DataFrame
    emis_summary_info = pd.DataFrame(
        {
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME: [
                "prog1",
                "prog2",
            ],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2020): [
                1,
                2,
            ],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2020): [
                9,
                10,
            ],
        }
    )

    # Define the program names
    program_names = ["prog1", "prog2"]

    # Call the function with the test data
    result = gen_annual_emissions_summary_list(emis_summary_info, program_names)

    # Define the expected result
    expected_result = {
        "prog1": ([1], [9]),
        "prog2": ([2], [10]),
    }

    # Assert that the function output is as expected
    assert result == expected_result


def test_gen_annual_emissions_summary_list_multi_years():
    # Define a sample DataFrame
    emis_summary_info = pd.DataFrame(
        {
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME: [
                "prog1",
                "prog2",
                "prog3",
                "prog4",
            ],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2020): [1, 2, 3, 4],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2021): [5, 6, 7, 8],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2022): [5, 6, 7, 8],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2020): [
                9,
                10,
                11,
                12,
            ],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2021): [
                13,
                14,
                15,
                16,
            ],
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2022): [
                13,
                14,
                15,
                16,
            ],
        }
    )

    # Define the program names
    program_names = ["prog1", "prog2", "prog3", "prog4"]

    # Call the function with the test data
    result = gen_annual_emissions_summary_list(emis_summary_info, program_names)

    # Define the expected result
    expected_result = {
        "prog1": ([5, 5], [13, 13]),
        "prog2": ([6, 6], [14, 14]),
        "prog3": ([7, 7], [15, 15]),
        "prog4": ([8, 8], [16, 16]),
    }

    # Assert that the function output is as expected
    assert result == expected_result
