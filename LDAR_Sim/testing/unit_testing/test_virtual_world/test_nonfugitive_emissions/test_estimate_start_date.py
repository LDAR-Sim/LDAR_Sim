"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_estimate_start_date.py
Purpose: Testing for the NonRepairableEmission class estimate_start_date method.

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
from hypothesis import given, strategies as st
from src.virtual_world.nonfugitive_emissions import NonRepairableEmission


def mock_simple_nonfugitive_emission_for_est_start_date_testing_1() -> NonRepairableEmission:
    return NonRepairableEmission(1, 1, date(*[2018, 1, 1]), date(*[2017, 1, 1]), False, {}, 365)


@st.composite
def gen_valid_est_start_date_testing_data(draw):
    t_since_ldar: int = draw(st.integers(min_value=1, max_value=365))
    current_date = draw(st.dates(min_value=date(2000, 1, 1), max_value=date(2023, 12, 31)))
    expected_est_sd = current_date - timedelta(days=t_since_ldar)
    expected_est_days_active = t_since_ldar
    return t_since_ldar, current_date, (expected_est_sd, expected_est_days_active)


@given(test_data=gen_valid_est_start_date_testing_data())
def test_000_estimate_start_date_estimates_correct_with_with_valid_t_since_ldar(
    test_data: Tuple[int, date, date],
) -> None:
    nonrep_emis: NonRepairableEmission = (
        mock_simple_nonfugitive_emission_for_est_start_date_testing_1()
    )
    time_since_ldar, cur_dt, ans = test_data
    exp_est_dt, est_days_active = ans
    nonrep_emis.estimate_start_date(cur_dt, time_since_ldar)
    assert nonrep_emis._estimated_date_began == exp_est_dt
    assert nonrep_emis._estimated_days_active == est_days_active
