"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_generate_emissions.py
Purpose: Contains unit tests to test generate_emissions function

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
import numpy as np
from datetime import date
from virtual_world.sources import Source


def mock_source(self, *args, **kwargs):
    self._source_ID = "source1"
    self._active_duration = 10
    self._inactive_duration = 0
    self._meth_spat_covs = {}
    self._emis_duration = 10
    self._emis_prod_rate = 0.002739  # ~1 emission should be made in a year
    self._multi_emissions = True
    self._repairable = True
    self._generated_emissions = {}


def mock_source2(self, *args, **kwargs):
    self._source_ID = "source1"
    self._active_duration = 10
    self._inactive_duration = 0
    self._meth_spat_covs = {}
    self._emis_duration = 10
    self._emis_prod_rate = 0.0273972  # ~10 emissions should be made in a year
    self._multi_emissions = True
    self._repairable = True
    self._generated_emissions = {}


def mock_source3(self, *args, **kwargs):
    self._source_ID = "source1"
    self._active_duration = 365
    self._inactive_duration = 0
    self._meth_spat_covs = {}
    self._emis_duration = 365
    self._emis_prod_rate = 0.0273972  # ~10 emissions should be made in a year
    self._multi_emissions = True
    self._repairable = True
    self._generated_emissions = {}


def mock_source4(self, *args, **kwargs):
    self._source_ID = "source1"
    self._active_duration = 365
    self._inactive_duration = 0
    self._meth_spat_covs = {}
    self._emis_duration = 365
    self._emis_prod_rate = 0.0273972  # ~10 emissions should be made in a year
    self._multi_emissions = False
    self._repairable = True
    self._generated_emissions = {}


def mock_create_emission(
    self,
    leak_count,
    start_date,
    sim_start_date,
    emission_rate_source_dictionary,
    repair_delay_dataframe,
):
    return start_date


def setup_mock_source(mocker):
    mocker.patch.object(Source, "__init__", mock_source)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_repairable", return_value=False)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_rep_delay", return_value=10)
    mocker.patch.object(Source, "_get_rep_cost", return_value=1)
    mocker.patch.object(Source, "_get_emis_duration", return_value=10)
    mocker.patch.object(Source, "_create_emission", mock_create_emission)


def setup_mock_source2(mocker):
    mocker.patch.object(Source, "__init__", mock_source2)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_repairable", return_value=False)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_rep_delay", return_value=10)
    mocker.patch.object(Source, "_get_rep_cost", return_value=1)
    mocker.patch.object(Source, "_get_emis_duration", return_value=10)
    mocker.patch.object(Source, "_create_emission", mock_create_emission)


def setup_mock_source3(mocker):
    mocker.patch.object(Source, "__init__", mock_source3)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_repairable", return_value=False)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_rep_delay", return_value=10)
    mocker.patch.object(Source, "_get_rep_cost", return_value=1)
    mocker.patch.object(Source, "_get_emis_duration", return_value=365)
    mocker.patch.object(Source, "_create_emission", mock_create_emission)


def setup_mock_source4(mocker):
    mocker.patch.object(Source, "__init__", mock_source4)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_repairable", return_value=False)
    mocker.patch.object(Source, "_get_rate", return_value=1)
    mocker.patch.object(Source, "_get_rep_delay", return_value=10)
    mocker.patch.object(Source, "_get_rep_cost", return_value=1)
    mocker.patch.object(Source, "_get_emis_duration", return_value=365)
    mocker.patch.object(Source, "_create_emission", mock_create_emission)


def simple_inputs():
    start_date = date(2021, 1, 1)
    end_date = date(2021, 12, 31)
    sim_number = 1
    emission_rate_source_dictionary = {"source1": []}
    repair_delay_dataframe = None
    return (
        start_date,
        end_date,
        sim_number,
        emission_rate_source_dictionary,
        repair_delay_dataframe,
        True,
    )


def expected_dictionary():
    return {"source1": [date(2021, 5, 20)]}


def expected_dictionary2():
    return {
        "source1": [
            date(2021, 10, 16),
            date(2021, 10, 4),
            date(2021, 9, 18),
            date(2021, 7, 20),
            date(2021, 6, 4),
            date(2021, 5, 20),
            date(2021, 3, 4),
            date(2021, 3, 2),
            date(2021, 2, 12),
            date(2021, 1, 11),
        ]
    }


def expected_dictionary3():
    return {
        "source1": [
            date(2021, 12, 29),
            date(2021, 10, 22),
            date(2021, 10, 5),
            date(2021, 9, 17),
            date(2021, 9, 12),
            date(2021, 8, 23),
            date(2021, 8, 19),
            date(2021, 7, 17),
            date(2021, 4, 24),
            date(2021, 3, 28),
            date(2021, 3, 24),
            date(2021, 3, 3),
            date(2021, 2, 26),
            date(2021, 2, 25),
            date(2020, 10, 26),
            date(2020, 10, 14),
            date(2020, 9, 28),
            date(2020, 7, 30),
            date(2020, 6, 14),
            date(2020, 5, 30),
            date(2020, 3, 14),
            date(2020, 3, 12),
            date(2020, 2, 23),
            date(2020, 1, 22),
        ]
    }


def expected_dictionary4():
    return {
        "source1": [
            date(2021, 2, 25),
            date(2020, 1, 22),
        ]
    }


@pytest.fixture
def input_and_expected_output():
    return simple_inputs(), expected_dictionary()


def test_generate_emissions(input_and_expected_output, mocker):
    # Tests that a single emission gets generated with the given EPR
    np.random.seed(0)
    setup_mock_source(mocker)
    input, expected_output = input_and_expected_output
    source_instance = Source()
    output = source_instance.generate_emissions(*input)
    assert expected_output == output


@pytest.fixture
def input_and_expected_output2():
    return simple_inputs(), expected_dictionary2()


def test_generate_emissions2(input_and_expected_output2, mocker):
    # Tests that 10 emissions gets generated with the given EPR and time frame
    np.random.seed(0)
    setup_mock_source2(mocker)
    input, expected_output = input_and_expected_output2
    source_instance = Source()
    output = source_instance.generate_emissions(*input)
    assert expected_output == output


@pytest.fixture
def input_and_expected_output3():
    return simple_inputs(), expected_dictionary3()


def test_generate_preemissions(input_and_expected_output3, mocker):
    # testing to ensure that the preemissions are generated correctly
    # in total should be around ~20 emissions given the EPR (got a little more due to chance)
    np.random.seed(0)
    setup_mock_source3(mocker)
    input, expected_output = input_and_expected_output3
    source_instance = Source()
    output = source_instance.generate_emissions(*input)
    assert expected_output == output


@pytest.fixture
def input_and_expected_output4():
    return simple_inputs(), expected_dictionary4()


def test_generate_singleemissions(input_and_expected_output4, mocker):
    # testing for when multiple emissions are not allowed
    # although EPR says we should have more than 10 emissions, only 2 should be generated
    np.random.seed(0)
    setup_mock_source4(mocker)
    input, expected_output = input_and_expected_output4
    source_instance = Source()
    output = source_instance.generate_emissions(*input)
    assert expected_output == output
