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

from datetime import date, timedelta
from typing import Tuple
import statistics as stats
from numpy import average, sum, random as rd, histogram, arange
import pytest
from src.virtual_world.sources import Source
from src.file_processing.input_processing.emissions_source_processing import EmissionsSourceSample
from testing.unit_testing.test_virtual_world.test_sources.sources_testing_fixtures import (  # noqa
    mock_source_and_args_for_generate_emissions_fix,
    mock_simple_source_constructor_params_fix,
    mock_source_and_args_for_generate_emissions_same_st_ed_fix,
)


# TODO : renumber/name the tests
def test_001_generation_of_emissions_dict(
    mock_source_and_args_for_generate_emissions: Tuple[Source, int, date, date]
) -> None:
    # Set a random seed for reproducibility
    rd.seed(0)

    src: Source = mock_source_and_args_for_generate_emissions[0]
    sim_sd, sim_ed, n_sims = mock_source_and_args_for_generate_emissions[1]
    expected_res: date = mock_source_and_args_for_generate_emissions[2]
    for sim in range(n_sims):
        src.generate_emissions(
            sim_start_date=sim_sd,
            sim_end_date=sim_ed,
            sim_number=sim,
            emission_rate_source_dictionary={
                "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
            },
            repair_delay_dataframe={},
        )
    emis_counts: list[int] = []
    for sim, emissions in src._generated_emissions.items():
        emis_counts.append(len(emissions))
    assert average(emis_counts) == pytest.approx(expected_res, rel=0.01)


def test_001_gen_emiss_is_unique_for_each_sim_run(
    mock_source_and_args_for_generate_emissions: Tuple[Source, int, date, date]
) -> None:
    # Set a random seed for reproducibility
    rd.seed(0)

    src: Source = mock_source_and_args_for_generate_emissions[0]
    sim_sd, sim_ed, n_sims = mock_source_and_args_for_generate_emissions[1]
    for sim in range(n_sims):
        src.generate_emissions(
            sim_start_date=sim_sd,
            sim_end_date=sim_ed,
            sim_number=sim,
            emission_rate_source_dictionary={
                "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
            },
            repair_delay_dataframe={},
        )
    emis_counts: list[int] = []
    for sim, emissions in src._generated_emissions.items():
        emis_counts.append(len(emissions))
    unique_elements = len(set(emis_counts))
    assert unique_elements > 1


def test_001_same_start_end_date_behavior(
    mock_source_and_args_for_generate_emissions_same_st_ed: Tuple[Source, int, date, date]
) -> None:
    rd.seed(0)

    src: Source = mock_source_and_args_for_generate_emissions_same_st_ed[0]
    sim_sd, sim_ed, n_sims = mock_source_and_args_for_generate_emissions_same_st_ed[1]
    expected_res: date = mock_source_and_args_for_generate_emissions_same_st_ed[2]
    for sim in range(n_sims):
        src.generate_emissions(
            sim_start_date=sim_sd,
            sim_end_date=sim_ed,
            sim_number=sim,
            emission_rate_source_dictionary={
                "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
            },
            repair_delay_dataframe={},
        )
    emis_counts: list[int] = []
    for sim, emissions in src._generated_emissions.items():
        emis_counts.append(len(emissions))
    assert average(emis_counts) == pytest.approx(expected_res, rel=0.1)


# def test_001_validate_randomness(self):
#     # Set up parameters for testing
#     sim_start_date = date(2023, 1, 1)
#     sim_end_date = date(2023, 1, 10)
#     sim_number = 1

#     emission_rate_source_dictionary = (
#         {"test": EmissionsSourceSample("test", "gram", "second", [1], 1000)},
#     )
#     repair_delay_dataframe = ({},)
#     # Call the method to generate emissions
#     emissions_dict = Source.generate_emissions(
#         sim_start_date,
#         sim_end_date,
#         sim_number,
#         emission_rate_source_dictionary,
#         repair_delay_dataframe,
#     )

#     # Extract the dates of the emissions for testing randomness
#     emission_dates = [
#         emission.start_date for emission in emissions_dict[self.your_instance._source_ID]
#     ]

#     # Calculate the observed frequencies in each simulated day
#     observed_counts, _ = histogram(
#         emission_dates,
#         bins=arange((sim_start_date - timedelta(days=1)), sim_end_date, timedelta(days=1)),
#     )

#     # Expected frequency assuming a binomial distribution
#     expected_counts = rd.binomial(1, Source._emis_prod_rate, len(observed_counts))

#     # Perform chi-squared test
#     chi_squared_stat = sum((observed_counts - expected_counts) ** 2 / expected_counts)
#     p_value = 1 - stats.chi2.cdf(chi_squared_stat, df=len(observed_counts) - 1)

#     # Set a significance level (e.g., 0.05) and assert that the p-value is greater than it
#     significance_level = 0.05
#     self.assertGreater(p_value, significance_level)
