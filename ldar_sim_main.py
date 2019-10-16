#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
#
# Copyright (C) 2019  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This file is for peer review. Do not distribute or modify it in any way.
# This program is presented WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#------------------------------------------------------------------------------

from weather_lookup import *
from ldar_sim import *
from time_counter import *
from batch_reporting import *
import numpy as np
import os
import datetime
import time
import gc

#------------------------------------------------------------------------------
#-----------------------------Global parameters--------------------------------
master_output_folder = 'OGI_demonstration/'
ref_program = 'P_ref'               # Name must match reference program below for batch plots
n_simulations = 25                  # Minimum of 2 simulations to get batch plots
n_timesteps = 2557                  # Up to ~5600 for 16 year nc file
spin_up = 0
start_year = 2011
operator_strength = 0
an_data = 'an_2003_2018_AB.nc'
fc_data = 'fc_2003_2018_AB.nc'
sites = '1169_anonym_template.csv'
leaks = 'rates_Clearstone.csv'
counts = 'counts_Clearstone.csv'
vents = 'ZA_site_emissions_2018.csv'
t_offsite = 'time_offsite_ground.csv'
subtype_times = [False, 'subtype_times.csv']     # If True, will overwrite site-specific times using subtype times
wd = '<wd here>'
site_samples = [False, 200]
write_data = True # Must be TRUE to make plots and maps
make_plots = True
make_maps = False

#-----------------------------Define programs----------------------------------
programs = [        # Minimum 2 programs to get batch plots
        {
            'methods': {
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 3,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'min_interval': 120,
                             'max_workday': 10,  
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P_ref',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': False,
            'consider_venting': False,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'operator', 
                            'batch': [True, 1]}
        },
        {
            'methods': {
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 3,
                             'min_temp': 0,
                             'max_wind': 5,
                             'max_precip': 0.001,
                             'min_interval': 120,
                             'max_workday': 10,  
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P_W',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': True,
            'consider_venting': True,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'OGI', 
                            'batch': [True, 2]}
        },
        {
            'methods': {
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 1,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'min_interval': 120,
                             'max_workday': 10,  
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P_L',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': True,
            'consider_venting': True,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'OGI', 
                            'batch': [True, 2]}
        },
        {
            'methods': {
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 1,
                             'min_temp': 0,
                             'max_wind': 5,
                             'max_precip': 0.001,
                             'min_interval': 120,
                             'max_workday': 10,  
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P_W_L',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': True,
            'consider_venting': True,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'OGI', 
                            'batch': [True, 2]}
        }
        ]

output_directory = programs[0]['working_directory'] + '/' + master_output_folder
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    
for i in range(n_simulations):
    for j in range(len(programs)):
        parameters = programs[j]
    
        gc.collect()
        print('Program ' + str(j + 1) + ' of ' + str(len(programs)) + '; simulation ' + str(i + 1) + ' of ' + str(n_simulations))
        
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
            'weather': None,        # weather gets assigned during initialization
            'daylight': None,       # daylight hours calculated during initialization
            'init_leaks': [],       # the initial leaks generated at timestep 1
            'empirical_vents': [0], # vent distribution created during initialization
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
            
            state['weather'] = weather_lookup (state, parameters)
            state['t'] = time_counter (parameters)
            sim = ldar_sim (state, parameters, timeseries)
                    
           
        # Loop through timeseries
        while state['t'].current_date <= state['t'].end_date:
            sim.update ()
            state['t'].next_day ()
        
        # Clean up and write files
        sim.finalize ()

# Do batch reporting
if write_data == True:
    # Create a data object...
    reporting_data = batch_reporting(output_directory, programs[0]['start_year'], spin_up, ref_program)
    if n_simulations > 1:
        reporting_data.program_report()
        if len(programs) > 1:        
           reporting_data.batch_report()
           reporting_data.batch_plots()


# Write metadata
metadata = open(output_directory + '/metadata.txt','w')
metadata.write(str(programs) + '\n' +
str(datetime.datetime.now()))

metadata.close()
    
    
#---------------------------------Method library-------------------------------

#                    'OGI': {
#                             'name': 'OGI',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 60,
#                             'max_workday': 10,  
#                             'cost_per_day': 1500,
#                             'reporting_delay': 2,
#                             'MDL': [0.47, 0.01]
#                             },
#                    'OGI_FU': {
#                             'name': 'OGI_FU',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'max_workday': 10,
#                             'cost_per_day': 1500,
#                             'reporting_delay': 2,
#                             'MDL': [0.47, 0.01]
#                             },
#                    'truck': {
#                             'name': 'truck',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 30,
#                             'max_workday': 10,
#                             'cost_per_day': 1500,
#                             'follow_up_thresh': 0,
#                             'follow_up_ratio': 0.5,
#                             'reporting_delay': 2,
#                             'MDL': 100 # grams/hour  
#                             },
#                    'aircraft': {
#                             'name': 'aircraft',
#                             'n_crews': 1,
#                             'min_temp': -35,
#                             'max_wind': 25,
#                             'max_precip': 10,
#                             'min_interval': 60,
#                             'max_workday': 10,
#                             'cost_per_day': 10000,
#                             'follow_up_thresh': 0,
#                             'follow_up_ratio': 0.5,
#                             't_lost_per_site': 10,                             
#                             'reporting_delay': 2,
#                             'MDL': 2000 # grams/hour                             
#                             },
