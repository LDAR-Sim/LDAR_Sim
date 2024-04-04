"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calc_est_emis_vol.py
Purpose: Testing for the overriden calc_est_emis_vol method in the FugitiveEmission class.

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
from LDAR_Sim.src.constants import conversion_constants as conv_const


def mock_fugitive_emission_init(self, *args, **kwargs):
    self._tagged = False
    self._estimated_date_began = kwargs.get("estimated_date_began", None)
    self._repair_date = kwargs.get("repair_date", None)
    self._measured_rate = kwargs.get("measured_rate", 0)


def setup_mock_fugitive_emission(mocker):
    mocker.patch.object(
        FugitiveEmission,
        "__init__",
        mock_fugitive_emission_init,
    )
    return date(2025, 1, 1)


def test_000_calc_est_emis_vol_correctly_returns_0_when_no_estimated_date_began(mocker):
    end_date: date = setup_mock_fugitive_emission(mocker)
    test_emission: FugitiveEmission = FugitiveEmission()
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == 0


def test_000_calc_est_emis_vol_correctly_returns_0_when_no_measured_rate(mocker):
    end_date: date = setup_mock_fugitive_emission(mocker)
    repair_date: date = date(2024, 11, 30)
    estimated_date_began: date = date(2024, 11, 1)
    test_emission: FugitiveEmission = FugitiveEmission(
        repair_date=repair_date,
        estimated_date_began=estimated_date_began,
    )
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == 0


def test_000_calc_est_emis_vol_correctly_returns_expected_vol_when_repair_date(mocker):
    end_date: date = setup_mock_fugitive_emission(mocker)
    repair_date: date = date(2024, 11, 30)
    estimated_date_began: date = date(2024, 11, 1)
    measured_rate: float = 10.0
    expected_vol_emitted = (
        measured_rate
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
        * (repair_date - estimated_date_began).days
    )
    test_emission: FugitiveEmission = FugitiveEmission(
        repair_date=repair_date,
        estimated_date_began=estimated_date_began,
        measured_rate=measured_rate,
    )
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == expected_vol_emitted


def test_000_calc_est_emis_vol_correctly_returns_expected_vol_when_detected_no_repair(mocker):
    end_date: date = setup_mock_fugitive_emission(mocker)
    estimated_date_began: date = date(2024, 11, 1)
    measured_rate: float = 10.0
    expected_vol_emitted = (
        measured_rate
        * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
        * (end_date - estimated_date_began).days
    )
    test_emission: FugitiveEmission = FugitiveEmission(
        estimated_date_began=estimated_date_began,
        measured_rate=measured_rate,
    )
    estimated_emis_volume = test_emission.calc_est_emis_vol(end_date=end_date)
    assert estimated_emis_volume == expected_vol_emitted
