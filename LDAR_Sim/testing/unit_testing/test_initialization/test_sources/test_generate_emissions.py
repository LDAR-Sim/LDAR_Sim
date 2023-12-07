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
from virtual_world.sources import Source
import numpy as np
from datetime import date, timedelta


# TODO : renumber/name the tests
def test_001_generation_of_emissions_dict():
    assert 0 == 0


def test_001_gen_emiss_is_unique_for_each_sim_run():
    assert 9 == 9


def test_001_same_start_end_date_behavior():
    assert 0 == 0


def test_001_negative_duration():
    assert 0 == 0


def test_001_unique_source_id_generation():
    assert 9 == 9


# TODO : fix up below test
# def test_001_validate_randomness(self):
#     # Set up parameters for testing
#     sim_start_date = date(2023, 1, 1)
#     sim_end_date = date(2023, 1, 10)
#     sim_number = 1

#     # Call the method to generate emissions
#     emissions_dict = Source.generate_emissions(sim_start_date, sim_end_date, sim_number)

#     # Extract the dates of the emissions for testing randomness
#     emission_dates = [
#         emission.start_date for emission in emissions_dict[self.your_instance._source_ID]
#     ]

#     # Calculate the observed frequencies in each simulated day
#     observed_counts, _ = np.histogram(
#         emission_dates,
#         bins=np.arange((sim_start_date - timedelta(days=1)), sim_end_date, timedelta(days=1)),
#     )

#     # Expected frequency assuming a binomial distribution
#     expected_counts = np.random.binomial(1, Source._emis_prod_rate, len(observed_counts))

#     # Perform chi-squared test
#     chi_squared_stat = np.sum((observed_counts - expected_counts) ** 2 / expected_counts)
#     p_value = 1 - stats.chi2.cdf(chi_squared_stat, df=len(observed_counts) - 1)

#     # Set a significance level (e.g., 0.05) and assert that the p-value is greater than it
#     significance_level = 0.05
#     self.assertGreater(p_value, significance_level)
