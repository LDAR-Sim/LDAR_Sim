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

import pytest
import pandas as pd
from src.constants.infrastructure_const import (
    Deployment_TF_Sites_Constants as DTSC,
)
from src.virtual_world.infrastructure import Infrastructure
import itertools

EXPECTED_COLUMNS = [
    DTSC.SITE_ID,
    DTSC.SITE_TYPE,
    DTSC.REQUIRED_SURVEY.format(method="A"),
    DTSC.SITE_DEPLOYMENT.format(method="A"),
    DTSC.METHOD_MEASURED.format(method="A"),
    DTSC.REQUIRED_SURVEY.format(method="B"),
    DTSC.SITE_DEPLOYMENT.format(method="B"),
    DTSC.METHOD_MEASURED.format(method="B"),
]

METHODS_PARAMS: dict = {
    "A": {
        "parameter_level": "methods",
        "version": "4.0",
        "method_name": "A",
        "is_follow_up": False,
        "deployment_type": "mobile",
    },
    "B": {
        "parameter_level": "methods",
        "version": "4.0",
        "method_name": "B",
        "is_follow_up": False,
        "deployment_type": "mobile",
    },
}

METHODS_PARAMS_FOLLOW_UP: dict = {
    "A": {
        "parameter_level": "methods",
        "version": "4.0",
        "method_name": "A",
        "is_follow_up": True,
        "deployment_type": "mobile",
    },
    "B": {
        "parameter_level": "methods",
        "version": "4.0",
        "method_name": "B",
        "is_follow_up": False,
        "deployment_type": "mobile",
    },
}

METHODS_PARAMS_STATIONARY: dict = {
    "A": {
        "parameter_level": "methods",
        "version": "4.0",
        "method_name": "A",
        "is_follow_up": False,
        "deployment_type": "stationary",
    },
    "B": {
        "parameter_level": "methods",
        "version": "4.0",
        "method_name": "B",
        "is_follow_up": False,
        "deployment_type": "mobile",
    },
}


class MockSite:
    def __init__(self, site_id, site_type, deployment, surveys):
        self.site_id = site_id
        self.site_type = site_type
        self.deployment = deployment
        self.surveys = surveys

    def get_id(self):
        return self.site_id

    def get_type(self):
        return self.site_type

    def do_site_deployment(self, method):
        return self.deployment

    def get_required_surveys(self, method):
        return self.surveys


def mock_infrastructure_initialization(
    self, virtual_world, methods, in_dir, site_measured_df, mock_site
):
    self._sites = mock_site


def make_empty_df():
    return pd.DataFrame(index=range(5), columns=EXPECTED_COLUMNS)


@pytest.mark.parametrize(
    "mock_site,methods_params,expected_data",
    [
        (
            [
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
            ],
            METHODS_PARAMS,
            {
                DTSC.SITE_ID: [1, 1, 1, 1, 1],
                DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
                DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="A"): [True, True, True, True, True],
                DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="B"): [True, True, True, True, True],
            },
        ),
        (
            [
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
            ],
            METHODS_PARAMS_STATIONARY,
            {
                DTSC.SITE_ID: [1, 1, 1, 1, 1],
                DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
                DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="A"): [True, True, True, True, True],
                DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="B"): [True, True, True, True, True],
            },
        ),
        (
            [
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
                MockSite(1, "A", True, 2),
            ],
            METHODS_PARAMS_FOLLOW_UP,
            {
                DTSC.SITE_ID: [1, 1, 1, 1, 1],
                DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
                DTSC.REQUIRED_SURVEY.format(method="A"): [False, False, False, False, False],
                DTSC.SITE_DEPLOYMENT.format(method="A"): [False, False, False, False, False],
                DTSC.METHOD_MEASURED.format(method="A"): [False, False, False, False, False],
                DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="B"): [True, True, True, True, True],
            },
        ),
        (
            [
                MockSite(1, "A", True, 0),
                MockSite(1, "A", True, 0),
                MockSite(1, "A", True, 0),
                MockSite(1, "A", True, 0),
                MockSite(1, "A", True, 0),
            ],
            METHODS_PARAMS,
            {
                DTSC.SITE_ID: [1, 1, 1, 1, 1],
                DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
                DTSC.REQUIRED_SURVEY.format(method="A"): [False, False, False, False, False],
                DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="A"): [False, False, False, False, False],
                DTSC.REQUIRED_SURVEY.format(method="B"): [False, False, False, False, False],
                DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
                DTSC.METHOD_MEASURED.format(method="B"): [False, False, False, False, False],
            },
        ),
        (
            [
                MockSite(1, "A", False, 5),
                MockSite(1, "A", False, 5),
                MockSite(1, "A", False, 5),
                MockSite(1, "A", False, 5),
                MockSite(1, "A", False, 5),
            ],
            METHODS_PARAMS,
            {
                DTSC.SITE_ID: [1, 1, 1, 1, 1],
                DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
                DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="A"): [False, False, False, False, False],
                DTSC.METHOD_MEASURED.format(method="A"): [False, False, False, False, False],
                DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="B"): [False, False, False, False, False],
                DTSC.METHOD_MEASURED.format(method="B"): [False, False, False, False, False],
            },
        ),
        (
            [
                MockSite(1, "A", False, 5),
                MockSite(1, "A", True, 5),
                MockSite(1, "A", False, 5),
                MockSite(1, "A", True, 5),
                MockSite(1, "A", False, 5),
            ],
            METHODS_PARAMS,
            {
                DTSC.SITE_ID: [1, 1, 1, 1, 1],
                DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
                DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="A"): [False, True, False, True, False],
                DTSC.METHOD_MEASURED.format(method="A"): [False, True, False, True, False],
                DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
                DTSC.SITE_DEPLOYMENT.format(method="B"): [False, True, False, True, False],
                DTSC.METHOD_MEASURED.format(method="B"): [False, True, False, True, False],
            },
        ),
    ],
)
def test_generation_tf_sites(monkeypatch, mock_site, methods_params, expected_data):
    """
    Test that the generation of the true/false site list is correct
    """
    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        lambda self, virtual_world, methods, in_dir, site_measured_df: mock_infrastructure_initialization(  # noqa
            self, virtual_world, methods, in_dir, site_measured_df, mock_site
        ),
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, methods_params, None, site_tf_df)

    infra.gen_site_measured_tf_data(methods_params, site_tf_df)

    expected: pd.DataFrame = pd.DataFrame(expected_data)

    expected: pd.DataFrame = pd.DataFrame(expected_data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)
