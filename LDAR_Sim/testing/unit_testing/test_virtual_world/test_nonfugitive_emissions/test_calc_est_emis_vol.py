"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calc_est_emis_vol.py
Purpose: Testing for the overriden calc_est_emis_vol method in the NonFugitiveEmissions class.

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
from src.virtual_world.nonfugitive_emissions import NonRepairableEmission
from src.constants import conversion_constants as conv_const


def mock_non_fugitive_emission_init(self, *args, **kwargs):
    self._tagged = False
    self._estimated_date_began = kwargs.get("estimated_date_began", None)
    self._measured_rate = kwargs.get("measured_rate", 0)
    self._estimated_days_active_after_detection = kwargs.get(
        "estimated_days_active_after_detection", 0
    )
    self._estimated_days_active = kwargs.get("estimated_days_active", 0)


def setup_mock_non_fugitive_emission(mocker):
    mocker.patch.object(
        NonRepairableEmission,
        "__init__",
        mock_non_fugitive_emission_init,
    )
    return date(2025, 1, 1)


def test_000_calc_est_emis_vol_correctly_returns_0_when_no_estimated_date_began(mocker):
    end_date: date = setup_mock_non_fugitive_emission(mocker)
    test_emission: NonRepairableEmission = NonRepairableEmission()
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == 0


def test_000_calc_est_emis_vol_correctly_returns_0_when_no_measured_rate(mocker):
    end_date: date = setup_mock_non_fugitive_emission(mocker)
    estimated_date_began: date = date(2024, 11, 1)
    estimated_days_active: int = 15
    estimated_days_active_after_detection: int = 30
    test_emission: NonRepairableEmission = NonRepairableEmission(
        estimated_date_began=estimated_date_began,
        estimated_days_active=estimated_days_active,
        estimated_days_active_after_detection=estimated_days_active_after_detection,
    )
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == 0


def test_000_calc_est_emis_vol_returns_expected_vol_when_est_duration_not_longer_than_end_date(
    mocker,
):
    end_date: date = setup_mock_non_fugitive_emission(mocker)
    estimated_date_began: date = date(2024, 11, 1)
    measured_rate: float = 10.0
    estimated_days_active: int = 15
    estimated_days_active_after_detection: int = 30
    expected_vol_emitted = (
        measured_rate
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
        * (estimated_days_active + estimated_days_active_after_detection)
    )
    test_emission: NonRepairableEmission = NonRepairableEmission(
        estimated_date_began=estimated_date_began,
        measured_rate=measured_rate,
        estimated_days_active=estimated_days_active,
        estimated_days_active_after_detection=estimated_days_active_after_detection,
    )
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == expected_vol_emitted


def test_000_calc_est_emis_vol_returns_expected_vol_when_est_duration_longer_than_end_date(
    mocker,
):
    end_date: date = setup_mock_non_fugitive_emission(mocker)
    estimated_date_began: date = date(2024, 11, 1)
    measured_rate: float = 10.0
    estimated_days_active: int = 200
    estimated_days_active_after_detection: int = 30
    expected_vol_emitted = (
        measured_rate
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
        * (end_date - estimated_date_began).days
    )
    test_emission: NonRepairableEmission = NonRepairableEmission(
        estimated_date_began=estimated_date_began,
        measured_rate=measured_rate,
        estimated_days_active=estimated_days_active,
        estimated_days_active_after_detection=estimated_days_active_after_detection,
    )
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == expected_vol_emitted
