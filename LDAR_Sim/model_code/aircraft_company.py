# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Aircraft company
# Purpose:     Company managing aircraft agents
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

from aircraft_crew import *
from weather_lookup import *
import numpy as np
from generic_functions import get_prop_rate

class aircraft_company:
    def __init__(self, state, parameters, config, timeseries):
        """
        Initialize a company to manage the aircraft crews (e.g. a contracting company).

        """
        self.name = 'aircraft'
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days('aircraft')
        self.timeseries['aircraft_prop_sites_avail'] = []
        self.timeseries['aircraft_cost'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['aircraft_eff_flags'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['aircraft_flags_redund1'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['aircraft_flags_redund2'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['aircraft_flags_redund3'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['aircraft_sites_visited'] = np.zeros(self.parameters['timesteps'])

        # Assign the correct follow-up threshold
        if self.config['follow_up_thresh'][1] == "absolute":
            self.config['follow_up_thresh'] = self.config['follow_up_thresh'][0]
        elif self.config['follow_up_thresh'][1] == "proportion":
            self.config['follow_up_thresh'] = get_prop_rate(self.config['follow_up_thresh'][0], self.state['empirical_leaks'])
        else:
            print('Follow-up threshold type not recognized. Must be "absolute" or "proportion".')

        # Additional variable(s) for each site       
        for site in self.state['sites']:
            site.update({'aircraft_t_since_last_LDAR': 0})
            site.update({'aircraft_surveys_conducted': 0})
            site.update({'attempted_today_aircraft?': False})
            site.update({'surveys_done_this_year_aircraft': 0})
            site.update({'aircraft_missed_leaks': 0})

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros((len(self.state['weather'].longitude), len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros((len(self.state['weather'].longitude), len(self.state['weather'].latitude)))

        # Initialize the individual aircraft crews (the agents)
        for i in range(config['n_crews']):
            self.crews.append(aircraft_crew(state, parameters, config, timeseries, self.deployment_days, id=i + 1))

        return

    def find_leaks(self):
        """
        The aircraft company tells all the crews to get to work.
        """

        for i in self.crews:
            i.work_a_day()

        # Update method-specific site variables each day
        for site in self.state['sites']:
            site['aircraft_t_since_last_LDAR'] += 1
            site['attempted_today_aircraft?'] = False

        if self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
            for site in self.state['sites']:
                site['surveys_done_this_year_aircraft'] = 0

        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep]:
                available_sites += 1
        prop_avail = available_sites / len(self.state['sites'])
        self.timeseries['aircraft_prop_sites_avail'].append(prop_avail)

        return

    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs) for each site.
        """

        for site in self.state['sites']:
            site['aircraft_prop_DDs'] = self.DD_map[site['lon_index'], site['lat_index']]
            site['aircraft_MCB'] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
