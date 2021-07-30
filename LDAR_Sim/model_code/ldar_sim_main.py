# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------
from pathlib import Path

from batch_reporting import BatchReporting
from ldar_sim_run import ldar_sim_run
import pandas as pd
import os
import shutil
import datetime
import warnings
import multiprocessing as mp
from generic_functions import check_ERA5_file

if __name__ == '__main__':
    # ------------------------------------------------------------------------------
    # -----------------------------Global parameters--------------------------------
    src_dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    src_dir = str(src_dir_path)
    root_dir = str(src_dir_path.parent)
    wd = os.path.abspath(root_dir) + "/inputs_template/"
    output_directory = os.path.abspath(root_dir) + "/outputs/"
    # Programs to compare; Position one should be the reference program (P_ref)
    #program_list = ['P_ref', 'P_dev_OGI', 'P_dev_aircraft', 'P_aircraft']
    program_list = ['P_sat','P_dev_satellite']

# -----------------------------Set up programs----------------------------------
    programs = []

    warnings.filterwarnings('ignore')    # Temporarily mute warnings

    for p in range(len(program_list)):
        file = wd + program_list[p] + '.txt'
        exec(open(file).read())
        programs.append(eval(program_list[p]))

    n_processes = programs[0]['n_processes']
    print_from_simulations = programs[0]['print_from_simulations']
    n_simulations = programs[0]['n_simulations']
    spin_up = programs[0]['spin_up']
    ref_program = program_list[0]
    write_data = programs[0]['write_data']

    # Check whether ERA5 data is already in the working directory and download data if not
    check_ERA5_file(wd, programs[0]['weather_file'])

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)

    # Set up simulation parameter files
    simulations = []
    for i in range(n_simulations):
        for j in range(len(programs)):
            opening_message = "Simulating program {} of {} ; simulation {} of {}".format(
                j + 1, len(programs), i + 1, n_simulations
            )
            simulations.append(
                [{'i': i, 'program': programs[j],
                  'wd': wd,
                  'output_directory':output_directory,
                  'opening_message': opening_message,
                  'print_from_simulation': print_from_simulations}])

    # Perform simulations in parallel
    with mp.Pool(processes=n_processes) as p:
        res = p.starmap(ldar_sim_run, simulations)

    # Do batch reporting
    if write_data:
        # Create a data object...
        reporting_data = BatchReporting(
            output_directory, programs[0]['start_year'],
            spin_up, ref_program)
        if n_simulations > 1:
            reporting_data.program_report()
            if len(programs) > 1:
                reporting_data.batch_report()
                reporting_data.batch_plots()

    # Write metadata
    metadata = open(output_directory + '/_metadata.txt', 'w')
    metadata.write(str(programs) + '\n' +
                   str(datetime.datetime.now()))

    metadata.close()

    # Write sensitivity analysis data on a program by program basis
    sa_df = pd.DataFrame(res)
    if 'program' in sa_df.columns:
        for program in sa_df['program'].unique():
            sa_out = sa_df.loc[sa_df['program'] == program, :]
            sa_outfile_name = os.path.join(wd, 'sensitivity_analysis',
                                           'sensitivity_' + program + '.csv')
            sa_out.to_csv(sa_outfile_name, index=False)
