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

from typing import Union
import numpy as np
from virtual_world.sites import Site


class DefaultSensor:
    def __init__(self, mdl: Union[list[float], float], quantification_error: float) -> None:
        # TODO revisit this implementation
        self._min_threshold: float = None
        if isinstance(mdl, (float, int)):
            self._mdl: float = mdl
        elif isinstance(mdl, list):
            self._mdl: float = mdl[0]
            if len(mdl) == 4:
                self._min_threshold: float = mdl[3]
        else:
            raise TypeError("mdl must be a integer, float or a list of floats")
        self._quantification_error: float = quantification_error

    def _rate_detected(self, emis_rate: float) -> bool:
        return emis_rate >= self._mdl

    def detect_emissions(self, site: Site, meth_name: str):
        return

    def check_min_threshold(self, emis_rate: float) -> bool:
        if self._min_threshold is not None:
            return emis_rate >= self._min_threshold
        return True

    def _measure_rate(self, true_rate: float) -> float:
        quant_error: float = np.random.normal(0, self._quantification_error)

        measured_rate = None
        if quant_error >= 0:
            measured_rate: float = true_rate + true_rate * quant_error
        if quant_error < 0:
            denom: float = abs(quant_error - 1)
            measured_rate: float = true_rate / denom

        return measured_rate
