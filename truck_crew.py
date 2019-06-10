import numpy as np
from datetime import timedelta
import math
import numpy as np

class truck_crew:
    def __init__ (self, state, parameters, config, timeseries, deployment_days, id):
        '''
        Constructs an individual truck crew based on defined configuration.
        '''
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}     # Crewstate is unique to this agent
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
        max_work = self.parameters['methods']['truck']['max_workday']
        
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
            print('Unreasonable number of work hours specified for truck crew ' + str(self.crewstate['id']))
               
        self.state['t'].current_date = self.state['t'].current_date.replace(hour = int(start_hour))              # Set start of work day
        while self.state['t'].current_date.hour < int(end_hour):
            facility_ID, found_site, site = self.choose_site ()
            if not found_site:
                break                                   # Break out if no site can be found
            self.visit_site (facility_ID, site)
            self.worked_today = True
        
        if self.worked_today == True:
            self.timeseries['truck_cost'][self.state['t'].current_timestep] += self.parameters['methods']['truck']['cost_per_day']

        return


    def choose_site (self):
        '''
        Choose a site to survey.

        '''
            
        # Sort all sites based on a neglect ranking
        self.state['sites'] = sorted(self.state['sites'], key=lambda k: k['t_since_last_LDAR_truck'], reverse = True)

        facility_ID = None                                  # The facility ID gets assigned if a site is found
        found_site = False                                  # The found site flag is updated if a site is found

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in self.state['sites']:

            # If the site hasn't been attempted yet today
            if site['attempted_today_truck?'] == False:
            
                # If the site is 'unripened' (i.e. hasn't met the minimum interval set out in the LDAR regulations/policy), break out - no LDAR today
                if site['t_since_last_LDAR_truck'] < self.parameters['methods']['truck']['min_interval']:
                    self.state['t'].current_date = self.state['t'].current_date.replace(hour = 23)
                    break
    
                # Else if site-specific required visits have not been met for the year
                elif site['surveys_done_this_year_truck'] < int(site['required_surveys_truck']):
    
                    # Check the weather for that site
                    if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                    
                        # The site passes all the tests! Choose it!
                        facility_ID = site['facility_ID']   
                        found_site = True
    
                        # Update site
                        site['surveys_conducted_truck'] += 1
                        site['surveys_done_this_year_truck'] += 1
                        site['t_since_last_LDAR_truck'] = 0
                        break
                                            
                    else:
                        site['attempted_today_truck?'] = True

        return (facility_ID, found_site, site)

    def visit_site (self, facility_ID, site):
        '''
        Look for emissions at the chosen site.
        '''

        # Sum all the emissions at the site
        leaks_present = []
        site_cum_rate = 0
        for leak in self.state['leaks']:
            if leak['facility_ID'] == facility_ID:
                if leak['status'] == 'active':
                    leaks_present.append(leak)
                    site_cum_rate += leak['rate']  
                    
        # Add vented emissions
        if self.parameters['consider_venting'] == True:
            venting = self.state['empirical_vents'][np.random.randint(0, len(self.state['empirical_vents']))]
            site_cum_rate += venting
                    
        # Simple detection module based optimistically on Fox et al 2019 lower bound (lit review)
        detect = False
        if site_cum_rate > (6*0.024):  # g/hour to kg/day
            detect = True    
        
        if detect == True:
            # If source is above follow-up threshold
            if site_cum_rate > self.config['follow_up_thresh']:
                
                # If the site is already flagged, your flag is redundant
                if site['currently_flagged'] == True:
                    self.timeseries['truck_flags_redund1'][self.state['t'].current_timestep] += 1
                
                elif site['currently_flagged'] == False:
                    # Flag the site for follow up
                    site['currently_flagged'] = True
                    site['date_flagged'] = self.state['t'].current_date
                    self.timeseries['truck_eff_flags'][self.state['t'].current_timestep] += 1
                    
                    # Does the chosen site already have tagged leaks?
                    redund2 = False
                    for leak in leaks_present:
                        if leak['date_found'] != None:
                            redund2 = True
                            
                    if redund2 == True:
                        self.timeseries['truck_flags_redund2'][self.state['t'].current_timestep] += 1
                    
                    # Would the site have been chosen without venting?
                    if (site_cum_rate - venting) < self.config['follow_up_thresh']:
                        self.timeseries['truck_flags_redund3'][self.state['t'].current_timestep] += 1
                
        elif detect == False:
            site['missed_leaks_truck'] += len(leaks_present)
                
        self.state['t'].current_date += timedelta(minutes = int(site['truck_time']))
