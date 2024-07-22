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
from sensors import quantification
from virtual_world.sites import Site
from constants.sensor_constants import QuantificationTypes


class DefaultSensor:
    def __init__(
        self,
        mdl: Union[list[float], float],
        quantification_parameters: list[float],
        quantification_type: str = QuantificationTypes.DEFAULT.value,
        input_dir: str = None,
    ) -> None:
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
        self.initialize_quantification_predictor(
            quantification_parameters,
            quantification_type=quantification_type,
            input_dir=input_dir,
        )

    def initialize_quantification_predictor(
        self, quantification_parameters: list[float], quantification_type: str, input_dir: str
    ):
        if quantification_type == QuantificationTypes.DEFAULT.value:
            self._quantification_predictor = quantification.DefaultQuantificationPredictor(
                *quantification_parameters
            )
        elif quantification_type == QuantificationTypes.UNIFORM.value:
            self._quantification_predictor = quantification.UniformQuantificationPredictor(
                *quantification_parameters
            )
        elif quantification_type == QuantificationTypes.SAMPLING.value:
            self._quantification_predictor = quantification.SamplingQuantificationPredictor(
                *quantification_parameters, input_dir=input_dir
            )

    def _rate_detected(self, emis_rate: float) -> bool:
        return emis_rate >= self._mdl

    def detect_emissions(self, site: Site, meth_name: str):
        return

    def check_min_threshold(self, emis_rate: float) -> bool:
        if self._min_threshold is not None:
            return emis_rate >= self._min_threshold
        return True

    def _measure_rate(self, true_rate: float) -> float:
        return self._quantification_predictor.predict(true_rate)
