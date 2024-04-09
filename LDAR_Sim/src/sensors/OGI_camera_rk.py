"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        OGI_camera_rk
Purpose: Provides an OGI camera sensor detection based on a 
sigmoidal Gaussian cumulative probability function as described in Ravikumar et al. (2018)

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

import math
import numpy as np
from sensors.default_equipment_level_sensor import DefaultEquipmentLevelSensor
from constants.general_const import Conversion_Constants as CC


class OGICameraRKSensor(DefaultEquipmentLevelSensor):
    MDL_CONST1 = 0.01275
    MDL_CONST2 = 0.00000278

    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)

    def _rate_detected(self, emis_rate: float) -> bool:
        k = np.random.normal(4.9, 0.3)
        # check if users are providing their own overwrite to the curve
        if len(self._mdl) < 2:
            x0 = np.random.normal(OGICameraRKSensor.MDL_CONST1, OGICameraRKSensor.MDL_CONST2)
        else:
            x0 = np.random.normal(self._mdl[0], self._mdl[1])
        x0 = math.log10(x0 * CC.GS_TO_GH)
        if emis_rate == 0:
            return False

        x = math.log10(emis_rate * CC.GS_TO_GH)
        prob_detect = 1 / (1 + math.exp(-k * (x - x0)))

        return np.random.binomial(1, prob_detect) and self.check_min_threshold(emis_rate)
