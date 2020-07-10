# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Truck company
# Purpose:     Company managing truck agents
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ------------------------------------------------------------------------------

from truck_crew import *
from weather_lookup import *
import numpy as np

class truck_company:
    def __init__(self, state, parameters, config, timeseries):
        """
        Initialize a company to manage the truck crews (e.g. a contracting company).

        """
        self.name = 'truck'
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days('truck')
        self.timeseries['truck_prop_sites_avail'] = []
        self.timeseries['truck_cost'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['truck_eff_flags'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['truck_flags_redund1'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['truck_flags_redund2'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['truck_flags_redund3'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['truck_sites_visited'] = np.zeros(self.parameters['timesteps'])

        # Additional variable(s) for each site       
        for site in self.state['sites']:
            site.update({'truck_t_since_last_LDAR': 0})
            site.update({'truck_surveys_conducted': 0})
            site.update({'attempted_today_truck?': False})
            site.update({'surveys_done_this_year_truck': 0})
            site.update({'truck_missed_leaks': 0})

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros((len(self.state['weather'].longitude), len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros((len(self.state['weather'].longitude), len(self.state['weather'].latitude)))

        # Initialize the individual truck crews (the agents)
        for i in range(config['n_crews']):
            self.crews.append(truck_crew(state, parameters, config, timeseries, self.deployment_days, id=i + 1))

        return

    def find_leaks(self):
        """
        The truck company tells all the crews to get to work.
        """

        for i in self.crews:
            i.work_a_day()

        # Update method-specific site variables each day
        for site in self.state['sites']:
            site['truck_t_since_last_LDAR'] += 1
            site['attempted_today_truck?'] = False

        if self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
            for site in self.state['sites']:
                site['surveys_done_this_year_truck'] = 0

        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep]:
                available_sites += 1
        prop_avail = available_sites / len(self.state['sites'])
        self.timeseries['truck_prop_sites_avail'].append(prop_avail)

        return

    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs) for each site.
        """

        for site in self.state['sites']:
            site['truck_prop_DDs'] = self.DD_map[site['lon_index'], site['lat_index']]
            site['truck_MCB'] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
