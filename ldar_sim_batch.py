#------------------------------------------------------------------------------
# Name:         LDAR-Sim Batch simulator / program comparison
#
# Purpose:      Simulate multiple programs.
#               Outputs: (1) A folder for each program with all simulations,
#               (2) A folder with results (equivalence determination).
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
from plotter_batch import *
import numpy as np
import os
import datetime

#------------------------------------------------------------------------------
#--------------------------------Set programs----------------------------------
master_output_folder = 'multi_comparison/'
# wd = 'C:/Users/tarca/Desktop/ldar_sim_working'
wd = 'C:/Users/tarca/Desktop/ldar_sim_working'
ref_program = 'Regulatory OGI'      # Name must match reference program below
n_simulations = 5                   # Run a minimum of 2 simulations
n_timesteps = 4500                # Min. 2000; Up to ~5600 for 16 year nc file
start_year = 2001

# Define programs. Your first program listed should be the reference program.
programs = [
        {
            'output_folder': master_output_folder + 'Drone',
            'simulation': None,
            'timesteps': n_timesteps,
            'start_year': start_year,
            'methods': {
                    'drone': {
                             'name': 'drone',
                             'n_crews': 1,
                             'min_temp': -20,
                             'max_wind': 10,
                             'max_precip': 0,
                             'min_interval': 100,
                             'max_workday': 10,
                             'cost_per_day': 3000,
                             'follow_up_thresh': 0,
                             'reporting_delay': 2
                             },
                    'OGI_FU': {
                             'name': 'OGI_FU',
                             'n_crews': 1,
                             'min_temp': -10,
                             'max_wind': 5,
                             'max_precip': 1,
                             'max_workday': 10,
                             'cost_per_day': 600,
                             'reporting_delay': 2
                             }                        
                        },        
            'repair_delay': 14,
            'WT_data': '15YearWT2001_2016.nc',
            'P_data': '15YearPrecip2001_2016.nc',
            'infrastructure_file': 'AER_Baytex_3_drone.csv',
            'leak_file': 'FWAQS_all.csv',
            'vent_file': 'ZA_site_emissions_2018.csv',
            'working_directory': wd,
            'LPR': 0.00133,
            'leaks_per_site_mean': 6.186,
            'leaks_per_site_std': 6.717,            
            'consider_daylight': True,
            'consider_venting': True,
            'max_det_op': 0.00   # Operator max additional detection probability of largest leak
        },                 
        {
            'output_folder': master_output_folder + 'Regulatory OGI',
            'simulation': None,
            'timesteps': n_timesteps,        
            'start_year': start_year,
            'methods': {
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 1,
                             'min_temp': -10,
                             'max_wind': 5,
                             'max_precip': 1,
                             'min_interval': 100,
                             'max_workday': 10,  
                             'cost_per_day': 600,
                             'reporting_delay': 2
                             }
                        },        
            'repair_delay': 14, 
            'WT_data': '15YearWT2001_2016.nc',
            'P_data': '15YearPrecip2001_2016.nc',
            'infrastructure_file': 'AER_Baytex_OGI_reg.csv',
            'leak_file': 'FWAQS_all.csv',
            'vent_file': 'ZA_site_emissions_2018.csv',
            'working_directory': wd,
            'LPR': 0.00133,
            'leaks_per_site_mean': 6.186,
            'leaks_per_site_std': 6.717,              
            'consider_daylight': True,
            'consider_venting': True,
            'max_det_op': 0.00   # Operator max additional detection probability of largest leak
        },
        {
            'output_folder': master_output_folder + 'Aircraft',
            'simulation': None,
            'timesteps': n_timesteps,
            'start_year': start_year,
            'methods': {
                    'aircraft': {
                             'name': 'aircraft',
                             'n_crews': 1,
                             'min_temp': -20,
                             'max_wind': 5,
                             'max_precip': 0,
                             'min_interval': 100,
                             'max_workday': 10,
                             'cost_per_day': 2000,
                             'follow_up_thresh': 110,
                             'reporting_delay': 2
                             },
                    'OGI_FU': {
                             'name': 'OGI_FU',
                             'n_crews': 1,
                             'min_temp': -10,
                             'max_wind': 5,
                             'max_precip': 1,
                             'max_workday': 10,
                             'cost_per_day': 600,
                             'reporting_delay': 2
                             }                        
                        },        
            'repair_delay': 14,
            'WT_data': '15YearWT2001_2016.nc',
            'P_data': '15YearPrecip2001_2016.nc',
            'infrastructure_file': 'AER_Baytex_3_aircraft.csv',
            'leak_file': 'FWAQS_all.csv',
            'vent_file': 'ZA_site_emissions_2018.csv',
            'working_directory': wd,
            'LPR': 0.00133,
            'leaks_per_site_mean': 6.186,
            'leaks_per_site_std': 6.717,              
            'consider_daylight': True,
            'consider_venting': True,
            'max_det_op': 0.00   # Operator max additional detection probability of largest leak
        },
        {
            'output_folder': master_output_folder + 'Truck',
            'simulation': None,
            'timesteps': n_timesteps,
            'start_year': start_year,
            'methods': {
                    'truck': {
                             'name': 'truck',
                             'n_crews': 1,
                             'min_temp': -35,
                             'max_wind': 25,
                             'max_precip': 10,
                             'min_interval': 100,
                             'max_workday': 10,
                             'cost_per_day': 500,
                             'follow_up_thresh': 0,
                             'reporting_delay': 2
                             },
                    'OGI_FU': {
                             'name': 'OGI_FU',
                             'n_crews': 1,
                             'min_temp': -10,
                             'max_wind': 5,
                             'max_precip': 1,
                             'max_workday': 10,
                             'cost_per_day': 600,
                             'reporting_delay': 2
                             }                        
                        },        
            'repair_delay': 14,
            'WT_data': '15YearWT2001_2016.nc',
            'P_data': '15YearPrecip2001_2016.nc',
            'infrastructure_file': 'AER_Baytex_3_truck.csv',
            'leak_file': 'FWAQS_all.csv',
            'vent_file': 'ZA_site_emissions_2018.csv',
            'working_directory': wd,
            'LPR': 0.00133,
            'leaks_per_site_mean': 6.186,
            'leaks_per_site_std': 6.717,            
            'consider_daylight': True,
            'consider_venting': True,
            'max_det_op': 0.00   # Operator max additional detection probability of largest leak
        },
        ]

