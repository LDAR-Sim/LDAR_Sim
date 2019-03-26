import pandas as pd
import csv
import os
import datetime
from OGI_company import *
from truck_company import *

class ldar_sim:
    def __init__ (self, state, parameters, timeseries):
        '''
        Construct the simulation.
        '''

        self.state = state
        self.parameters = parameters
        self.timeseries = timeseries

        # Initialize method(s) to be used; append to state
        for m in self.parameters['methods']:
            if m == 'OGI':
                self.state['methods'].append (OGI_company (self.state,
                    self.parameters, self.parameters['methods'][m], timeseries))
            elif m == 'truck':
                self.state['methods'].append (truck_company (self.state,
                    self.parameters, self.parameters['methods'][m]))
            else:
                print ('Cannot add this method: ' + m)

        # Read in the sites as a list of dictionaries
        with open(self.parameters['infrastructure_file']) as f:
            self.state['sites'] = [{k: v for k, v in row.items()}
                    for row in csv.DictReader(f, skipinitialspace=True)]

        # Additional variable(s) for each site
        for site in self.state['sites']:
            site.update( {"t_since_last_LDAR": 0})
            site.update( {"surveys_conducted": 0})

        # Initialize baseline leaks for each site
        # First, generate initial leak count for each site
        for site in self.state['sites']:
            n_leaks = round(np.random.normal(6.186, 6.717))                       # Placeholder mean and stdev from FEAST - need to empirically justify this distribution
            if n_leaks <= 0:
                site.update({'n_new_leaks': 0})
            else:
                site.update({'n_new_leaks': n_leaks})

        # Second, load empirical leak-size data, switch from pandas to numpy (for speed), and convert g/s to kg/day
        self.empirical_leaks = pd.read_csv(self.parameters['leak_file'])
        self.empirical_leaks = np.array (self.empirical_leaks.iloc [:, 0])*84.4

        # Third, for each leak, create a dictionary and populate values for relevant keys
        for site in self.state['sites']:
            if site['n_new_leaks'] > 0:
                for leak in range(site['n_new_leaks']):
                    self.state['leaks'].append({
                                                'leak_ID': site['facility_ID'] + '_' + str(len(self.state['leaks']) + 1).zfill(10),
                                                'facility_ID': site['facility_ID'],
                                                'rate': self.empirical_leaks[np.random.randint(0, len(self.empirical_leaks))],
                                                'status': 'active',
                                                'days_active': 0,
                                                'component': 'unknown',
                                                'date_began': self.state['t'],
                                                'date_found': None,
                                                'date_repaired': None,
                                                'repair_delay': None,
                                                'found_by_company': None,
                                                'found_by_crew': None,
                                                'requires_shutdown': False,
                                                })

        print ('Initialization complete!')
        return

    def update (self):
        '''
        this rolls the model forward one timestep
        returns nothing
        '''

        self.update_state()                 # Update state of sites and leaks
        self.add_leaks ()                   # Add leaks to the leak pool
        self.find_leaks ()                  # Find leaks
        self.repair_leaks ()                # Repair leaks
        self.report ()                      # Assemble any reporting about model state
        return

    def update_state (self):
        '''
        update the state of active leaks and sites
        '''

        for leak in self.state['leaks']:
            if leak['status'] == 'active':
                leak['days_active'] += 1

        for site in self.state['sites']:
            site['t_since_last_LDAR'] += 1

    def add_leaks (self):
        '''
        add new leaks to the leak pool
        '''
        # First, determine whether each site gets a new leak or not
        for site in self.state['sites']:
            n_leaks = np.random.binomial(1, 0.00133)
            if n_leaks == 0:
                site.update({'n_new_leaks': 0})
            else:
                site.update({'n_new_leaks': n_leaks})

        # For each leak, create a dictionary and populate values for relevant keys
        for site in self.state['sites']:
            if site['n_new_leaks'] > 0:
                for leak in range(site['n_new_leaks']):
                    self.state['leaks'].append({
                                                'leak_ID': site['facility_ID'] + '_' + str(len(self.state['leaks']) + 1).zfill(10),
                                                'facility_ID': site['facility_ID'],
                                                'rate': self.empirical_leaks[np.random.randint(0, len(self.empirical_leaks))],
                                                'status': 'active',
                                                'days_active': 0,
                                                'component': 'unknown',
                                                'date_began': self.state['t'],
                                                'date_found': None,
                                                'date_repaired': None,
                                                'repair_delay': None,
                                                'found_by_company': None,
                                                'found_by_crew': None,
                                                'requires_shutdown': False,
                                                })

        return

    def find_leaks (self):
        '''
        Loop over all your methods in the simulation and ask them to find some leaks.
        '''

        for m in self.state['methods']:
            m.find_leaks ()

        return

    def repair_leaks (self):
        '''
        Repair tagged leaks.
        '''
        for leak in self.state['tags']:
            if self.state['t'] - leak['date_found']  == self.parameters['delay_to_fix']:
                leak['status'] = 'repaired'
                leak['date_repaired'] = self.state['t']
                leak['repair_delay'] = leak['date_repaired'] - leak['date_found']

        return

    def report (self):
        '''
        Daily reporting of leaks, repairs, and emissions.
        '''

        # Update timeseries
        active_leaks = []
        for leak in self.state['leaks']:
            if leak['status'] == 'active':
                active_leaks.append(leak)

        self.timeseries['day'].append(self.state['t'])
        self.timeseries['active_leaks'].append(len(active_leaks))
        self.timeseries['new_leaks'].append(sum(d['n_new_leaks'] for d in self.state['sites']))
        self.timeseries['cum_repaired_leaks'].append(sum(d['status'] == 'repaired' for d in self.state['leaks']))
        self.timeseries['daily_emissions_kg'].append(sum(d['rate'] for d in active_leaks))
#       self.timeseries['prop_sites_unavail']           This might be a dream. Would have to check conditions for EVERY site.. could take forever (although previous model did it).

        print ('Day ' + str(self.state['t']) + ' complete!')
        return

    def finalize (self):
        '''
        Compile and write output files.
        '''
        output_directory = os.path.join(self.parameters['working_directory'], self.parameters['output_folder'])
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for site in self.state['sites']:
            del site['n_new_leaks']
            del site['t_since_last_LDAR']

        df = pd.DataFrame(self.state['leaks'])
        df2 = pd.DataFrame(self.timeseries)
        df3 = pd.DataFrame(self.state['sites'])
        df.to_csv(output_directory + '/leaks_output.csv', index = False)
        df2.to_csv(output_directory + '/timeseries_output.csv', index = False)
        df3.to_csv(output_directory + '/sites_output.csv', index = False)

        # Write metadata
        metadata = open(output_directory + '/metadata.txt','w')
        metadata.write(str(self.parameters) + '\n' +
        str(datetime.datetime.now()))
        metadata.close()


        print ('Simulation complete. Thank you for using the LDAR Simulator.')
        return


