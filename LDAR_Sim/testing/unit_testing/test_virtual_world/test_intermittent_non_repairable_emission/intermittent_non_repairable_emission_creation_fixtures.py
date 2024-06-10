"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        intermittent_non_repairable_emission_creation_fixtures
Purpose: Contains fixtures for creating mock intermittent non-repairable emissions
         for testing purposes.

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
from datetime import date


@pytest.fixture(name="intermittent_non_repairable_emission_creation_params")
def intermittent_non_repairable_emission_creation_params_fixture() -> dict:
    return {
        "emission_number": 1,
        "emission_rate": 1.0,
        "start_date": date(2024, 1, 1),
        "simulation_start_date": date(2024, 1, 1),
        "repairable": False,
        "tech_spatial_coverage_probabilities": {},
        "duration": 365,
        "active_duration": 10,
        "inactive_duration": 10,
    }
