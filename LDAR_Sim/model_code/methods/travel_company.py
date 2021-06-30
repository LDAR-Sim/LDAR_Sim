# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Travel Base Company
# Purpose:     Company managing crew agents agents
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
import pandas as pd
from sklearn.cluster import KMeans

from methods.base_company import company as base_company


class travel_company(base_company):
    """
    """

    def __init__(self, state, parameters, config, timeseries):
        super(travel_company, self).__init__(state, parameters, config, timeseries)
        # --- Travel / Scheduling Specific Initializiation ---

        for site in self.state['sites']:
            site.update({'{}_t_since_last_LDAR'.format(self.name): 0})
            site.update({'{}_surveys_conducted'.format(self.name): 0})
            site.update({'{}_attempted_today?'.format(self.name): False})
            site.update({'{}_surveys_done_this_year'.format(self.name): 0})
            site.update({'{}_missed_leaks'.format(self.name): 0})

        # Use clustering analysis to assign facilities to each agent, if 2+ agents are aviable
        if self.config['n_crews'] > 1:
            lats = []
            lons = []
            ID = []
            for site in self.state['sites']:
                ID.append(site['facility_ID'])
                lats.append(site['lat'])
                lons.append(site['lon'])
            # HBD - What is sdf?
            sdf = pd.DataFrame({"ID": ID,
                                'lon': lons,
                                'lat': lats})
            locs = sdf[['lat', 'lon']].values
            num = config['n_crews']
            kmeans = KMeans(n_clusters=num, random_state=0).fit(locs)
            label = kmeans.labels_
        else:
            label = np.zeros(len(self.state['sites']))

        for i in range(len(self.state['sites'])):
            self.state['sites'][i]['label'] = label[i]

    # --- Travel / Scheduling Specific Methods ---
    def find_leaks(self):
        super(travel_company, self).find_leaks()

        # Update travel specific variables
        for site in self.state['sites']:
            site['{}_t_since_last_LDAR'.format(self.name)] += 1
            site['{}_attempted_today?'.format(self.name)] = False

        if self.config['is_follow_up']:
            self.state['flags'] = [flag for flag in self.state['sites']
                                   if flag['currently_flagged']]
        elif self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
            for site in self.state['sites']:
                site['{}_surveys_done_this_year'.format(self.name)] = 0
