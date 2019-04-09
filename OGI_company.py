
from OGI_crew import *
from weather_lookup import *

class OGI_company:
    def __init__ (self, state, parameters, config, timeseries):
        '''
        Initialize a company to manage the OGI crews (e.g. a contracting company).

        '''
        print('Initializing OGI company...')
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []                         # Empty list of OGI agents (crews)
        self.deployment_days = self.state['weather'].deployment_days('OGI')
        self.timeseries['prop_sites_avail_OGI'] = []
        
        
        # Initialize the individual OGI crews (the agents)
        for i in range (config['n_crews']):
            self.crews.append (OGI_crew (state, parameters, config, timeseries, self.deployment_days, id = i))

        return


    def find_leaks (self):
        '''
        The OGI company tells all the crews to get to work.
        '''

        for i in self.crews:
            i.work_a_day ()
            
        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                available_sites += 1
        prop_avail = available_sites/len(self.state['sites'])
        self.timeseries['prop_sites_avail_OGI'].append(prop_avail) 
            
        return

