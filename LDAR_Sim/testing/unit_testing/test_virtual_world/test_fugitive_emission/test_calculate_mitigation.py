"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_mitigation.py
Purpose: Contains unit tests for testing the calculation of mitigation of 
fugitive emissions

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
from src.virtual_world.fugitive_emission import FugitiveEmission
from src.constants.general_const import Emission_Constants as ec


def mock_simple_fugitive_emission_for_mitigation1() -> FugitiveEmission:
    return FugitiveEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), False, {}, 14, 200, 365)


def mock_simple_fugitive_emission_for_mitigation2() -> FugitiveEmission:
    return FugitiveEmission(
        1,
        1,
        date(*[2019, 12, 30]),
        date(*[2017, 1, 1]),
        False,
        {},
        14,
        200,
        365,
    )


def test_000_calc_mit_returns_expected_values_for_simple_case() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation1()

    fug_emis._active_days = 100
    fug_emis._status = ec.REPAIRED
    mitigated = fug_emis.calc_mitigated(date(*[2019, 1, 1]))
    expected = 22896
    assert expected == mitigated


def test_000_calc_mit_returns_expected_values_for_simple_active_emissions() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation1()

    fug_emis._active_days = 100
    mitigated = fug_emis.calc_mitigated(date(*[2019, 1, 1]))
    expected = 0.0
    assert expected == mitigated


def test_000_calc_mit_returns_expected_values_for_not_active() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation1()

    fug_emis._active_days = 0
    mitigated = fug_emis.calc_mitigated(date(*[2019, 1, 1]))
    expected = 0.0
    assert expected == mitigated


def test_000_calc_mit_returns_expected_values_for_edge_case_nrd_less_than_active() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation1()
    fug_emis._status = ec.REPAIRED
    fug_emis._active_days = 370
    mitigated = fug_emis.calc_mitigated(date(*[2019, 1, 1]))
    expected = 0.0
    assert expected == mitigated


def test_000_calc_mit_returns_expected_values_for_repaired_by_nrd_but_active_is_less() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation1()
    fug_emis._status = ec.REPAIRED
    fug_emis._active_days = 10
    fug_emis._tagged_by_company = ec.NATURAL
    mitigated = fug_emis.calc_mitigated(date(*[2019, 1, 1]))
    expected = 0.0
    assert expected == mitigated


def test_000_calc_mit_emiss_start_before_sim() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation1()
    fug_emis._status = ec.REPAIRED
    fug_emis._active_days = 50
    fug_emis._days_active_b4_sim = 50
    mitigated = fug_emis.calc_mitigated(date(*[2019, 1, 1]))
    expected = 22896
    assert expected == mitigated


def test_000_calc_mit_emiss_rep_emiss_end_date_before_theory_date() -> None:
    fug_emis: FugitiveEmission = mock_simple_fugitive_emission_for_mitigation2()
    fug_emis._status = ec.REPAIRED
    fug_emis._active_days = 1
    mitigated = fug_emis.calc_mitigated(date(*[2020, 1, 1]))
    expected = 86.4
    assert expected == mitigated
