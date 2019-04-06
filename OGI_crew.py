
import numpy as np

class OGI_crew:
    def __init__ (self, state, parameters, config, timeseries, id):
        '''
        Constructs an individual OGI crew based on defined configuration.
        '''
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crewstate = {'id': id}     # Crewstate is unique to this agent
        self.crewstate['truck'] = np.random.choice (self.config['truck_types'])
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        self.n_sites_done_today = 0
        self.time_of_day = 800
        return

    def work_a_day (self):
        '''
        Go to work and find the leaks for a given day
        '''

        self.n_sites_done_today = 0         # Reset well count
        self.time_of_day = 800              # Reset time of day
        while self.time_of_day < 1800:
            facility_ID = self.choose_site ()
            if self.time_of_day < 1800:
                self.visit_site (facility_ID)
        return


    def choose_site (self):
        '''
        Choose a site to survey.

        '''

        # First, identify the site you want based on a neglect ranking
        self.state['sites'] = sorted(self.state['sites'], key=lambda k: k['t_since_last_LDAR'], reverse = True)

        # Then, check all the conditions for that site...
        for site in self.state['sites']:

            # If the site is 'unripened' (i.e. hasn't met the minimum interval set out in the LDAR regulations/policy), break out - no LDAR today
            if site['t_since_last_LDAR'] < self.parameters['minimum_interval']:
                self.time_of_day = 1800
                break

            # Else if site-specific required visits have not been met for the year - I think this is a clever way to do this that works?!
            elif site['surveys_conducted']*(365/self.state['t']) < int(site['required_surveys']):

                # Check the weather for that site
                weather = self.state['weather'].get_weather (
                    lat = float(next(item for item in self.state['sites'] if item['facility_ID'] == site['facility_ID'])['lat']),
                    lon = float(next(item for item in self.state['sites'] if item['facility_ID'] == site['facility_ID'])['lon']),
                    time = self.state['t'])

                # Is the weather suitable?
                if weather['temp'] < self.config['min_temp'] or weather['wspeed'] > self.config['max_wind'] and weather['precip'] > self.config['max_precip']:
                    self.timeseries['wells_skipped_weather'][self.state['t']] += 1
                    continue

                else:
                    # The site passes all the tests! Choose it!
                    facility_ID = site['facility_ID']

                    # Update site
                    site['surveys_conducted'] += 1
                    site['t_since_last_LDAR'] = 0

                    # Need to update 'surveys_this_year' and 't_since_last_LDAR'
                    return (facility_ID)
                    break


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
            leak['date_found'] = self.state['t']
            leak['found_by_company'] = 'OGI_company'
            leak['found_by_crew'] = self.crewstate['id']
            self.state['tags'].append(leak)

        self.time_of_day += 200
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
            self.time_of_day = 1800
        return
