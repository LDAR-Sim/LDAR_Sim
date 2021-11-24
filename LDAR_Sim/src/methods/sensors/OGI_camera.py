# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.OGI_Camera
# Purpose:     OGI company specific deployment classes and methods based on RK (2018)
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

import math
import numpy as np
from utils.attribution import update_tag


def detect_emissions(self, site, covered_leaks, covered_equipment_rates, covered_site_rate,
                     site_rate, venting, equipment_rates):

    for leak in covered_leaks:
        k = np.random.normal(4.9, 0.3)
        x0 = np.random.normal(self.config['sensor']['MDL'][0], self.config['sensor']['MDL'][1])
        x0 = math.log10(x0 * 3600)  # Convert from g/s to g/h and take log

        if leak['rate'] == 0:
            prob_detect = 0
        else:
            x = math.log10(leak['rate'] * 3600)  # Convert from g/s to g/h
            prob_detect = 1 / (1 + math.exp(-k * (x - x0)))

        if np.random.binomial(1, prob_detect):
            update_tag(leak, site, self.timeseries, self.state['t'],
                       self.state['campaigns'], self.config['label'], self.id)
        else:
            site[self.config['label'] + '_missed_leaks'] += 1

    return None
