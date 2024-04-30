"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        OGI_camera_zim
Purpose: Provides an OGI camera sensor detection based on Zimmerle 2020 
DOI 10.1021/acs.est.0c01285
uses power function as shown in figure 2 to calculate probability of
detection using leak size, and two mdl parameters are set based on camera
crew experience.

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

MDL_CONST1 = 0.24
MDL_CONST2 = 0.39
GS_TO_SCFH = 187


class OGICameraZimSensor(DefaultComponentLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)
        self._mdl = mdl

    def _rate_detected(self, emis_rate: float) -> bool:
        # check that the user provided an overwrite to the MDL values
        # otherwise, use the defaults
        if len(self._mdl) < 2:
            prob_detect = MDL_CONST1 * (GS_TO_SCFH * emis_rate) ** MDL_CONST2
        else:
            prob_detect = self._mdl[0] * (GS_TO_SCFH * emis_rate) ** self._mdl[1]
        if prob_detect >= 1:
            return True
        return np.random.binomial(1, prob_detect) and self.check_min_threshold(emis_rate)
