"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        METEC_NoWind_sensor
Purpose: Provides the sensor overwrites needed to replicate the probability
of detection curves provided by a METEC report. These values do not factor in wind speeds

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
from constants.sensor_constants import QuantificationTypes
from sensors.default_sensor import DefaultSensor
from sensors.default_component_level_sensor import DefaultComponentLevelSensor
from sensors.default_equipment_group_level_sensor import DefaultEquipmentGroupLevelSensor
from constants.general_const import Conversion_Constants as CC


class METECNWSite(DefaultSensor):
    def __init__(
        self,
        mdl: float,
        quantification_95_percent_ci_lower_range: float,
        quantification_95_percent_ci_upper_range: float,
        quantification_type: str = QuantificationTypes.DEFAULT.value,
    ) -> None:
        super().__init__(
            mdl,
            quantification_95_percent_ci_lower_range,
            quantification_95_percent_ci_upper_range,
            quantification_type,
        )
        self._mdl = mdl

    def _rate_detected(self, emis_rate: float) -> bool:
        prob_detect = 1 / (1 + np.exp(self._mdl[0] - self._mdl[1] * (emis_rate * CC.GS_TO_KGHR)))
        if prob_detect >= 1:
            return True
        return np.random.binomial(1, prob_detect) and self.check_min_threshold(emis_rate)


class METECNWEquipmentGroup(DefaultEquipmentGroupLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)

    def _rate_detected(self, emis_rate: float) -> bool:
        prob_detect = 1 / (1 + np.exp(self._mdl[0] - self._mdl[1] * (emis_rate * CC.GS_TO_KGHR)))
        if prob_detect >= 1:
            return True
        return np.random.binomial(1, prob_detect) and self.check_min_threshold(emis_rate)


class METECNWComponent(DefaultComponentLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)

    def _rate_detected(self, emis_rate: float) -> bool:
        prob_detect = 1 / (1 + np.exp(self._mdl[0] - self._mdl[1] * (emis_rate * CC.GS_TO_KGHR)))
        if prob_detect >= 1:
            return True
        return np.random.binomial(1, prob_detect) and self.check_min_threshold(emis_rate)
