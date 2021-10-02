# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.sensor.AVO
# Purpose:     Detect emissions with AVO specific methods
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


def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
    is_sp_detectable = '{}_sp_detectable'.format(self.config['name'])

    for leak in leaks_present:
        # Check if leak is spatially detectable. Keep track of initial test
        if leak[is_sp_detectable] is None:
            leak[is_sp_detectable] = np.random.binomial(1, self.config['spatial_coverage'])
        # Check if leak is temporally detectable
        is_temporal_detect = np.random.binomial(1, self.config['temporal_coverage'])
        if (leak['rate'] > self.config['MDL'][0]) \
                & bool(leak[is_sp_detectable]) & bool(is_temporal_detect):
            if leak['tagged']:
                self.timeseries[self.config['label'] +
                                '_redund_tags'][self.state['t'].current_timestep] += 1

            # Add these leaks to the 'tag pool'
            elif not leak['tagged']:
                leak['tagged'] = True
                leak['date_tagged'] = self.state['t'].current_date
                leak['tagged_by_company'] = self.config['label']
                leak['tagged_by_crew'] = self.id
        else:
            site[self.config['label'] + '_missed_leaks'] += 1

    return None
