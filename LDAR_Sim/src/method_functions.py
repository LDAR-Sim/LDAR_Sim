# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

import numpy as np


def measured_rate(true_rate, QE):
    quant_error = np.random.normal(0, QE)
    measured_rate = None
    if quant_error >= 0:
        measured_rate = true_rate + true_rate * quant_error
    if quant_error < 0:
        denom = abs(quant_error - 1)
        measured_rate = true_rate / denom

    return measured_rate
