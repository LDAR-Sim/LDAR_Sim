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
import time

#------------------------------------------------------------------------------
#----------------------Static user-defined input parameters--------------------
n_simulations = 2
for i in range(n_simulations):       
    parameters = {
    'simulation': str(i),
    'timesteps': 5000,
    'spin_up': 0,
    'start_year': 2003,
    'an_data': 'an_2003_2018_AB.nc',
    'fc_data': 'fc_2003_2018_AB.nc',
    'infrastructure_file': 'AER_Baytex_template.csv',
    'leak_file': 'rates_Clearstone.csv',
    'count_file': 'counts_Clearstone.csv',
    'vent_file': 'ZA_site_emissions_2018.csv',
    'output_folder': 'solo_operator_2',
    'working_directory': "D:\OneDrive - University of Calgary\Documents\Thomas\PhD\Thesis\LDAR_Sim\model\python_v2",
    'LPR': 0.00133,         # Will be overwritten if sensitivity == True
    'repair_delay': 14,     # Will be overwritten if sensitivity == True
    'max_det_op': 0.00,     # Will be overwritten if sensitivity == True
    'consider_daylight': True,
    'consider_venting': True,
    'write_data': True, # Must be TRUE to make plots and maps
    'make_plots': True,
    'make_maps': False,
    'start_time': time.time(),
    'sensitivity': {'perform': False, 
                    'program': 'aircraft', 
                    'batch': False},
    'methods': {
#                    'drone': {
#                             'name': 'drone',
#                             'n_crews': 2,
#                             'min_temp': -20,
#                             'max_wind': 20,
#                             'max_precip': 0,
#                             'min_interval': 30,
#                             'max_workday': 10,
#                             'cost_per_day': 3000,
#                             'follow_up_thresh': 2,
#                             'reporting_delay': 2
#                             },
#                    'satellite': {
#                             'name': 'satellite',
#                             'n_crews': 2,
#                             'min_temp': -50,
#                             'max_wind': 20,
#                             'max_precip': 0,
#                             'min_interval': 30,
#                             'max_workday': 23,
#                             'cost_per_day': 1000,
#                             'follow_up_thresh': 100,
#                             'reporting_delay': 2
#                             },
#                    'M21': {
#                             'name': 'M21',
#                             'n_crews': 2,
#                             'min_temp': -25,
#                             'max_wind': 20,
#                             'max_precip': 5,
#                             'min_interval': 120,
#                             'max_workday': 10,
#                             'cost_per_day': 400,
#                             'reporting_delay': 2
#                             },
#                    'OGI': {
#                             'name': 'OGI',
#                             'n_crews': 1,
#                             'min_temp': -10,
#                             'max_wind': 20,
#                             'max_precip': 1,
#                             'min_interval': 60,
#                             'max_workday': 10,  
#                             'cost_per_day': 600,
#                             'reporting_delay': 2,
#                             'MDL': [0.47, 0.01]
#                             },
#                    'OGI_FU': {
#                             'name': 'OGI_FU',
#                             'n_crews': 2,
#                             'min_temp': -35,
#                             'max_wind': 20,
#                             'max_precip': 5,
#                             'max_workday': 10,
#                             'cost_per_day': 600,
#                             'reporting_delay': 2  ,
#                             'MDL': [0.47, 0.01]
#                             },
#                    'truck': {
#                             'name': 'truck',
#                             'n_crews': 2,
#                             'min_temp': -30,
#                             'max_wind': 20,
#                             'max_precip': 5,
#                             'min_interval': 30,
#                             'max_workday': 10,
#                             'cost_per_day': 500,
#                             'follow_up_thresh': 0.5,
#                             'reporting_delay': 2
#                             },
#                    'aircraft': {
#                             'name': 'aircraft',
#                             'n_crews': 2,
#                             'min_temp': -30,
#                             'max_wind': 20,
#                             'max_precip': 5,
#                             'min_interval': 30,
#                             'max_workday': 10,
#                             'cost_per_day': 2000,
#                             'follow_up_thresh': 60,
#                             'reporting_delay': 2,
#                             'MDL': 2000 # grams/hour
#                             }
                }
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
        'empirical_counts': [],
        'empirical_leaks': [],
        'empirical_sites': [],
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
    

