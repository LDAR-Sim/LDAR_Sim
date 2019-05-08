import numpy as np

class operator_agent:
    def __init__ (self, state):
        '''
        Constructs an operator who visits all sites and occasionally finds
        a leak.
        '''
        self.state = state
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
        mean_leaks = np.median(self.state['init_leaks'])
        
        for leak in self.state['leaks']:
            if leak['status'] == 'active':
                prob_detect = 0.00133*7/mean_leaks    # LPR * days of the week / leaks per well in baseline
                detect = np.random.binomial(1, prob_detect)

                if detect == True:
                    # Add these leaks to the 'tag pool'
                    leak['date_found'] = self.state['t'].current_date
                    leak['found_by_company'] = 'operator'
                    leak['found_by_crew'] = 1
                    self.state['tags'].append(leak)
                    
                    
        return