"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_generate_emissions
Purpose: Unit test file for testing the generation of emissions from sources

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

from datetime import date
import pandas as pd

import numpy as np
import scipy.stats
from src.virtual_world.sources import Source
from src.file_processing.input_processing.emissions_source_processing import EmissionsSourceSample
from testing.unit_testing.test_virtual_world.test_sources.sources_testing_resources.sources_testing_fixtures import (  # noqa
    mock_source_and_args_for_generate_emissions_fix,
    mock_simple_source_constructor_params_fix,
    mock_source_and_args_for_generate_emissions_same_st_ed_fix,
)
from virtual_world.emission_types.emission import Emission


def mock_source_init(self, *args, **kwargs) -> None:
    self._generated_emissions = {}
    if kwargs:
        self._source_ID = kwargs["id"]
        self._emis_duration = kwargs["emis_duration"]
        self._emis_prod_rate = kwargs["emis_prod_rate"]
        self._repairable = kwargs["repairable"]
        self._emis_rate_source = kwargs["emis_rate_source"]
        self._meth_spat_covs = kwargs["meth_spat_covs"]
        self._multi_emissions = kwargs["multi_emissions"]
        self._persistent = kwargs["persistent"]


def test_001_validate_date_randomness(mocker) -> None:
    # Set up parameters for testing
    sim_start_date = date(2023, 1, 1)
    sim_end_date = date(2023, 12, 31)
    sim_number = 1

    emission_rate_source_dictionary = {
        "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
    }

    repair_delay_dataframe = pd.DataFrame()
    mocker.patch.object(Source, "__init__", mock_source_init)
    source_id = "test"
    test_source = Source(
        id=source_id,
        emis_duration=365,
        emis_prod_rate=0.5,
        repairable=False,
        emis_rate_source="test",
        meth_spat_covs={},
        multi_emissions=True,
        persistent=True,
    )
    # Fix a seed for testing so that the test is reproducible
    np.random.seed(0)
    # Call the method to generate emissions
    emissions_dict: dict[str, list[Emission]] = test_source.generate_emissions(
        sim_start_date,
        sim_end_date,
        sim_number,
        emission_rate_source_dictionary,
        repair_delay_dataframe,
    )

    # Extract the dates of the emissions for testing randomness
    emission_dates = [emission._start_date for emission in emissions_dict[source_id]]

    date_diffs = [(emis_date - sim_start_date).days for emis_date in emission_dates]

    num_bins = 20

    expected_counts = np.full(num_bins, len(date_diffs) / num_bins)

    observed_counts, _ = np.histogram(date_diffs, bins=num_bins)

    chi_sq_stat, p_value, _, _ = scipy.stats.chi2_contingency([observed_counts, expected_counts])

    alpha = 0.05

    assert p_value > alpha


def test_001_test_single_emission_creation(mocker) -> None:
    # Set up parameters for testing
    sim_start_date = date(2023, 1, 1)
    sim_end_date = date(2024, 1, 31)
    sim_number = 1

    emission_rate_source_dictionary = {
        "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
    }
    repair_delay_dataframe = pd.DataFrame()
    mocker.patch.object(Source, "__init__", mock_source_init)
    source_id = "test"
    test_source = Source(
        id=source_id,
        emis_duration=365,
        emis_prod_rate=1,
        repairable=False,
        emis_rate_source="test",
        meth_spat_covs={},
        multi_emissions=False,
        persistent=True,
    )
    # Fix a seed for testing so that the test is reproducible
    np.random.seed(0)
    # Call the method to generate emissions
    emissions_dict: dict[str, list[Emission]] = test_source.generate_emissions(
        sim_start_date,
        sim_end_date,
        sim_number,
        emission_rate_source_dictionary,
        repair_delay_dataframe,
    )
    assert len(emissions_dict["test"]) == 3
    assert emissions_dict["test"][0]._start_date == date(2022, 1, 1)
    assert emissions_dict["test"][1]._start_date == date(2023, 1, 2)
    assert emissions_dict["test"][2]._start_date == date(2024, 1, 3)


def test_001_test_multi_emission_creation(mocker) -> None:
    # Set up parameters for testing
    sim_start_date = date(2023, 1, 1)
    sim_end_date = date(2023, 12, 31)
    sim_number = 1

    emission_rate_source_dictionary = {
        "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
    }
    repair_delay_dataframe = pd.DataFrame()
    mocker.patch.object(Source, "__init__", mock_source_init)
    source_id = "test"
    test_source = Source(
        id=source_id,
        emis_duration=365,
        emis_prod_rate=1,
        repairable=False,
        emis_rate_source="test",
        meth_spat_covs={},
        multi_emissions=True,
        persistent=True,
    )
    # Fix a seed for testing so that the test is reproducible
    np.random.seed(0)
    # Call the method to generate emissions
    emissions_dict: dict[str, list[Emission]] = test_source.generate_emissions(
        sim_start_date,
        sim_end_date,
        sim_number,
        emission_rate_source_dictionary,
        repair_delay_dataframe,
    )
    assert len(emissions_dict["test"]) == 730
