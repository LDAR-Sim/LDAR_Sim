# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Aircraft crew
# Purpose:     Initialize each aircraft crew under aircraft company
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

from methods.base_crew import crew 
import pandas as pd 
from generic_functions import find_homebase , get_distance, find_homebase_opt
from datetime import timedelta
import numpy as np 

class AC_Screw (crew):
    def __init__(self,state, parameters, config, timeseries, deployment_days, id):
        # Run base crew Init
        super(AC_Screw, self).__init__(state, parameters, config, timeseries, deployment_days, id)
        # Check if scheduling
        m_name = self.config['name']
        self.scheduling  = parameters['methods'][m_name]['scheduling']
        # Read in the homebases as a list of dictionaries 
        homebases = parameters['working_directory'] + self.scheduling['home_bases']
        HB = pd.read_csv(homebases,sep=',')
        self.state['homebases'] = HB
        # get lat & lon of all homebases 
        self.HX = self.state['homebases']['lon']
        self.HY = self.state['homebases']['lat']
        
        # initiate the location of LDAR crew  
        self.state['current_x']= self.scheduling['LDAR_crew_init_location'][0]
        self.state['current_y']= self.scheduling['LDAR_crew_init_location'][1]
            
    
    def work_a_day(self, candidate_flags):
        """
        Go to work and find the leaks for a given day
        """
        m_name = self.config['name']
        self.worked_today = False
        self.candidate_flags = candidate_flags
        work_hours = None
        max_work = self.parameters['methods'][m_name]['max_workday']

        if self.parameters['methods'][m_name]['consider_daylight']:
            daylight_hours = self.state['daylight'].get_daylight(self.state['t'].current_timestep)
            if daylight_hours <= max_work:
                work_hours = daylight_hours
            elif daylight_hours > max_work:
                work_hours = max_work
        else:
            work_hours = max_work

        if work_hours < 24 and work_hours != 0:
            start_hour = (24 - work_hours) / 2
            end_hour = start_hour + work_hours
        else:
            print(
                'Unreasonable number of work hours specified for Aircraft crew ' +
                str(self.crewstate['id']))

        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(start_hour))  # Set start of work day
        
        if self.scheduling['geography']:
            # start day by reading location of the LDAR team 
            x_LDAR = self.state['current_x']
            y_LDAR = self.state['current_y']
    
            while self.state['t'].current_date.hour < int(end_hour):
                facility_ID, found_site, site, travel_time = self.choose_site(x_LDAR,y_LDAR)
                if not found_site:
                    Home,DIST = find_homebase(x_LDAR,y_LDAR,self.HX,self.HY) 
                    x_LDAR = Home[0]
                    y_LDAR = Home[1]
                    self.state['current_x'] = x_LDAR
                    self.state['current_y'] = y_LDAR
                    break  # Break out  
                
                self.state['t'].current_date += timedelta(minutes= travel_time)
                if self.state['t'].current_date.hour > int(end_hour):
                    x_temp = np.float(site['lon'])
                    y_temp = np.float(site['lat'])
                    x_cut = self.state['current_x'] 
                    y_cut = self.state['current_y']
                    Home,DIST = find_homebase_opt(x_temp,y_temp,x_cut,y_cut,self.HX,self.HY)
                    
                    self.state['current_x'] = Home[0]
                    self.state['current_y'] = Home[1]
                    break 
                else:
                    x_LDAR = np.float(site['lon'])
                    y_LDAR = np.float(site['lat'])
                    self.visit_site(site)
                self.worked_today = True
                    
        else: 
            # Start day with a time increment required for flying to first site
            self.state['t'].current_date += timedelta(minutes=int(self.config['t_bw_sites']))
    
            while self.state['t'].current_date.hour < int(end_hour):
                facility_ID, found_site, site = self.choose_site(0,0)
                if not found_site:
                    break  # Break out if no site can be found
                self.visit_site(site)
            self.worked_today = True

    
        if self.worked_today:
            self.timeseries['{}_cost'.format(m_name)][self.state['t'].current_timestep] += \
                self.parameters['methods'][m_name]['cost_per_day']
            self.timeseries['total_daily_cost'][self.state['t'].current_timestep] += \
                self.parameters['methods'][m_name]['cost_per_day']

        return

    def choose_site(self,x_LDAR,y_LDAR):
        """
        Choose a site to survey.

        """
        m_name = self.config['name']
        # Sort all sites based on a neglect ranking
        self.state['sites'] = sorted(
            self.state['sites'],
            key=lambda k: k['{}_t_since_last_LDAR'.format(m_name)],
            reverse=True)

        facility_ID = None  # The facility ID gets assigned if a site is found
        found_site = False  # The found site flag is updated if a site is found
        travel_time = None
        site = None
        Site_T = [] 
        s_list = []
        SP_list = self.parameters['methods'][m_name]['scheduling']['Speed_list']
        speed = np.random.choice(SP_list)

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in self.state['sites']:
            s_list.append(site)
            x_site = np.float(site['lon'])
            y_site = np.float(site['lat'])
            
            # if the site was assigned to this agent
            if site['label'] + 1 == self.crewstate['id']:
                # If the site hasn't been attempted yet today
                if not site['{}_attempted_today?'.format(m_name)]:
    
                    # If the site is 'unripened' (i.e. hasn't met the minimum interval set
                    # out in the LDAR regulations/policy), break out - no LDAR today
                    if site['{}_t_since_last_LDAR'.format(m_name)] < int(site['aircraft_min_int']):
                        self.state['t'].current_date = self.state['t'].current_date.replace(hour=23)
                        break
    
                    # Else if site-specific required visits have not been met for the year
                    elif site['{}_surveys_done_this_year'.format(m_name)] < int(site['aircraft_RS']):
    
                        # Check the weather for that site
                        if self.deployment_days[site['lon_index'],
                                                site['lat_index'],
                                                self.state['t'].current_timestep]:
                            
                             if self.scheduling['geography']: 
                                d = get_distance(x_LDAR,y_LDAR,x_site,y_site,"Euclidian")
                                wt = d/speed * 60
                                Site_T.append(wt)
                                if not self.scheduling['route_planning']: 
                                    # The site passes all the tests! Choose it!
                                    travel_time = wt
                                    facility_ID = site['facility_ID']
                                    found_site = True
            
                                    # Update site
                                    site['{}_surveys_conducted'.format(m_name)] += 1
                                    site['{}_surveys_done_this_year'.format(m_name)] += 1
                                    site['{}_t_since_last_LDAR'.format(m_name)] = 0
                                    break
                             else: 
                                # The site passes all the tests! Choose it!
                                facility_ID = site['facility_ID']
                                found_site = True
        
                                # Update site
                                site['{}_surveys_conducted'.format(m_name)] += 1
                                site['{}_surveys_done_this_year'.format(m_name)] += 1
                                site['{}_t_since_last_LDAR'.format(m_name)] = 0
                                break
    
                        else:
                            site['{}_attempted_today?'.format(m_name)] = True
                        
        if self.scheduling['route_planning']:
            if len(Site_T) > 0: 
                j = Site_T.index(min(Site_T))
                site = s_list[j]
                facility_ID = site['facility_ID']
                travel_time = min(Site_T)*60
                found_site = True
                
                # Update site
                site['{}_surveys_conducted'.format(m_name)] += 1
                site['{}_surveys_done_this_year'.format(m_name)] += 1
                site['{}_t_since_last_LDAR'.format(m_name)] = 0

        if self.scheduling['geography'] or self.scheduling['route_planning']:        
            return (facility_ID, found_site, site, travel_time)
        else:
            return (facility_ID, found_site, site)