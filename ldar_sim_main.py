#------------------------------------------------------------------------------
# Name:         LDAR-Sim User Interface
#
# Purpose:      Simulate an LDAR program for a set of user-defined conditions.
#               Creates a new folder in your working directory and outputs
#               three csv files describing each leak, site, and day.
#
# Authors:      Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:      2019-Mar-26
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
from weather_lookup import *
from ldar_sim import *
from time_counter import *
import numpy as np

#------------------------------------------------------------------------------
#----------------------Static user-defined input parameters--------------------
n_simulations = 1
for i in range(n_simulations):
    parameters = {
        'simulation': str(i),
        'timesteps': 500,
        'start_year': 2011,
        'methods': {
                    'M21': {
                             'name': 'M21',
                             'n_crews': 2,
                             'min_temp': -25,
                             'max_wind': 20,
                             'max_precip': 5,
                             'min_interval': 120,
                             'max_workday': 10,
                             'cost_per_day': 400,
                             'reporting_delay': 2
                             },
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 1,
                             'min_temp': -10,
                             'max_wind': 5,
                             'max_precip': 1,
                             'min_interval': 60,
                             'max_workday': 10,  
                             'cost_per_day': 600,
                             'reporting_delay': 2
                             },
                    'OGI_FU': {
                             'name': 'OGI_FU',
                             'n_crews': 2,
                             'min_temp': -35,
                             'max_wind': 20,
                             'max_precip': 5,
                             'max_workday': 10,
                             'cost_per_day': 600,
                             'reporting_delay': 2                             
                             },
                    'truck': {
                             'name': 'truck',
                             'n_crews': 2,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 5,
                             'min_interval': 30,
                             'max_workday': 10,
                             'cost_per_day': 500,
                             'follow_up_thresh': 0.5,
                             'reporting_delay': 2
                             },
                    'aircraft': {
                             'name': 'aircraft',
                             'n_crews': 2,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 5,
                             'min_interval': 30,
                             'max_workday': 10,
                             'cost_per_day': 2000,
                             'follow_up_thresh': 60,
                             'reporting_delay': 2
                             }
                    },
    
        'repair_delay': 14,
        'WT_data': '5YearWT2011_2016.nc',
        'P_data': '5YearPrecip2011_2016.nc',
        'infrastructure_file': 'AER_Baytex_template.csv',
        'leak_file': 'FWAQS_all.csv',
        'vent_file': 'ZA_site_emissions_2018.csv',          # File containing site-level total emissions in g/sec
        'output_folder': 'test_delays_2',
        'working_directory': "D:/OneDrive - University of Calgary/Documents/Thomas/PhD/Thesis/LDAR_Sim/model/python_v2",
        'LPR': 0.00133,
        'leaks_per_site_mean': 6.186,
        'leaks_per_site_std': 6.717,
        'consider_daylight': True,
        'consider_venting': True,
        'max_det_op': 0.00   # Operator max additional detection probability of largest leak
    }
    
#------------------------------------------------------------------------------
#-----------------------Initialize dynamic model state-------------------------
    
    state = {
        't': None,   
        'operator': None,       # operator gets assigned during initialization
        'methods': [],          # list of methods in action
        'sites': [],            # sites in the simulation
        'flags': [],            # list of sites flagged for follow-up
        'leaks': [],            # list of all current leaks
        'tags': [],             # leaks that have been tagged for repair
        'weather': None,        # this gets assigned during initialization
        'daylight': None,
        'init_leaks': [],       # the initial leaks generated at timestep 1
        'empirical_vents': [],
        'max_rate': None        # the largest leak in the input file
    }
    
#------------------------Initialize timeseries data----------------------------
    
    timeseries = {
        'datetime': [],
        'active_leaks': [],
        'new_leaks': [],
        'n_tags': [],
        'cum_repaired_leaks': [],
        'daily_emissions_kg': []
    }
    
#-----------------------------Run simulations----------------------------------
    
    if __name__ == '__main__':
    
        # Initialize objects
        print('Initializing, please wait...')
        
        state['weather'] = weather_lookup (state, parameters)
        state['t'] = time_counter (parameters)
        sim = ldar_sim (state, parameters, timeseries)
        
        print ('Initialization complete!')
    
       
    # Loop through timeseries
    while state['t'].current_date <= state['t'].end_date:
        sim.update ()
        state['t'].next_day ()
    
    # Clean up and write files
    sim.finalize ()
    

