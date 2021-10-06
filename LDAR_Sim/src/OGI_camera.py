# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        OGI general
# Purpose:     General OGI that any crew can call
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
import math


class OGI_camera:
    def __init__(self, state, parameters, config, timeseries, crewstate):
        """
        Constructs an OGI camera then any crew can use.
        Should not be used for technologies that are not on site (e.g., satellite, aircraft)
        """
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crewstate = crewstate
        self.MDL = config['sensor']['MDL']

        return

    def detect_leaks(self, site, leaks):
        for leak in leaks:
            k = np.random.normal(4.9, 0.3)
            x0 = np.random.normal(self.MDL[0], self.MDL[1])
            x0 = math.log10(x0 * 3600)  # Convert from g/s to g/h and take log

            if leak['rate'] == 0:
                prob_detect = 0
            else:
                x = math.log10(leak['rate'] * 3600)  # Convert from g/s to g/h
                prob_detect = 1 / (1 + math.exp(-k * (x - x0)))
            detect = np.random.binomial(1, prob_detect)

            if detect:
                if leak['tagged']:
                    self.timeseries[self.config['label'] +
                                    '_redund_tags'][self.state['t'].current_timestep] += 1

                # Add these leaks to the 'tag pool'
                elif not leak['tagged']:
                    leak['tagged'] = True
                    leak['date_tagged'] = self.state['t'].current_date
                    leak['tagged_by_company'] = self.config['label']
                    leak['tagged_by_crew'] = self.crewstate['id']
                    self.state['tags'].append(leak)

            elif not detect:
                site[self.config['label'] + '_missed_leaks'] += 1

        return
