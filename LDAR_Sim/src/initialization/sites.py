# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.sites
# Purpose:     Pregenerate sites and regenerate sites
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

import copy
import fnmatch
import os
import pickle
import random

import numpy as np
import pandas as pd
from initialization.leaks import (generate_initial_leaks,
                                  generate_leak_timeseries)
from utils.distributions import fit_dist, unpackage_dist
from utils.emis_inputs import (assign_vents)
from methods.init_func.repair_delay import determine_delay


def init_generator_files(generator_dir, sim_params, in_dir, virtual_world):
    sites_file = virtual_world['infrastructure_file']
    sites_in = pd.read_csv(in_dir / sites_file)
    sim_sites = sites_in.to_dict('records')
    if not os.path.exists(generator_dir):
        os.mkdir(generator_dir)
    gen_files = fnmatch.filter(os.listdir(generator_dir), '*.p')
    if len(gen_files) > 0:
        try:
            old_sites = pickle.load(open(generator_dir / 'sites.p', "rb"))
            old_params = pickle.load(open(generator_dir / 'params.p', "rb"))
        except FileNotFoundError:
            old_sites = None
            old_params = None
            # Check to see if params used to generate the pickle files have changed
        if old_params != sim_params or old_sites != sim_sites:
            for file in gen_files:
                os.remove(generator_dir / file)
    pickle.dump(sim_sites, open(generator_dir / 'sites.p', "wb"))
    pickle.dump(sim_params, open(generator_dir / 'params.p', "wb"))


def get_subtype_dist(program, wd):
    # Get Sub_type data
    if program['emissions']['subtype_leak_dist_file']:
        subtypes = pd.read_csv(
            wd / program['emissions']['subtype_leak_dist_file'],
            index_col='subtype_code')
        program['subtypes'] = subtypes.to_dict('index')
        for st in program['subtypes']:
            program['subtypes'][st]['leak_rate_units'] = program['emissions']['units']
        unpackage_dist(program, wd)
    elif program['emissions']['leak_file_use'] == 'fit':
        program['subtypes'] = {0: {
            'leak_rate_dist': fit_dist(
                samples=program['empirical_leaks'],
                dist_type='lognorm'),
            'leak_rate_units': ['gram', 'second']}}
    elif not program['emissions']['subtype_leak_dist_file']:
        program['subtypes'] = {0: {
            'dist_type': program['emissions']['leak_dist_type'],
            'dist_scale': program['emissions']['leak_dist_params'][0],
            'dist_shape': program['emissions']['leak_dist_params'][1:],
            'leak_rate_units': program['emissions']['units']}}
        unpackage_dist(program, wd)


def get_subtype_file(program, wd):
    if program['subtype_file']:
        subtypes = pd.read_csv(
            wd / program['subtype_file'],
            index_col='subtype_code')
        program['subtypes'] = subtypes.to_dict('index')
        for st in program['subtypes']:
            program['subtypes'][st]['leak_rate_units'] = program['emissions']['units']
        unpackage_dist(program, wd)
        assign_vents(program, wd)
    elif program['emissions']['leak_file_use'] == 'fit':
        program['subtypes'] = {0: {
            'leak_rate_dist': fit_dist(
                samples=program['empirical_leaks'],
                dist_type='lognorm'),
            'leak_rate_units': ['gram', 'second']}}
    elif not program['subtype_file']:
        program['subtypes'] = {0: {
            'dist_type': program['emissions']['leak_dist_type'],
            'dist_scale': program['emissions']['leak_dist_params'][0],
            'dist_shape': program['emissions']['leak_dist_params'][1:],
            'leak_rate_units': program['emissions']['units']}}
        unpackage_dist(program, wd)


def generate_sites(virtual_world, in_dir, pregen_leaks, start_date, end_date):
    """[summary]

    Args:
        virtual_world (dict): The virtual world parameters informing site generation.
        in_dir (Path): The path to the inputs directory
        pregen_leaks (boolean): Boolean indicating whether or not to pregenerate leaks.

    Returns:
        [dict]: sites, Union[dict, None]: leak_timeseries, Union[dict, None]: initial_leaks
    """
    # Read in the sites as a list of dictionaries
    sites_in = pd.read_csv(in_dir / virtual_world['infrastructure_file'])
    sites = sites_in.to_dict('records')

    # Sample sites and shuffle
    n_samples = virtual_world['site_samples']
    if n_samples is None:
        n_samples = len(sites)
    # even if n_samples is None, the sample function is still used to shuffle
    sites = random.sample(sites, n_samples)

    # Get leaks from file
    if virtual_world['emissions']['leak_file'] is not None:
        virtual_world['emissions']['empirical_leaks'] = np.array(
            pd.read_csv(in_dir / virtual_world['emissions']['leak_file']).iloc[:, 0])

    # get_subtype_dist(program, in_dir)
    get_subtype_file(virtual_world, in_dir)

    leak_timeseries = {}
    initial_leaks = {}
    # Additional variable(s) for each site
    for site in sites:
        # Add a distribution and unit for each leak
        if len(virtual_world['subtypes']) > 1:
            # Get all keys from subtypes
            for col in virtual_world['subtypes'][next(iter(virtual_world['subtypes']))]:
                site[col] = virtual_world['subtypes'][site['subtype_code']][col]
        elif len(virtual_world['subtypes']) > 0:
            site.update(virtual_world['subtypes'][0])

        # Determine repair delay for each site
        site['repair_delay'] = determine_delay(virtual_world)

        if pregen_leaks:
            initial_site_leaks = generate_initial_leaks(virtual_world, site, start_date)
            initial_leaks.update({site['facility_ID']: initial_site_leaks})
            site_timeseries = generate_leak_timeseries(virtual_world, site, start_date, end_date)
            leak_timeseries.update({site['facility_ID']: site_timeseries})
            if 'leak_rate_dist' in site:
                del site['leak_rate_dist']

    if pregen_leaks:
        return sites, leak_timeseries, initial_leaks
    else:
        return sites, None, None


def regenerate_sites(virtual_world, prog_0_sites, in_dir):
    '''
    Regenerate sites allows site level parameters to update on pregenerated
    sites. This is necessary when programs have different site level params
    for example, the survey frequency or survey time could be different.
    '''
    # Read in the sites as a list of dictionaries
    sites_in = pd.read_csv(
        in_dir / virtual_world['infrastructure_file'], index_col='facility_ID')
    # Add facility ID back into object
    sites_in['facility_ID'] = sites_in.index
    sites = sites_in.to_dict('index')
    out_sites = []
    for site_or in prog_0_sites:
        s_idx = site_or['facility_ID']
        new_site = copy.deepcopy(sites[s_idx])
        new_site.update({'cum_leaks': site_or['cum_leaks'],
                         'initial_leaks': site_or['initial_leaks'],
                         'leak_rate_units': site_or['leak_rate_units'],
                         'repair_delay': site_or['repair_delay']})
        if 'empirical_leak_rates' in site_or:
            new_site.update({
                'empirical_leak_rates': site_or['empirical_leak_rates']
            })
        if 'leak_rate_dist' in site_or:
            new_site.update({
                'leak_rate_dist': site_or['leak_rate_dist'],
            })
        if 'empirical_vent_rates' in site_or:
            new_site.update({
                'empirical_vent_rates': site_or['empirical_vent_rates']
            })
        out_sites.append(new_site)
    return out_sites
