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

import time
import random
import csv
import copy
import pandas as pd
import numpy as np

from initialization.leaks import (generate_leak_timeseries,
                                  generate_initial_leaks)
from utils.distributions import (fit_dist, unpackage_dist)


def get_subtype_dist(program, wd):
    # Get Sub_type data
    if program['emissions']['subtype_leak_dist_file']:
        subtypes = pd.read_csv(
            wd / program['emissions']['subtype_leak_dist_file'],
            index_col='subtype_code')
        program['subtypes'] = subtypes.to_dict('index')
        unpackage_dist(program)
    elif program['emissions']['leak_file_use'] == 'fit':
        program['subtypes'] = {0: {
            'dist': fit_dist(
                samples=program['empirical_leaks'],
                dist_type='lognorm'),
            'units': ['gram', 'second']}}
    elif not program['emissions']['subtype_leak_dist_file']:
        program['subtypes'] = {0: {
            'dist_type': program['emissions']['leak_dist_type'],
            'dist_scale': program['emissions']['leak_dist_params'][0],
            'dist_shape': program['emissions']['leak_dist_params'][1:],
            'leak_rate_units': program['emissions']['units']}}
        unpackage_dist(program)


def generate_sites(program, in_dir):
    """[summary]

    Args:
        program ([type]): [description]
        in_dir ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Read in the sites as a list of dictionaries
    sites_in = pd.read_csv(in_dir / program['infrastructure_file'], index_col='facility_ID')
    # Add facility ID back into object
    sites_in['facility_ID'] = sites_in.index
    sites = sites_in.to_dict('index')

    # Sample sites
    if program['site_samples'][0]:
        keys = random.sample(sites.keys(), program['site_samples'][1])
        sites = {k: sites[k] for k in keys}

    if program['subtype_times'][0]:
        subtypes_times_f = pd.read_csv(
            in_dir / program['subtype_times'][1],
            index_col='subtype_code')
        subtypes_times = subtypes_times_f.to_dict('index')

        for sidx, site in sites.items():
            subtypes_times = subtypes_times[site['subtype_code']]
            site.update(subtypes_times)

    if program['emissions']['leak_file'] != "":
        program['empirical_leaks'] = np.array(
            pd.read_csv(in_dir / program['leak_file']).iloc[:, 0])

    get_subtype_dist(program, in_dir)

    # Shuffle all the entries to randomize order for identical 't_Since_last_LDAR' values
    site_l = list(sites.items())

    random.shuffle(site_l)
    sites = dict(site_l)

    leak_timeseries = {}
    initial_leaks = {}
    # Additional variable(s) for each site
    for sidx, site in sites.items():
        site.update({'facility_ID': sidx})
        # Add a distribution and unit for each leak
        if len(program['subtypes']) > 1:
            # Get all keys from subtypes
            for col in program['subtypes'][next(iter(program['subtypes']))]:
                site[col] = program['subtypes'][int(site['subtype_code'])][col]
        elif len(program['subtypes']) > 0:
            site.update(program['subtypes'][0])

        initial_site_leaks = generate_initial_leaks(program, site)
        initial_leaks.update({site['facility_ID']: initial_site_leaks})
        site_timeseries = generate_leak_timeseries(program, site)
        leak_timeseries.update({site['facility_ID']: site_timeseries})
    return sites, leak_timeseries, initial_leaks


def regenerate_sites(program, prog_0_sites, in_dir):
    '''
    Regenerate sites allows site level parameters to update on pregenerated
    sites. This is necessary when programs have different site level params
    for example, the survey frequency or survey time could be different.
    '''
    # Read in the sites as a list of dictionaries
    sites_in = pd.read_csv(in_dir / program['infrastructure_file'], index_col='facility_ID')
    # Add facility ID back into object
    sites_in['facility_ID'] = sites_in.index
    sites = sites_in.to_dict('index')
    out_sites = {}
    for s_idx, site_or in prog_0_sites.items():
        new_site = copy.deepcopy(sites[s_idx])
        new_site.update({'cum_leaks': site_or['cum_leaks'],
                         'initial_leaks': site_or['initial_leaks'],
                         'leak_rate_dist': site_or['leak_rate_dist'],
                         'leak_rate_units': site_or['leak_rate_units']})
        out_sites.update({s_idx: new_site})
    return out_sites
