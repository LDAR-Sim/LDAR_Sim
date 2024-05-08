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

"""
User input:
    MDL values: [
        threshold - threshold for detection,
        prob_detect - probability of detection at threshold
    ]
"""


class CustomThreshold(DefaultComponentLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)
        self._mdl = mdl

    def _rate_detected(self, emis_rate: float) -> bool:
        threshold = self._mdl[0]
        prob_detect = self._mdl[1]
        if emis_rate >= threshold:
            return np.random.binomial(1, prob_detect)
        else:
            return False
