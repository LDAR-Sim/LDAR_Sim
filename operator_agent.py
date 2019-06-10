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
        self.timeseries['operator_redund_tags'] = np.zeros(self.parameters['timesteps'])

        return

#    def work_a_day (self):
#        '''
#        Simple detection of leaks during operator visits. 
#        Detection is not a function of leak-size.
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
    
    def work_a_day (self):
        '''
        Detect leaks during operator visits. 
        Detection can be a function of leak-size.
        '''      
        
        active_leaks = self.timeseries['active_leaks'][self.state['t'].current_timestep]
        leak_term = ( self.init_sum_leaks / active_leaks ) * self.init_mean_leaks
        
        for leak in self.state['leaks']:
            if leak['status'] == 'active':
                prob_detect = self.parameters['LPR'] * 7 / leak_term    # LPR * days of the week / leaks per well in baseline
                prob_detect += self.parameters['max_det_op'] * (leak['rate']/self.state['max_rate'])
                detect = np.random.binomial(1, prob_detect)

                if detect == True:
                    if leak['tagged'] == True:
                        self.timeseries['operator_redund_tags'][self.state['t'].current_timestep] += 1
                        
                    elif leak['tagged'] == False:
                        # Add these leaks to the 'tag pool'
                        leak['tagged'] = True
                        leak['date_found'] = self.state['t'].current_date
                        leak['found_by_company'] = 'operator'
                        leak['found_by_crew'] = 1
                        self.state['tags'].append(leak)
                        
        return
    