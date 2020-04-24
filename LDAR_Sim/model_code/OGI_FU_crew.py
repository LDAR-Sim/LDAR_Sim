#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        OGI follow-up crew
# Purpose:     Initialize each follow-up crew under OGI follow-up company
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
#------------------------------------------------------------------------------

import numpy as np
from datetime import timedelta
import math
import numpy as np

class OGI_FU_crew:
    def __init__ (self, state, parameters, config, timeseries, deployment_days, id):
        '''
        Constructs an individual OGI_FU crew based on defined configuration.
        '''
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        self.worked_today = False
        return

    def work_a_day (self):
        '''
        Go to work and find the leaks for a given day
        '''
        self.worked_today = False
        work_hours = None
        max_work = self.parameters['methods']['OGI_FU']['max_workday']
        
        if self.parameters['consider_daylight'] == True:
            daylight_hours = self.state['daylight'].get_daylight(self.state['t'].current_timestep)
            if daylight_hours <= max_work:
                work_hours = daylight_hours
            elif daylight_hours > max_work:
                work_hours = max_work
        elif self.parameters['consider_daylight'] == False:
            work_hours = max_work
        
        if work_hours < 24 and work_hours != 0:
            start_hour = (24 - work_hours) / 2
            end_hour = start_hour + work_hours
        else:
            print('Unreasonable number of work hours specified for OGI Follow-up crew ' + str(self.crewstate['id']))
               
        self.state['t'].current_date = self.state['t'].current_date.replace(hour = int(start_hour))              # Set start of work day
        while self.state['t'].current_date.hour < int(end_hour):
            facility_ID, found_site, site = self.choose_site ()
            if not found_site:
                break                                   # Break out if no site can be found
            self.visit_site (facility_ID, site)
            self.worked_today = True
        
        if self.worked_today == True:
            self.timeseries['OGI_FU_cost'][self.state['t'].current_timestep] += self.parameters['methods']['OGI_FU']['cost_per_day']

        return


    def choose_site (self):
        '''
        Choose a site to follow up.

        '''
        # Sort flagged sites based on a neglect ranking
        self.state['flags'] = sorted(self.state['flags'], key=lambda k: k['OGI_FU_t_since_last_LDAR'], reverse = True)
        facility_ID = None                                  # The facility ID gets assigned if a site is found
        found_site = False                                  # The found site flag is updated if a site is found      

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        if len(self.state['flags']) == 0:
            site = None
        
        if len(self.state['flags']) > 0: 
            for site in self.state['flags']:
                
                # If the site is ripe
                if (self.state['t'].current_date - site['date_flagged']).days  >= self.parameters['methods'][site['flagged_by']]['reporting_delay']:
    
                    # If the site hasn't been attempted yet today
                    if site['attempted_today_OGI_FU?'] == False:
                            
                        # Check the weather for that site
                        if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                        
                            # The site passes all the tests! Choose it!
                            facility_ID = site['facility_ID']   
                            found_site = True
        
                            # Update site
                            site['OGI_FU_surveys_conducted'] += 1
                            site['OGI_FU_t_since_last_LDAR'] = 0   
                            site['attempted_today_OGI_FU?'] = True                                 
                            break
                                                
                        else:
                            site['attempted_today_OGI_FU?'] = True

        return (facility_ID, found_site, site)

    def visit_site (self, facility_ID, site):
        '''
        Look for leaks at the chosen site.
        '''

        # Identify all the leaks at a site
        leaks_present = []
        for leak in self.state['leaks']:
            if leak['facility_ID'] == facility_ID:
                if leak['status'] == 'active':
                    leaks_present.append(leak)

        # Detection module from Ravikumar et al 2018, assuming 3 m distance
        for leak in leaks_present:
            k = np.random.normal(4.9, 0.3)
            x0 = np.random.normal(self.config['MDL'][0], self.config['MDL'][1])
            if leak['rate'] == 0:
                prob_detect = 0
            else:
                x = math.log10(leak['rate']*41.6667)            # Convert from kg/day to g/h
                prob_detect = 1/(1 + math.exp(-k*(x-x0)))
            detect = np.random.binomial(1, prob_detect)
            
            if detect == True:
                if leak['tagged'] == True:
                    self.timeseries['OGI_FU_redund_tags'][self.state['t'].current_timestep] += 1 
               
                # Add these leaks to the 'tag pool'
                elif leak['tagged'] == False:
                    leak['tagged'] = True
                    leak['date_found'] = self.state['t'].current_date
                    leak['found_by_company'] = self.config['name']
                    leak['found_by_crew'] = self.crewstate['id']
                    self.state['tags'].append(leak)
                
            elif detect == False:
                site['OGI_FU_missed_leaks'] += 1
                
        self.state['t'].current_date += timedelta(minutes = int(site['OGI_FU_time']))
        self.state['t'].current_date += timedelta(minutes = int(self.state['offsite_times'][np.random.randint(0, len(self.state['offsite_times']))]))
        self.timeseries['OGI_FU_sites_visited'][self.state['t'].current_timestep] += 1

        # Remove site from flag pool
        site['currently_flagged'] = False
     
        return
