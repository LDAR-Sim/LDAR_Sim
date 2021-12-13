# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        out_processing.prog_table
# Purpose:     Generate output program table for web app
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

from pandas import merge
from numpy import median, inf, nan
from out_processing.clean_results import clean_sim_df, agg_flatten


def generate(sim_results, baseline_program):
    """ Generate output table for web app. This includes the following columnns:
        'program_name', 'sim', 'emis_kg_day_site_med', 'act_leaks_day_site_med',
        'mit_vol_tco2e', 'mit_vol_perc', 'cost', 'cost_mit_vol_tco2e',
        'nat_leak_repair_count', 'emis_nat_perc'
    Args:
        sim_results (dict): simulation outputs
        baseline_program (string): Name of the Baseline program

    Returns:
        [dict]: Program summary statistics including:
            'program_name', 'sim', 'emis_kg_day_site_med', 'act_leaks_day_site_med',
            'mit_vol_tco2e', 'mit_vol_perc', 'cost', 'cost_mit_vol_tco2e',
            'nat_leak_repair_count', 'emis_nat_perc'
    """
    ps_idx = ['program_name', 'sim']
    prog_sites = clean_sim_df(sim_results, 'sites', index='facility_ID', params=[
        {'in': 'facility_ID', 'out': 'facility_ID', 'type': str},
        {'in': 'lat', 'out': 'lat', 'type': float},
        {'in': 'lon', 'out': 'lon', 'type': float},
        {'in': 'total_emissions_kg', 'out': 'total_emissions_kg', 'type': float},
        {'in': 'subtype_code', 'out': 'subtype_code', 'type': int},
    ], aggregate=False)

    # Requires to steps, count each by sim then take the average of the sim
    sim_sites_count = agg_flatten(prog_sites, ps_idx, ['facility_ID'], ['count'],
                                  prefix="site", include_col_name=False, include_agg_name=True)

    prog_ts = clean_sim_df(sim_results, 'timeseries', index='ts', params=[
        {'in': 'daily_emissions_kg', 'out': 'emis_kg_day', 'type': float},
        {'in': 'active_leaks', 'out': 'active_leaks_day', 'type': float},
        {'in': 'total_daily_cost', 'out': 'cost_day', 'type': float},
    ], aggregate=False)

    sim_stats_daily = agg_flatten(prog_ts, ps_idx, ['emis_kg_day', 'active_leaks_day', 'cost_day'],
                                  ['sum', median], include_col_name=True, include_agg_name=True)

    # sim_days_count = agg_flatten(prog_ts, ps_idx, ['ts'], ['count'], prefix='days',
    #                              include_col_name=False, include_agg_name=True)

    params = [
        {'in': 'leak_ID', 'out': 'leak_ID', 'type': str},
        {'in': 'facility_ID', 'out': 'facility_ID', 'type': str},
        {'in': 'days_active', 'out': 'days_active', 'type': int},
        {'in': 'date_began', 'out': 'date_began'},
        {'in': 'date_repaired', 'out': 'date_repaired'},
        {'in': 'init_detect_by', 'out': 'init_detect_by'},
        {'in': 'rate', 'out': 'rate_kg_day', 'type': float, 'xfac': 86.4},
    ]
    leaks = clean_sim_df(sim_results, 'leaks', index='leak_ID',
                         params=params, aggregate=False)

    # sim_leaks_count = agg_flatten(leaks, ps_idx, ['leak_ID'], ['count'], prefix="leak",
    #                               include_col_name=False, include_agg_name=True)

    leaks['volume_kg'] = leaks['rate_kg_day'] * leaks['days_active']
    natural_leaks = leaks[leaks['program_name'] == baseline_program][
        ["leak_ID", "sim", 'volume_kg']] \
        .rename(columns={'volume_kg': 'nat_volume_kg'})
    leaks = merge(leaks, natural_leaks, how='left', on=["leak_ID", "sim"])
    leaks['mit_vol_kg'] = leaks['nat_volume_kg'] - leaks['volume_kg']
    # Get responsible companies and attribute leak mitigation to them.
    leaks['init_detect_by'] = leaks['init_detect_by'].replace([None], 'active')

    sim_leaks_by_NRD = agg_flatten(leaks[leaks['init_detect_by'] == 'natural'],
                                   ps_idx,
                                   ['volume_kg'],
                                   ['sum', 'count'],
                                   prefix="nat_vol",
                                   include_col_name=False, include_agg_name=True)

    sim_emis_mit = agg_flatten(leaks, ps_idx,
                               ['mit_vol_kg', 'volume_kg'],
                               agg_types=['sum'],
                               include_col_name=True, include_agg_name=True)

    sim_progs = merge(sim_stats_daily, sim_leaks_by_NRD, how='left', on=["program_name", 'sim'])
    sim_progs = merge(sim_progs, sim_emis_mit, how='left', on=["program_name", 'sim'])
    sim_progs = merge(sim_progs, sim_sites_count, how='left', on=["program_name", 'sim'])

    sim_progs['emis_kg_day_site_med'] = sim_progs['emis_kg_day_median'] / sim_progs['site_count']
    sim_progs['act_leaks_day_site_med'] = sim_progs['active_leaks_day_median'] \
        / sim_progs['site_count']
    sim_progs['mit_vol_tco2e'] = sim_progs['mit_vol_kg_sum'] / 1000*28
    sim_progs['mit_vol_perc'] = sim_progs['mit_vol_kg_sum'] / sim_progs['volume_kg_sum']
    sim_progs['cost_mit_vol_tco2e'] = sim_progs['cost_day_sum'] / sim_progs['mit_vol_tco2e']
    sim_progs['emis_nat_perc'] = sim_progs['nat_vol_sum'] / sim_progs['volume_kg_sum']
    sim_progs.replace([inf, -inf], nan, inplace=True)

    sim_progs = sim_progs.rename(columns={
        'cost_day_sum': 'cost', 'nat_vol_count': 'nat_leak_repair_count'})
    out_table = sim_progs[[
        'program_name', 'sim', 'emis_kg_day_site_med', 'act_leaks_day_site_med',
        'mit_vol_tco2e', 'mit_vol_perc', 'cost', 'cost_mit_vol_tco2e',
        'nat_leak_repair_count', 'emis_nat_perc'
    ]]
    out_table = agg_flatten(out_table, ['program_name'], agg_types=['mean'],
                            include_col_name=True, include_agg_name=False)
    out_table = out_table.drop(columns=['sim'])

    out_table = out_table.set_index('program_name').to_dict('records')
    for p in out_table:
        p.update({'methods': []})
    return out_table
