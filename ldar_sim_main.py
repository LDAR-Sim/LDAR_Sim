#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

from weather_lookup import *
from ldar_sim import *
from time_counter import *

#-------------------------------------------------------------------------------
#----------------------Static user-defined input parameters---------------------

parameters = {
    'timesteps': 500,
    'start_year': 2011,
    'methods': {'OGI': {
                         'n_crews': 1,
                         'truck_types': ['silverado', 'tacoma', 'dodge'],
                         'min_temp': -30,
                         'max_wind': 20,
                         'max_precip': 2
                         },

##   future possibilities:     'truck'/'UAV'/'satellite'/whatever: {
##                   e.g.      'n_crews': 20,
##                   e.g.      'truck_types': ['silverado', 'tacoma', 'dodge'],
##                   e.g.      'n_wells_per_day': 300,
##                         },
                },

    'WT_data': '5YearWT2011_2016.nc',
    'P_data': '5YearPrecip2011_2016.nc',
    'infrastructure_file': 'AER_sites.csv',
    'leak_file': 'FWAQS_all.csv',
    'delay_to_fix': 3,
    'minimum_interval': 10,
    'output_folder': 'sim_output',
    'working_directory': "D:/OneDrive - University of Calgary/Documents/Thomas/PhD/Thesis/LDAR_Sim/model/python_v2"
}

#-------------------------------------------------------------------------------
#-----------------------Initialize dynamic model state--------------------------

state = {
    't': None,                 
    'methods': [],          # list of methods in action
    'sites': [],            # sites in the simulation
    'tags': [],             # leaks that have been tagged for repair
    'leaks': [],            # list of all current leaks
    'weather': None,        # this gets assigned during initialization
}

#------------------------Initialize timeseries data-----------------------------

timeseries = {
    'datetime': [],
    'active_leaks': [],
    'new_leaks': [],
    'cum_repaired_leaks': [],
    'daily_emissions_kg': [],
    'wells_skipped_weather': [0]*parameters['timesteps']
}

#-----------------------------Run simulations-----------------------------------

if __name__ == '__main__':

    # Initialize objects
    print('Initializing, please wait...')
    
    state['weather'] = weather_lookup (state, parameters)
    state['t'] = time_counter(parameters)
    sim = ldar_sim (state, parameters, timeseries)

    # Loop through timeseries
    while state['t'].current_date <= state['t'].end_date:
        sim.update ()
        state['t'].next_day ()

    # Clean up and write files
    sim.finalize ()


