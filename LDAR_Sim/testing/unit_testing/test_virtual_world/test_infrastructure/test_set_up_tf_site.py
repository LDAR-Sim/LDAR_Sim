"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_populate_tf_site.py
Purpose: Contains unit tests related to populating the true/false deployment
site list data frame

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

from src.ldar_sim_run import set_up_tf_df
from src.constants.infrastructure_const import Deployment_TF_Sites_Constants as DTSC


METHODS_PARAMS: dict = {
    "A": {"parameter_level": "methods", "version": "4.0", "method_name": "A"},
    "B": {"parameter_level": "methods", "version": "4.0", "method_name": "B"},
}


def test_set_up_tf_df():
    n_sites: int = 5
    result = set_up_tf_df(METHODS_PARAMS, n_sites)
    expected_columns = [
        DTSC.SITE_ID,
        DTSC.SITE_TYPE,
        DTSC.REQUIRED_SURVEY.format(method="A"),
        DTSC.SITE_DEPLOYMENT.format(method="A"),
        DTSC.SITE_MEASURED.format(method="A"),
        DTSC.REQUIRED_SURVEY.format(method="B"),
        DTSC.SITE_DEPLOYMENT.format(method="B"),
        DTSC.SITE_MEASURED.format(method="B"),
    ]

    assert len(result) == 5
    assert list(result.columns) == expected_columns
