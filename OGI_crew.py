
import numpy as np
from datetime import timedelta
import random

class OGI_crew:
    def __init__ (self, state, parameters, config, timeseries, deployment_days, id):
        '''
        Constructs an individual OGI crew based on defined configuration.
        '''
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}     # Crewstate is unique to this agent
        self.crewstate['truck'] = np.random.choice (self.config['truck_types'])
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        self.n_sites_done_today = 0
        return

    def work_a_day (self):
        '''
        Go to work and find the leaks for a given day
        '''

        self.n_sites_done_today = 0                                                                # Reset well count
        self.state['t'].current_date = self.state['t'].current_date.replace(hour = 8)              # Set start of work day
        while self.state['t'].current_date.hour < 18:
            facility_ID, found_site = self.choose_site ()
            if not found_site:
                break                                   # Break out if no site can be found
            self.visit_site (facility_ID)

        return


    def choose_site (self):
        '''
        Choose a site to survey.

        '''

        # First, shuffle all the entries to randomize order for identical 't_Since_last_LDAR' values
        random.shuffle(self.state['sites'])
            
        # Then, identify the site you want based on a neglect ranking
        self.state['sites'] = sorted(self.state['sites'], key=lambda k: k['t_since_last_LDAR'], reverse = True)

        facility_ID = None                                  # The facility ID gets assigned if a site is found
        found_site = False                                  # The found site flag is updated if a site is found

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in self.state['sites']:

            # If the site is 'unripened' (i.e. hasn't met the minimum interval set out in the LDAR regulations/policy), break out - no LDAR today
            if site['t_since_last_LDAR'] < self.parameters['minimum_interval']:
                self.state['t'].current_date = self.state['t'].current_date.replace(hour = 23)
                break

            # Else if site-specific required visits have not been met for the year
            elif site['surveys_conducted']*(365/self.state['t'].current_timestep) < int(site['required_surveys']):

                # Check the weather for that site
                if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                
                    # The site passes all the tests! Choose it!
                    facility_ID = site['facility_ID']   
                    found_site = True

                    # Update site
                    site['surveys_conducted'] += 1
                    site['t_since_last_LDAR'] = 0
                    break
                                        
                else:
                    self.timeseries['wells_skipped_weather'][self.state['t'].current_timestep] += 1

        return (facility_ID, found_site)

    def visit_site (self, facility_ID):
        '''
        Look for leaks at the chosen site.
        '''

        # Identify all the leaks at a site
        self.leaks_present = []
        for leak in self.state['leaks']:
            if leak['facility_ID'] == facility_ID:
                self.leaks_present.append(leak)

        # Add these leaks to the 'tag pool'
        for leak in self.leaks_present:
            leak['date_found'] = self.state['t'].current_date
            leak['found_by_company'] = 'OGI_company'
            leak['found_by_crew'] = self.crewstate['id']
            self.state['tags'].append(leak)

        self.state['t'].current_date += timedelta(hours = 2)
        self.n_sites_done_today += 1



        self.random_disaster ()         # See if there's a disaster
        return


    def random_disaster (self):
        '''
        random disasters
        '''

        if np.random.random() > 0.99999:
            disaster = np.random.choice (['car crash', 'OGI camera failure', 'tire blowout'])
            print ('OGI crew ' + str (self.crewstate['id']) + ' with a ' + \
                    self.crewstate['truck'] + ' truck had a ' + disaster)

            # no more wells today
            self.state['t'].current_date = self.state['t'].current_date.replace(hour = 23)
        return
