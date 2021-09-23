# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR_sim_sens
# Purpose:     Sensitivity analysis wrapper
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
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

from ldar_sim_run import ldar_sim_run
import os
import copy
import datetime
import multiprocessing as mp
from scipy.stats import ks_2samp
import shutil
import pandas as pd

from utils.result_processing import get_referenced_dataframe
from generic_functions import check_ERA5_file
from initialization.preseed import gen_seed_timeseries
from initialization.sites import generate_sites, regenerate_sites
from initialization.args import files_from_args
from initialization.input_manager import InputManager
from utils.sensitivity import (yaml_to_dict,
                               generate_sens_prog_set,
                               set_from_keylist,
                               generate_violin,
                               group_timeseries)


def run_programs(programs, n_simulations, output_directory):
    """ Setup and run simulations

    Args:
        programs (list): list of program objects
        n_simulations (int): number of simulations for each program
        output_directory (pathlib object): Output directory

    Returns:
        list: Output results from Simulations. Each simulation will include
            timeseries, sites, leaks, and meta (data) dictionaries.
    """
    simulations = []
    for i in range(n_simulations):
        if pregen_leaks:
            sites, leak_timeseries, initial_leaks = generate_sites(
                programs[0], input_directory)
        else:
            sites = [], leak_timeseries = [], initial_leaks = []
        if preseed_random:
            seed_timeseries = gen_seed_timeseries(simulation_parameters)
        else:
            seed_timeseries = None
        for j in range(len(programs)):
            if pregen_leaks:
                # Because changing the parameters, can change leak sizes, and counts,
                # the leaks are regenerated at the initial generated sites, for each
                # program
                sites = regenerate_sites(programs[j], sites, input_directory)
            opening_message = "Simulating program {} of {} ; simulation {} of {}".format(
                j + 1, len(programs), i + 1, n_simulations
            )
            simulations.append(
                [{'i': i, 'program': copy.deepcopy(programs[j]),
                    'globals':simulation_parameters,
                    'input_directory': input_directory,
                    'output_directory':output_directory,
                    'opening_message': opening_message,
                    'pregenerate_leaks': pregen_leaks,
                    'print_from_simulation': print_from_simulations,
                    'sites': sites,
                    'leak_timeseries': leak_timeseries,
                    'initial_leaks': initial_leaks,
                    'seed_timeseries': seed_timeseries,
                  }])

    # Perform simulations in parallel
    with mp.Pool(processes=n_processes) as p:
        res = p.starmap(ldar_sim_run, simulations)

    # Write metadata to file
    metadata = open(output_directory / 'metadata.txt', 'w')
    metadata.write(str(programs) + '\n' + str(datetime.datetime.now()))
    metadata.close()
    return res


# ------- Run Program --------
if __name__ == '__main__':
    # Initialize programs and variables
    root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
    parameter_filenames = files_from_args(root_dir)
    print('LDAR-Sim using parameters supplied as arguments')
    input_manager = InputManager(root_dir)
    simulation_parameters = input_manager.read_and_validate_parameters(parameter_filenames)

    input_directory = simulation_parameters['input_directory']
    output_directory = simulation_parameters['output_directory']
    programs = simulation_parameters.pop('programs')
    n_processes = simulation_parameters['n_processes']
    print_from_simulations = simulation_parameters['print_from_simulations']
    n_simulations = simulation_parameters['n_simulations']
    ref_program = simulation_parameters['reference_program']
    write_data = simulation_parameters['write_data']
    start_date = simulation_parameters['start_date']
    pregen_leaks = simulation_parameters['pregenerate_leaks']
    preseed_random = simulation_parameters['preseed_random']

    # Check whether ERA5 data is already in the working directory and download data if not
    for p in programs:
        check_ERA5_file(input_directory, p['weather_file'])
    # Initialize Sensitivity Parameters
    sens_parameters = yaml_to_dict(input_directory / 'sens_vars.yaml')
    # Z vars add new sets of programs to each group of programs
    # X vars will run new sets of programs
    sens_z_var = sens_parameters['sens_z_var']
    programs = generate_sens_prog_set(sens_z_var, programs)
    sens_x_vars = sens_parameters['sens_x_vars']
    stat_columns = sens_parameters['stat_columns']

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    #  ----------Run Program Routine-------------
    all_progs = []
    if not sens_x_vars:
        # If prog_var_manip is unused run program with parameters in Program Files
        programs, n_simulations, output_directory,
        sites = [], leak_timeseries = [], initial_leaks = []
        all_progs['base'] = run_programs(
            programs, ref_program, n_simulations, write_data, output_directory)
    else:
        #
        for x_var in sens_x_vars:
            sim_progs = []
            var_paths = [path.split(".") for path in x_var['paths']]
            # Get program names and the their associated index in programs object
            key = var_paths[0][-1]
            # Run the program sets with each value of sens_x_var
            for val in x_var['vals']:
                munip_progs = copy.deepcopy(programs)
                for path in var_paths:
                    for (idx, p) in enumerate(munip_progs):
                        # Update the x_var value for each program __all can also be used to
                        # refer to all programs.
                        if p["orig_program_name"] == path[0] or path[0].lower() == '__all':
                            set_from_keylist(munip_progs[idx], path[1:], val)

                # Generate output folder if it doesnt exist
                prog_outdir = output_directory / '{}/{}/'.format(key, val)
                if not os.path.exists(prog_outdir):
                    os.makedirs(prog_outdir)

                # Run Program
                print('------ running {} : {} --------'.format(path, val))
                prog_results = run_programs(munip_progs, n_simulations, prog_outdir)
                for prog in prog_results:
                    prog.update({'key_x': key, 'value_x': val})
                sim_progs += prog_results

            # This will calculate the emissions ratio and the cost difference and
            # and generate pandas data frams that include those added columns
            alt_ts = get_referenced_dataframe(
                sim_progs,
                [['daily_emissions_kg', 'emis_rat', 'rat'],
                 ['total_daily_cost', 'cost_diff', 'diff']],
                ref_program)

            # Create output folder for the sensitivity variable
            pset_output_dir = output_directory/'sens'/'{}'.format(key)
            if pset_output_dir.exists() and pset_output_dir.is_dir():
                shutil.rmtree(pset_output_dir)
            os.makedirs(pset_output_dir)

            # Split up dataframe into multiple frames, by the sensitivity variable
            # this is required for plotting and estimating the KS p_vals
            group_ts = group_timeseries(alt_ts, 'value_x')
            # Group the time series
            group_prog = alt_ts.groupby(['program_name', 'key_x', 'value_x'])
            for col in stat_columns:
                generate_violin(group_ts, col['column'], col['description'], pset_output_dir)
                # Generate descriptive statistics on each input column and save to file
                pgroup_desc_stats = group_prog[col['column']].describe().reset_index()
                pgroup_desc_stats = pgroup_desc_stats.merge(
                    group_prog[col['column']].quantile(0.95).reset_index().rename(
                        columns={col['column']: "95%"}))
                pgroup_desc_stats.to_csv(
                    pset_output_dir / 'desc_{}.csv'.format(col['column']), index=False)
                # Run a Kolmogorov–Smirnov test between each distribution
                ks_mat = {
                    k_x: {
                        k_y: ks_2samp(
                            group_ts[k_x][col['column']],
                            group_ts[k_y][col['column']]).pvalue
                        for k_y, _ in group_ts.items()}
                    for k_x, _ in group_ts.items()}
                ks_df = pd.DataFrame(ks_mat)
                ks_df.to_csv(pset_output_dir/'ks_pval_mat_{}.csv'.format(col['column']))
