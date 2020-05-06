# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ------------------------------------------------------------------------------

from weather_lookup import *
from ldar_sim import *
from time_counter import *
from batch_reporting import *
import os
import datetime
import time
import gc

# ------------------------------------------------------------------------------
# -----------------------------Global parameters--------------------------------
wd = "../inputs_template/"
wd = os.path.abspath (wd) + "/"
program_list = ['P_ref', 'P_alt', 'P_alt2']  # Programs to compare; Position one should be the reference program (P_ref)

# -----------------------------Set up programs----------------------------------
programs = []
for p in range(len(program_list)):
    file = wd + 'inputs/' + program_list[p] + '.txt'
    exec(open(file).read())
    programs.append(eval(program_list[p]))

n_simulations = programs[0]['n_simulations']
spin_up = programs[0]['spin_up']
ref_program = program_list[0]
write_data = programs[0]['write_data']
output_directory = wd + 'outputs/'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for i in range(n_simulations):
    for j in range(len(programs)):
        parameters = programs[j]
        parameters['working_directory'] = wd

        gc.collect()
        print('Program ' + str(j + 1) + ' of ' + str(len(programs)) + '; simulation ' + str(i + 1) + ' of ' + str(
            n_simulations))

        parameters['simulation'] = str(i)

        # ------------------------------------------------------------------------------
        # -----------------------Initialize dynamic model state-------------------------

        state = {
            't': None,
            'operator': None,  # operator gets assigned during initialization
            'methods': [],  # list of methods in action
            'sites': [],  # sites in the simulation
            'flags': [],  # list of sites flagged for follow-up
            'leaks': [],  # list of all current leaks
            'tags': [],  # leaks that have been tagged for repair
            'weather': None,  # weather gets assigned during initialization
            'daylight': None,  # daylight hours calculated during initialization
            'init_leaks': [],  # the initial leaks generated at timestep 1
            'empirical_vents': [0],  # vent distribution created during initialization
            'max_rate': None  # the largest leak in the input file
        }

        # ------------------------Initialize timeseries data----------------------------

        timeseries = {
            'datetime': [],
            'active_leaks': [],
            'new_leaks': [],
            'n_tags': [],
            'cum_repaired_leaks': [],
            'daily_emissions_kg': []
        }

        # -----------------------------Run simulations----------------------------------

        if __name__ == '__main__':
            # Initialize objects

            state['weather'] = WeatherLookup(state, parameters)
            state['t'] = TimeCounter(parameters)
            sim = LdarSim(state, parameters, timeseries)

        # Loop through timeseries
        while state['t'].current_date <= state['t'].end_date:
            sim.update()
            state['t'].next_day()

        # Clean up and write files
        sim.finalize()

# Do batch reporting
if write_data:
    # Create a data object...
    reporting_data = BatchReporting(output_directory, programs[0]['start_year'], spin_up, ref_program)
    if n_simulations > 1:
        reporting_data.program_report()
        if len(programs) > 1:
            reporting_data.batch_report()
            reporting_data.batch_plots()

# Write metadata
metadata = open(output_directory + '/metadata.txt', 'w')
metadata.write(str(programs) + '\n' +
               str(datetime.datetime.now()))

metadata.close()

