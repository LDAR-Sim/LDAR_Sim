"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        prog_method_measured_func.py
Purpose: To contain functions to produce program-method measured true/false 
data frames

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
from constants.infrastructure_const import Deployment_TF_Sites_Constants as DTSC


def set_up_tf_method_deployed_df(methods: dict[str, dict], site_count) -> pd.DataFrame:
    """
    Input:
    methods: dict[str, dict] - dictionary of methods and their parameters
    site_count: int - number of sites in the virtual world

    Returns:
    pd.DataFrame - a null filled dataframe with the columns for the true/false site list
    """
    column_names = [DTSC.SITE_ID, DTSC.SITE_TYPE] + [
        item
        for method in methods.keys()
        for item in [
            DTSC.REQUIRED_SURVEY.format(method=method),
            DTSC.SITE_DEPLOYMENT.format(method=method),
            DTSC.METHOD_MEASURED.format(method=method),
        ]
    ]

    return pd.DataFrame(index=range(site_count), columns=column_names)


def filter_deployment_tf_by_program_methods(
    tf_df_ori: pd.DataFrame, methods: list[str]
) -> pd.DataFrame:
    """
    Input:
    tf_df_ori: pd.DataFrame - the original true/false site list dataframe
    methods: list[str] - list of methods to filter the dataframe

    Returns:
    pd.DataFrame - a filtered dataframe with the columns for the true/false
    """
    formatted_method_columns = [DTSC.METHOD_MEASURED.format(method=method) for method in methods]
    columns = [DTSC.SITE_ID, DTSC.SITE_TYPE] + formatted_method_columns
    filtered_df = tf_df_ori[columns].copy()
    filtered_df[DTSC.MEASURED] = filtered_df[formatted_method_columns].any(axis=1)

    return filtered_df[[DTSC.SITE_ID, DTSC.SITE_TYPE, DTSC.MEASURED]]
