"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        Custom Threshold
Purpose: Provides a custom PoD where users provide the threshold for 
detection. Anything below this threshold is considered undetected. Anything
above the given threshold is detected with a user defined probability.

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
from sensors.default_component_level_sensor import DefaultComponentLevelSensor
from sensors.default_equipment_group_level_sensor import DefaultEquipmentGroupLevelSensor
from sensors.default_site_level_sensor import DefaultSiteLevelSensor

"""
    POD = P(x) = 1 / (1 + exp(b0 + b1 * x))
        b0 = user defined coefficient
        b1 = user defined coefficient
        x = emission rate
User input:
    MDL values: [
        prob_detect b0, 
        prob_detect b1,
        0,  # not used but need some input
        threshold - threshold for detection,
    ]
"""


class GenericPOD_Comp(DefaultComponentLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)
        self._mdl = mdl
        if len(mdl) == 3:
            self._min_threshold: float = mdl[2]

    def _rate_detected(self, emis_rate: float) -> bool:
        b0 = self._mdl[0]
        b1 = self._mdl[1]
        if self.check_min_threshold(emis_rate):
            prob_detect = 1 / (1 + np.exp(b0 + b1 * emis_rate))
            return np.random.binomial(1, prob_detect)
        else:
            return False


class GenericPOD_Equip(DefaultEquipmentGroupLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)
        self._mdl = mdl
        if len(mdl) == 3:
            self._min_threshold: float = mdl[2]

    def _rate_detected(self, emis_rate: float) -> bool:
        b0 = self._mdl[0]
        b1 = self._mdl[1]
        if self.check_min_threshold(emis_rate):
            prob_detect = 1 / (1 + np.exp(b0 + b1 * emis_rate))
            return np.random.binomial(1, prob_detect)
        else:
            return False


class GenericPOD_Site(DefaultSiteLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)
        self._mdl = mdl
        if len(mdl) == 3:
            self._min_threshold: float = mdl[2]

    def _rate_detected(self, emis_rate: float) -> bool:
        b0 = self._mdl[0]
        b1 = self._mdl[1]
        if self.check_min_threshold(emis_rate):
            prob_detect = 1 / (1 + np.exp(b0 + b1 * emis_rate))
            return np.random.binomial(1, prob_detect)
        else:
            return False
