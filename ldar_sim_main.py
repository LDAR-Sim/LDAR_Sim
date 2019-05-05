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
n_simulations = 2
for i in range(n_simulations):
    parameters = {
        'simulation': str(i),
        'timesteps': 2100,
        'start_year': 2011,
        'methods': {
#                    'M21': {
#                             'n_crews': 1,
#                             'truck_types': ['silverado', 'tacoma', 'dodge'],
#                             'min_temp': -25,
#                             'max_wind': 20,
#                             'max_precip': 5,
#                             'min_interval': 120
#                             },
#                        'OGI': {
#                                 'n_crews': 1,
#                                 'truck_types': ['silverado', 'tacoma', 'dodge'],
#                                 'min_temp': -25,
#                                 'max_wind': 20,
#                                 'max_precip': 5,
#                                 'min_interval': 120
#                                 },
                        'OGI_FU': {
                                 'n_crews': 1,
                                 'truck_types': ['silverado', 'tacoma', 'dodge'],
                                 'min_temp': -25,
                                 'max_wind': 20,
                                 'max_precip': 5
                                 },
                        'aircraft': {
                                 'n_crews': 1,
                                 'min_temp': -30,
                                 'max_wind': 20,
                                 'max_precip': 5,
                                 'min_interval': 30
                                 }
                    },
    
        'repair_delay': 14,
        'WT_data': '5YearWT2011_2016.nc',
        'P_data': '5YearPrecip2011_2016.nc',
        'infrastructure_file': 'AER_sites_500_aircraft.csv',
        'leak_file': 'FWAQS_all.csv',
        'output_folder': 'aircraft_program_test',
        'working_directory': "D:/OneDrive - University of Calgary/Documents/Thomas/PhD/Thesis/LDAR_Sim/model/python_v2"
    }
    
#------------------------------------------------------------------------------
#-----------------------Initialize dynamic model state-------------------------
    
    state = {
        't': None,                 
        'methods': [],          # list of methods in action
        'sites': [],            # sites in the simulation
        'flags': [],            # list of sites flagged for follow-up
        'leaks': [],            # list of all current leaks
        'tags': [],             # leaks that have been tagged for repair
        'weather': None,        # this gets assigned during initialization
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
        state['t'] = time_counter(parameters)
        sim = ldar_sim (state, parameters, timeseries)
        
        print ('Initialization complete!')
    
       
    # Loop through timeseries
    while state['t'].current_date <= state['t'].end_date:
        sim.update ()
        state['t'].next_day ()
    
    # Clean up and write files
    sim.finalize ()
    

