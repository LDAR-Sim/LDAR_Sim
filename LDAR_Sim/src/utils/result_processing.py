# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        utils.result_processing
# Purpose:     process the output of ldar_sim_run / starmap
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
from pandas import concat, merge


def get_referenced_dataframe(sim_results, columns, ref_prog='P_ref'):
    """ Generate Ratios between values from programs and a reference program
        eg:
        get_ref_ratios(sim_results, ['daily_emissions_kg', 'emis_rat', 'rat'], ref_prog='P_ref')
        will calulate the ratio of daily_emissions_kg between all programs and the reference
        program for all timesteps, and store the values in a dataframe column named emis_rat
    Args:
        sim_results (list): list: Output results from Simulations. Each simulation will include
            timeseries, sites, leaks, and meta (data) dictionaries.
        columns (list of lists): a list of columns to calulate where the first element is the
            column within the timeseries dataframe, the second is the name for the new output column
            and the third is the operation (diff or rat) Where diff takes the difference between
            the reference program and all other programs, and rat take the ratio between the two.
        ref_prog (str, optional): reference program name. Defaults to 'P_ref'.

    Returns:
        Dataframe: Pandas dataframe with columns passed in columns argument, the reference operation
        x and y keys and values, program names and timestep (index).
    """
    ref = []
    alt = []
    in_cols = [col[0] for col in columns]
    for sim in sim_results:
        p_ts = sim['timeseries'][in_cols].copy()
        p_ts['n_sim'] = int(sim['meta']['simulation'])
        p_ts['program_name'] = sim['meta']['program_name']
        p_ts['key_x'] = sim['key_x']
        p_ts['value_x'] = sim['value_x']
        if sim['meta']['program_name'] == ref_prog:
            ref.append(p_ts)
        try:
            p_ts['key_z'] = sim['meta']['key_z']
            p_ts['value_z'] = sim['meta']['value_z']
        except KeyError:
            pass
        alt.append(p_ts)
    all_ref = concat(ref).reset_index().rename({'program_name': 'ref_prog'}, axis=1)
    all_ref = all_ref.rename({col[0]: "ref_{}".format(col[0]) for col in columns}, axis=1)
    all_alt = concat(alt).reset_index()
    alt_updates = merge(all_alt, all_ref, on=["index", "n_sim", "key_x", "value_x"])
    for col in columns:
        if col[2] == 'rat':
            alt_updates[col[1]] = alt_updates[col[0]]/alt_updates["ref_{}".format(col[0])]
        else:
            alt_updates[col[1]] = alt_updates[col[0]] - alt_updates["ref_{}".format(col[0])]
    return alt_updates
