"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        default_sensor
Purpose: The provides default behaviors for all sensors

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

import numpy as np
from virtual_world.sites import Site


class DefaultSensor:
    def __init__(self, mdl: float, quantification_error: float) -> None:
        self._mdl: float = mdl
        self._quantification_error: float = quantification_error

    def _rate_detected(self, emis_rate: float) -> bool:
        return emis_rate >= self._mdl[0]

    def detect_emissions(self, site: Site, meth_name: str):
        return

    def check_min_threshold(self, emis_rate: float) -> bool:
        if len(self._mdl) == 3:
            return emis_rate >= self._mdl[3]

    def _measure_rate(self, true_rate: float) -> float:
        quant_error: float = np.random.normal(0, self._quantification_error)

        measured_rate = None
        if quant_error >= 0:
            measured_rate: float = true_rate + true_rate * quant_error
        if quant_error < 0:
            denom: float = abs(quant_error - 1)
            measured_rate: float = true_rate / denom

        return measured_rate
