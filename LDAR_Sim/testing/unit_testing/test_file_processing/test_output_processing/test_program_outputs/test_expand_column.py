"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_expand_column.py
Purpose: Unit tests for the function to test the expand_column function

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

import pandas as pd
from file_processing.output_processing.program_output_helpers import expand_column
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def test_001_expand_column_simp():
    # Create a list of EquipmentGroupSurveyReport instances
    data = [
        {eca.SITE_ID: 1, eca.EQG: "eqg1", eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}]},
        {eca.SITE_ID: 1, eca.EQG: "eqg2", eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}]},
        {
            eca.SITE_ID: 1,
            eca.EQG: "eqg3",
            eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}, {eca.COMP: "comp2", eca.M_RATE: 3}],
        },
    ]

    expected_df_eqg = pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1],
            eca.EQG: ["eqg1", "eqg2", "eqg3"],
            eca.COMP: [
                [{eca.COMP: "comp1", eca.M_RATE: 1}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}, {eca.COMP: "comp2", eca.M_RATE: 3}],
            ],
            eca.M_RATE: [1, 1, 1],
        }
    )
    expected_df_comp = pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1, 1],
            eca.EQG: ["eqg1", "eqg2", "eqg3", "eqg3"],
            eca.COMP: ["comp1", "comp1", "comp1", "comp2"],
            eca.M_RATE: [1, 1, 1, 3],
        }
    )
    # Create a DataFrame
    df = pd.DataFrame({eca.SITE_ID: [1], eca.M_RATE: [1], eca.EQG: [data]})
    # Call the expand_column function
    first_expanded_df = expand_column(df, eca.EQG)
    second_expanded_df = expand_column(first_expanded_df, eca.COMP)

    assert first_expanded_df.sort_index(axis=1).equals(expected_df_eqg.sort_index(axis=1))
    assert second_expanded_df.sort_index(axis=1).equals(expected_df_comp.sort_index(axis=1))


def test_001_expand_column_comp():
    # Create a list of EquipmentGroupSurveyReport instances
    data1 = [
        {eca.SITE_ID: 1, eca.EQG: "eqg1", eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}]},
        {eca.SITE_ID: 1, eca.EQG: "eqg2", eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}]},
        {
            eca.SITE_ID: 1,
            eca.EQG: "eqg3",
            eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}, {eca.COMP: "comp2", eca.M_RATE: 3}],
        },
    ]
    data2 = [
        {eca.SITE_ID: 2, eca.EQG: "eqg1", eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}]},
        {eca.SITE_ID: 2, eca.EQG: "eqg2", eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}]},
        {
            eca.SITE_ID: 2,
            eca.EQG: "eqg3",
            eca.COMP: [{eca.COMP: "comp1", eca.M_RATE: 1}, {eca.COMP: "comp2", eca.M_RATE: 3}],
        },
    ]
    expected_df_eqg = pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1, 2, 2, 2],
            eca.EQG: ["eqg1", "eqg2", "eqg3", "eqg1", "eqg2", "eqg3"],
            eca.COMP: [
                [{eca.COMP: "comp1", eca.M_RATE: 1}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}, {eca.COMP: "comp2", eca.M_RATE: 3}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}],
                [{eca.COMP: "comp1", eca.M_RATE: 1}, {eca.COMP: "comp2", eca.M_RATE: 3}],
            ],
            eca.M_RATE: [1, 1, 1, 1, 1, 1],
        }
    )
    expected_df_comp = pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2],
            eca.EQG: ["eqg1", "eqg2", "eqg3", "eqg3", "eqg1", "eqg2", "eqg3", "eqg3"],
            eca.COMP: ["comp1", "comp1", "comp1", "comp2", "comp1", "comp1", "comp1", "comp2"],
            eca.M_RATE: [1, 1, 1, 3, 1, 1, 1, 3],
        }
    )
    # Create a DataFrame
    df = pd.DataFrame({eca.SITE_ID: [1, 2], eca.M_RATE: [1, 1], eca.EQG: [data1, data2]})
    # Call the expand_column function
    first_expanded_df = expand_column(df, eca.EQG)
    second_expanded_df = expand_column(first_expanded_df, eca.COMP)

    assert first_expanded_df.sort_index(axis=1).equals(expected_df_eqg.sort_index(axis=1))
    assert second_expanded_df.sort_index(axis=1).equals(expected_df_comp.sort_index(axis=1))
