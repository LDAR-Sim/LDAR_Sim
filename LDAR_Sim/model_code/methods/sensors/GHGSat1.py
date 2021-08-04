
# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.mobile_company
# Purpose:     Mobile company specific deployment classes and methods (ie. Scheduling)
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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
import random
from generic_functions import geo_idx


def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
    m_name = self.config['label']
    # extract the wind speed on site based on site's geo indices
    site_lat = np.float16(site['lat'])
    site_lon = np.float16(site['lon'])
    lat_idx = geo_idx(site_lat, self.state['weather'].latitude)
    lon_idx = geo_idx(site_lon, self.state['weather'].longitude)
    ti = self.state['t'].current_timestep
    windspeed = self.state['weather'].winds[ti, lat_idx, lon_idx]
    # MDL is calculated based on wind speed and parameter 
    # listed in Jacob et al., 2016
	# For point source, MDL is proportion to wind speed
	# when wind speed is 5km/h (1.39 m/s) MDL is 5.79 g/s
    Q_min = 5.79 * (1.39/windspeed)
    # set MDL to 0 for testing
    # Q_min = 0

    # check detection
    if site_true_rate > Q_min:
        # calculate the measured emission size
		# Based on Table1 of Jacob et al.,2016, the precision of 
		# GHGSat can be off by sigma (usually between 1% to 5%) 
        # sample a sigma number
        sigma = random.choice([0.01, 0.02, 0.03, 0.04, 0.05])
        site_measured_rate = site_true_rate * (1 - sigma)

        # If source is above follow-up threshold
        if site_measured_rate > self.config['follow_up_thresh']:
            # Put all necessary information in a dictionary to
            # be assessed at end of day
            site_dict = {
                'site': site,
                'leaks_present': leaks_present,
                'site_true_rate': site_true_rate,
                'site_measured_rate': site_measured_rate,
                'venting': venting
            }

    else:
        site_dict = None
        site['{}_missed_leaks'.format(m_name)] += len(leaks_present)

    return site_dict
