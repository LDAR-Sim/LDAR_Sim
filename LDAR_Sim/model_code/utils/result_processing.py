# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Result Processing
# Purpose:     Initialize each SeekOps crew under SeekOps company
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, verWsion 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------
from pandas import concat, merge


def get_emis_ratios(sim_results, columns, ref_prog='P_ref'):
    ref = []
    alt = []
    for sim in sim_results:
        p_ts = sim['timeseries'][columns].copy()
        p_ts['n_sim'] = int(sim['meta']['simulation'])
        p_ts['program_name'] = sim['meta']['program_name']
        p_ts['key'] = sim['key']
        p_ts['value'] = sim['value']
        if sim['meta']['program_name'] == ref_prog:
            ref.append(p_ts)
        else:
            alt.append(p_ts)
    all_ref = concat(ref).reset_index().rename(
        {columns[0]: 'ref_emis', 'program_name': 'ref_prog'}, axis=1)
    all_alt = concat(alt).reset_index()
    alt_updates = merge(all_alt, all_ref, on=["index", "n_sim", "key", "value"])
    alt_updates['emis_ratio'] = alt_updates[columns[0]]/alt_updates['ref_emis']
    return alt_updates
