
from OGI_crew import *

class OGI_company:
    def __init__ (self, state, parameters, config, timeseries):
        '''
        Initialize a company to manage the OGI crews (e.g. a contracting company).

        '''
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []                 # Empty list of OGI agents (crews)

        # Initialize the individual OGI crews (the agents)
        for i in range (config['n_crews']):
            self.crews.append (OGI_crew (state, parameters, config, timeseries, id = i))

        return


    def find_leaks (self):
        '''
        The OGI company tells all the crews to get to work.
        '''

        for i in self.crews:
            i.work_a_day ()

        return

