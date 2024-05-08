"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        Mobile_pipeline
Purpose: Provides a probability of detection curve based on the following paper
       https://doi.org/10.1016/j.envpol.2022.120027


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
PoD = 1/(1+exp(-(5.0221+0.139q - 0.1498c - 0.057s - (12.7024/L) - 0.4115U - 0.0807T )))

Where: 
    q = leak rate in grams per minute
    c = survey speed (mph)
    s = survey distance (m)
    L = Monin-Obukhov length
    U = wind speed (m/s)
    T = temperature (C)

User input:
MDL values: [
    c - survey speed (mph),
    s - survey distance (m),
    L - Monin-Obukhov length,
    U - wind speed (m/s),
]
** If using optional values, the user must provide all optional values
"""

SECONDTOMINUTE = 60


class MobilePipeline(DefaultComponentLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)

    def _rate_detected(self, emis_rate: float) -> bool:
        T = 15  # temperature in Celsius
        c = self._mdl[0]
        s = self._mdl[1]
        L = self._mdl[2]
        U = self._mdl[3]
        emis_rate = emis_rate * SECONDTOMINUTE
        # check how many inputs users provided

        prob_detect = 1 / (
            1
            + np.exp(
                -(
                    5.0221
                    + 0.139 * emis_rate
                    - 0.1498 * c
                    - 0.057 * s
                    - (12.7024 * L)
                    - 0.4115 * U
                    - 0.0807 * T
                )
            )
        )
        if prob_detect >= 1:
            return True
        return np.random.binomial(1, prob_detect)


class MobilePipelineTruck(DefaultComponentLevelSensor):
    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)
        self._mdl = mdl

    def _rate_detected(self, emis_rate: float) -> bool:
        T = 15  # temperature in Celsius
        c = self._mdl[0]
        s = self._mdl[1]
        L = self._mdl[2]
        U = self._mdl[3]
        emis_rate = emis_rate * SECONDTOMINUTE
        # check how many inputs users provided

        prob_detect = 1 / (
            1
            + np.exp(
                -(
                    5.0221
                    + 0.139 * emis_rate
                    - 0.1498 * c
                    - 0.057 * s
                    - (12.7024 * L)
                    - 0.4115 * U
                    - 0.0807 * T
                )
            )
        )
        if prob_detect >= 1:
            return True
        rolls = np.random.binomial(1, prob_detect, 6)
        if 1 in rolls:
            return 1
        else:
            return 0
