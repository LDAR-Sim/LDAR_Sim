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


def make_empty_df():
    return pd.DataFrame(index=range(5), columns=EXPECTED_COLUMNS)


def test_simple_generation_tf_sites(monkeypatch):
    """
    Test that the generation of the true/false site list is correct
    """

    class MockSite:
        def get_id(self):
            return 1

        def get_type(self):
            return "A"

        def do_site_deployment(self, method):
            return True

        def get_required_surveys(self, method):
            return 2

    def mock_infrastructure_initialization(self, virtual_world, methods, in_dir, site_measured_df):
        self._sites = [MockSite() for _ in range(5)]

    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        mock_infrastructure_initialization,
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, METHODS_PARAMS, None, site_tf_df)

    infra.gen_site_measured_tf_data(METHODS_PARAMS, site_tf_df)

    data = {
        DTSC.SITE_ID: [1, 1, 1, 1, 1],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="A"): [True, True, True, True, True],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="B"): [True, True, True, True, True],
    }
    expected: pd.DataFrame = pd.DataFrame(data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)

def test_simple_generation_tf_sites_stationary(monkeypatch):
    """
    Test that the generation of the true/false site list is correct
    """

    class MockSite:
        def get_id(self):
            return 1

        def get_type(self):
            return "A"

        def do_site_deployment(self, method):
            return True

        def get_required_surveys(self, method):
            return 2

    def mock_infrastructure_initialization(self, virtual_world, methods, in_dir, site_measured_df):
        self._sites = [MockSite() for _ in range(5)]

    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        mock_infrastructure_initialization,
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, METHODS_PARAMS_STATIONARY, None, site_tf_df)

    infra.gen_site_measured_tf_data(METHODS_PARAMS_STATIONARY, site_tf_df)

    data = {
        DTSC.SITE_ID: [1, 1, 1, 1, 1],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="A"): [True, True, True, True, True],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="B"): [True, True, True, True, True],
    }
    expected: pd.DataFrame = pd.DataFrame(data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)


def test_simple_generation_tf_sites_for_followup(monkeypatch):
    """
    Test that the generation of the true/false site list is correct
    """

    class MockSite:
        def get_id(self):
            return 1

        def get_type(self):
            return "A"

        def do_site_deployment(self, method):
            return True

        def get_required_surveys(self, method):
            return 2

    def mock_infrastructure_initialization(self, virtual_world, methods, in_dir, site_measured_df):
        self._sites = [MockSite() for _ in range(5)]

    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        mock_infrastructure_initialization,
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, METHODS_PARAMS_FOLLOW_UP, None, site_tf_df)

    infra.gen_site_measured_tf_data(METHODS_PARAMS_FOLLOW_UP, site_tf_df)

    data = {
        DTSC.SITE_ID: [1, 1, 1, 1, 1],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [False, False, False, False, False],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [False, False, False, False, False],
        DTSC.METHOD_MEASURED.format(method="A"): [False, False, False, False, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="B"): [True, True, True, True, True],
    }
    expected: pd.DataFrame = pd.DataFrame(data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)


def test_simple_fail_generation_tf_sites(monkeypatch):
    """
    Test that the generation of the true/false site list is correct
    """

    class MockSite:
        def get_id(self):
            return 1

        def get_type(self):
            return "A"

        def do_site_deployment(self, method):
            return True

        def get_required_surveys(self, method):
            return 0

    def mock_infrastructure_initialization(self, virtual_world, methods, in_dir, site_measured_df):
        self._sites = [MockSite() for _ in range(5)]

    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        mock_infrastructure_initialization,
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, METHODS_PARAMS, None, site_tf_df)

    infra.gen_site_measured_tf_data(METHODS_PARAMS, site_tf_df)

    data = {
        DTSC.SITE_ID: [1, 1, 1, 1, 1],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [False, False, False, False, False],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="A"): [False, False, False, False, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [False, False, False, False, False],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [True, True, True, True, True],
        DTSC.METHOD_MEASURED.format(method="B"): [False, False, False, False, False],
    }
    expected: pd.DataFrame = pd.DataFrame(data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)


def test_simple_fail_generation_tf_sites2(monkeypatch):
    """
    Test that the generation of the true/false site list is correct
    """

    class MockSite:
        def get_id(self):
            return 1

        def get_type(self):
            return "A"

        def do_site_deployment(self, method):
            return False

        def get_required_surveys(self, method):
            return 5

    def mock_infrastructure_initialization(self, virtual_world, methods, in_dir, site_measured_df):
        self._sites = [MockSite() for _ in range(5)]

    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        mock_infrastructure_initialization,
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, METHODS_PARAMS, None, site_tf_df)

    infra.gen_site_measured_tf_data(METHODS_PARAMS, site_tf_df)

    data = {
        DTSC.SITE_ID: [1, 1, 1, 1, 1],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [False, False, False, False, False],
        DTSC.METHOD_MEASURED.format(method="A"): [False, False, False, False, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [False, False, False, False, False],
        DTSC.METHOD_MEASURED.format(method="B"): [False, False, False, False, False],
    }
    expected: pd.DataFrame = pd.DataFrame(data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)


def test_complex_generation_tf_sites(monkeypatch):
    """
    Test that the generation of the true/false site list is correct
    """

    class MockSite:
        return_values = itertools.cycle([False, False, True, True])

        def get_id(self):
            return 1

        def get_type(self):
            return "A"

        def do_site_deployment(self, method):
            return next(MockSite.return_values)

        def get_required_surveys(self, method):
            return 5

    def mock_infrastructure_initialization(self, virtual_world, methods, in_dir, site_measured_df):
        self._sites = [MockSite() for _ in range(5)]

    monkeypatch.setattr(
        "src.virtual_world.infrastructure.Infrastructure.__init__",
        mock_infrastructure_initialization,
    )

    site_tf_df = make_empty_df()

    infra = Infrastructure({}, METHODS_PARAMS, None, site_tf_df)

    infra.gen_site_measured_tf_data(METHODS_PARAMS, site_tf_df)

    data = {
        DTSC.SITE_ID: [1, 1, 1, 1, 1],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="A"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="B"): [False, True, False, True, False],
    }
    expected: pd.DataFrame = pd.DataFrame(data)

    assert list(site_tf_df.columns) == list(expected.columns)
    assert len(site_tf_df) == len(expected)
    pd.testing.assert_frame_equal(site_tf_df, expected, check_index_type=False, check_dtype=False)
