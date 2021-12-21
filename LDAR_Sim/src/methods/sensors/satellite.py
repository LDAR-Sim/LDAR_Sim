# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.GHGSat1
# Purpose:     GHGSat1 company specific deployment classes and methods
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

import random

import numpy as np
from utils.generic_functions import geo_idx


def detect_emissions(self, site, covered_leaks, covered_equipment_rates, covered_site_rate,
                     site_rate, venting, equipment_rates):
    equip_measured_rates = []
    site_measured_rate = 0
    found_leak = False
    n_leaks = len(covered_leaks)
    missed_leaks_str = '{}_missed_leaks'.format(self.config['label'])
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
    Q_min = self.config['sensor']['MDL'][0] * (self.config['sensor']['MDL'][1]/windspeed)

    # check detection
    if covered_site_rate > Q_min:
        # calculate the measured emission size
        # Based on Table1 of Jacob et al.,2016, the precision of
        # GHGSat can be off by sigma (usually between 1% to 5%)
        # sample a sigma number
        sigma = random.choice([0.01, 0.02, 0.03, 0.04, 0.05])
        site_measured_rate = covered_site_rate * (1 - sigma)
        found_leak = True

    else:
        site_dict = None
        site[missed_leaks_str] += n_leaks
        self.timeseries[missed_leaks_str][self.state['t'].current_timestep] += n_leaks

    site_dict = {
        'site': site,
        'leaks_present': covered_leaks,
        'site_true_rate': site_rate,
        'site_measured_rate': site_measured_rate,
        'equip_measured_rates': equip_measured_rates,
        'vent_rate': venting,
        'found_leak': found_leak,
    }

    return site_dict