output_directory = programs[0]['working_directory'] + '/' + master_output_folder
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
for program in programs:
    parameters = program
    
    for i in range(n_simulations): 
        parameters['simulation'] = str(i)
    
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

batch_plots (output_directory, programs[0]['start_year'], ref_program)
# Write metadata
metadata = open(output_directory + '/metadata.txt','w')
metadata.write(str(programs) + '\n' +
str(datetime.datetime.now()))

metadata.close()
    
    
#---------------------------------Method library-------------------------------
#
#                    'M21': {
#                             'name': 'M21',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 60,
#                             'max_workday': 10,
#                             'cost_per_day': 400,
#                             'reporting_delay': 2
#                             },
#                    'OGI': {
#                             'name': 'OGI',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 60,
#                             'max_workday': 10,  
#                             'cost_per_day': 600,
#                             'reporting_delay': 2
#                             },
#                    'OGI_FU': {
#                             'name': 'OGI_FU',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'max_workday': 10,
#                             'cost_per_day': 600,
#                             'reporting_delay': 2
#                             },
#                    'truck': {
#                             'name': 'truck',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 30,
#                             'max_workday': 10,
#                             'cost_per_day': 500,
#                             'follow_up_thresh': 0,
#                             'reporting_delay': 2
#                             },
#                    'aircraft': {
#                             'name': 'aircraft',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 60,
#                             'max_workday': 10,
#                             'cost_per_day': 2000,
#                             'follow_up_thresh': 0,
#                             'reporting_delay': 2
#                             },
#                    'drone': {
#                             'name': 'truck',
#                             'n_crews': 2,
#                             'min_temp': -20,
#                             'max_wind': 10,
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
#                             'max_wind': 30,
#                             'max_precip': 0,
#                             'min_interval': 30,
#                             'max_workday': 23,
#                             'cost_per_day': 1000,
#                             'follow_up_thresh': 100,
#                             'reporting_delay': 2
#                             },