# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        fixed crew
# Purpose:     Initialize each fixed crew under fixed company
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

class fixed_crew:
    def __init__(self, state, parameters, config, timeseries, site, deployment_days, id):
        """
        Constructs an individual fixed crew based on defined configuration.
        """
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.site = site
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}  # Crewstate is unique to this agent
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        #self.worked_today = False
        return

    def work_a_day(self, candidate_flags):
        """
        Go to work and find the leaks for a given day
        """
        self.candidate_flags = candidate_flags

        # Sum all the emissions at the site
        leaks_present = []
        site_cum_rate = 0
        for leak in self.state['leaks']:
            if leak['facility_ID'] == self.site['facility_ID']:
                if leak['status'] == 'active':
                    if leak['days_active'] >= self.config['time_to_detection']:
                        leaks_present.append(leak)
                        site_cum_rate += leak['rate']

        # Add vented emissions
        venting = 0
        if self.parameters['consider_venting'] == True:
            venting = self.state['empirical_vents'][np.random.randint(0, len(self.state['empirical_vents']))]
            site_cum_rate += venting

        # Simple detection module based on strict minimum detection limit
        detect = False
        if site_cum_rate > (self.config['MDL']):
            detect = True

        if detect == True:
            # If source is above follow-up threshold, calculate measured rate using quantification error
            quant_error = np.random.normal(0, self.config['QE'])
            measured_rate = None
            if quant_error >= 0:
                measured_rate = site_cum_rate + site_cum_rate*quant_error
            if quant_error < 0:
                denom = abs(quant_error - 1)
                measured_rate = site_cum_rate/denom

            # If source is above follow-up threshold
            if measured_rate > self.config['follow_up_thresh']:
                # Put all necessary information in a dictionary to be assessed at end of day
                site_dict = {
                    'site': self.site,
                    'leaks_present': leaks_present,
                    'site_cum_rate': site_cum_rate,
                    'measured_rate': measured_rate,
                    'venting': venting
                }

                self.candidate_flags.append(site_dict)

        self.timeseries['fixed_cost'][self.state['t'].current_timestep] += \
            self.parameters['methods']['fixed']['cost_per_day']

        self.timeseries['total_daily_cost'][self.state['t'].current_timestep] += \
            self.parameters['methods']['fixed']['cost_per_day']

        return