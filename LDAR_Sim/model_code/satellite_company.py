# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Satellite company
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


import numpy as np
from orbit_predictor.sources import get_predictor_from_tle_lines
import netCDF4 as nc


class satellite_company:
    def __init__(self, state, parameters, config, timeseries):
        """
        Initialize a company to manage the satellite
        """
        self.name = 'satellite'
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days('satellite')
        self.timeseries['satellite_prop_sites_avail'] = []
        self.timeseries['satellite_cost'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['satellite_eff_flags'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['satellite_flags_redund1'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['satellite_flags_redund2'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['satellite_flags_redund3'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['satellite_sites_visited'] = np.zeros(self.parameters['timesteps'])
		
		
		# load pre-defined orbit grids 
        Dataset = nc.Dataset(self.parameters['methods']['Satellite']['Satellite_grid'],'r')
        self.satgrid = Dataset.variables['sat'][:]
        Dataset.close()
        
        # load cloud cover data
        Dataset = nc.Dataset(self.parameters['methods']['Satellite']['CloudCover'],'r')
        self.cloudcover = Dataset.variables['tcc'][:]
        Dataset.close()
        
        
        # build a satellite orbit object 
        sat = self.parameters['methods']['Satellite']['name']
        tlefile = self.parameters['methods']['Satellite']['TLE_file']
        TLEs = []  
        with open(tlefile) as f:
            for line in f:
                TLEs.append(line.rstrip())   

        i = 0 
        for x in TLEs: 
            if x == sat: 
                break
            i+=1
        TLE_LINES = (TLEs[i+1],TLEs[i+2])
        
        self.predictor = get_predictor_from_tle_lines(TLE_LINES)
        
        return
    

        # Assign the correct follow-up threshold
        if self.config['follow_up_thresh'][1] == "absolute":
            self.config['follow_up_thresh'] = self.config['follow_up_thresh'][0]
        elif self.config['follow_up_thresh'][1] == "proportion":
            self.config['follow_up_thresh'] = get_prop_rate(
                self.config['follow_up_thresh'][0],
                self.state['empirical_leaks'])
        else:
            print('Follow-up threshold type not recognized. Must be "absolute" or "proportion".')

        # Additional variable(s) for each site
        for site in self.state['sites']:
            site.update({'satellite_t_since_last_LDAR': 0})
            site.update({'satellite_surveys_conducted': 0})
            site.update({'attempted_today_satellite?': False})
            site.update({'surveys_done_this_year_satellite': 0})
            site.update({'satellite_missed_leaks': 0})

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros(
            (len(self.state['weather'].longitude),
              len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros(
            (len(self.state['weather'].longitude),
              len(self.state['weather'].latitude)))

         # Initialize the individual aircraft crews (the agents)
        for i in range(config['n_crews']):
            self.crews.append(Satellite(state, parameters, config,
                                             timeseries, self.deployment_days, id=i + 1))

        return


    def find_leaks(self):
        """
        The satellite company tells all the crews to get to work.
        """

        self.candidate_flags = []
        for i in self.crews:
            i.work_a_day(self.candidate_flags)

        # Flag sites according to the flag ratio
        if len(self.candidate_flags) > 0:
            self.flag_sites()

        # Update method-specific site variables each day
        for site in self.state['sites']:
            site['satellite_t_since_last_LDAR'] += 1
            site['attempted_today_satellite?'] = False

        if self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
            for site in self.state['sites']:
                site['surveys_done_this_year_satellite'] = 0

        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'],
                                    site['lat_index'],
                                    self.state['t'].current_timestep]:
                available_sites += 1
        prop_avail = available_sites / len(self.state['sites'])
        self.timeseries['aircraft_prop_sites_avail'].append(prop_avail)

        return


    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs)
        for each site.
        """

        for site in self.state['sites']:
            site['satellite_prop_DDs'] = self.DD_map[site['lon_index'], site['lat_index']]
            site['satellite_MCB'] = self.MCB_map[site['lon_index'], site['lat_index']]

        return