import numpy as np
from datetime import timedelta
import math
import numpy as np

class aircraft_crew:
    def __init__ (self, state, parameters, config, timeseries, deployment_days, id):
        '''
        Constructs an individual aircraft crew based on defined configuration.
        '''
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}     # Crewstate is unique to this agent
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        return

    def work_a_day (self):
        '''
        Go to work and find the leaks for a given day
        '''
        self.state['t'].current_date = self.state['t'].current_date.replace(hour = 8)              # Set start of work day
        while self.state['t'].current_date.hour < 18:
            facility_ID, found_site, site = self.choose_site ()
            if not found_site:
                break                                   # Break out if no site can be found
            self.visit_site (facility_ID, site)

        return


    def choose_site (self):
        '''
        Choose a site to survey.

        '''
            
        # Sort all sites based on a neglect ranking
        self.state['sites'] = sorted(self.state['sites'], key=lambda k: k['t_since_last_LDAR_aircraft'], reverse = True)

        facility_ID = None                                  # The facility ID gets assigned if a site is found
        found_site = False                                  # The found site flag is updated if a site is found

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in self.state['sites']:

            # If the site hasn't been attempted yet today
            if site['attempted_today_aircraft?'] == False:
            
                # If the site is 'unripened' (i.e. hasn't met the minimum interval set out in the LDAR regulations/policy), break out - no LDAR today
                if site['t_since_last_LDAR_aircraft'] < self.parameters['methods']['aircraft']['min_interval']:
                    self.state['t'].current_date = self.state['t'].current_date.replace(hour = 23)
                    break
    
                # Else if site-specific required visits have not been met for the year
                elif site['surveys_done_this_year_aircraft'] < int(site['required_surveys_aircraft']):
    
                    # Check the weather for that site
                    if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                    
                        # The site passes all the tests! Choose it!
                        facility_ID = site['facility_ID']   
                        found_site = True
    
                        # Update site
                        site['surveys_conducted_aircraft'] += 1
                        site['surveys_done_this_year_aircraft'] += 1
                        site['t_since_last_LDAR_aircraft'] = 0
                        break
                                            
                    else:
                        site['attempted_today_aircraft?'] = True

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
                    
        # Simple detection module based optimistically on Fox et al 2019 lower bound (lit review)
        detect = False
        if site_cum_rate > (2000*0.024):  # g/hour to kg/day
            detect = True    
        
        if detect == True:
            # Flag the site for follow up
            site['flagged'] = True
                
        elif detect == False:
            site['missed_leaks_aircraft'] += len(leaks_present)
                
        self.state['t'].current_date += timedelta(minutes = int(site['aircraft_time']))
