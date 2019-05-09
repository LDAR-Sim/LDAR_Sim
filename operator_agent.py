import numpy as np

class operator_agent:
    def __init__ (self, timeseries, parameters, state):
        '''
        Constructs an operator who visits all sites and occasionally finds
        a leak.
        '''
        print('Initializing operator...')
        self.parameters = parameters
        self.state = state
        self.timeseries = timeseries
        self.init_mean_leaks = np.mean(self.state['init_leaks'])
        self.init_sum_leaks = np.sum(self.state['init_leaks']) 
        self.n_sites = len(self.state['sites'])

        return

#    def work_a_day (self):
#        '''
#        Detect leaks during operator visits
#        '''
#        for leak in self.state['leaks']:
#            if leak['status'] == 'active':
#                prob_detect = 0.00133*7/6.186   # LPR * days of the week / leaks per well in baseline
#                detect = np.random.binomial(1, prob_detect)
#
#                if detect == True:
#                    # Add these leaks to the 'tag pool'
#                    leak['date_found'] = self.state['t'].current_date
#                    leak['found_by_company'] = 'operator'
#                    leak['found_by_crew'] = 1
#                    self.state['tags'].append(leak)
#                    
#                    
#        return

    def work_a_day (self):
        '''
        Detect leaks during operator visits
        '''      
        
        active_leaks = self.timeseries['active_leaks'][self.state['t'].current_timestep]
        leak_term = ( self.init_sum_leaks / active_leaks ) * self.init_mean_leaks
        
        for leak in self.state['leaks']:
            if leak['status'] == 'active':
                prob_detect = self.parameters['LPR'] * 7 / leak_term    # LPR * days of the week / leaks per well in baseline
                detect = np.random.binomial(1, prob_detect)

                if detect == True:
                    # Add these leaks to the 'tag pool'
                    leak['date_found'] = self.state['t'].current_date
                    leak['found_by_company'] = 'operator'
                    leak['found_by_crew'] = 1
                    self.state['tags'].append(leak)
                        
        return
    
#    def work_a_day (self):
#        '''
#        Detect leaks during operator visits
#        '''      
#        
#        active_leaks = self.timeseries['active_leaks'][self.state['t'].current_timestep]
#        leak_term = ( self.init_sum_leaks / active_leaks ) * self.init_mean_leaks
#        
#        for leak in self.state['leaks']:
#            if leak['status'] == 'active':
#                prob_detect = self.parameters['LPR'] * 7 / leak_term    # LPR * days of the week / leaks per well in baseline
#                detect = np.random.binomial(1, prob_detect)
#
#                if detect == True:
#                    # Add these leaks to the 'tag pool'
#                    leak['date_found'] = self.state['t'].current_date
#                    leak['found_by_company'] = 'operator'
#                    leak['found_by_crew'] = 1
#                    self.state['tags'].append(leak)
#                        
#        return