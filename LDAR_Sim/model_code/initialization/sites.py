
import numpy as np
import random
import csv
import pandas as pd

from initialization.leaks import (generate_leak_timeseries,
                                  generate_initial_leaks)
from utils.distributions import unpackage_dist


def generate_sites(program, in_dir):
    # Read in the sites as a list of dictionaries
    with open(in_dir / program['infrastructure_file']) as f:
        sites = [{k: v for k, v in row.items()}
                 for row in csv.DictReader(f, skipinitialspace=True)]
    empirical_counts = np.array(pd.read_csv(
        in_dir / program['emissions']['leak_count_file']).iloc[:, 0])
    # Sample sites
    if program['site_samples'][0]:
        sites = random.sample(
            sites,
            program['site_samples'][1])

    if program['subtype_times'][0]:
        subtype_times = pd.read_csv(in_dir / program['subtype_times'][1])
        cols_to_add = subtype_times.columns[1:].tolist()
        for col in cols_to_add:
            for site in sites:
                site[col] = subtype_times.loc[subtype_times['subtype_code'] ==
                                              int(site['subtype_code']), col].iloc[0]
    unpackage_dist(program, in_dir)

    # Shuffle all the entries to randomize order for identical 't_Since_last_LDAR' values
    random.shuffle(sites)
    leak_timeseries = {}
    initial_leaks = {}
    # Additional variable(s) for each site
    for site in sites:
        # Add a distribution and unit for each leak
        if program['emissions']['subtype_leak_dist_file'] is None:
            # If subtypes are not used, set subtype code to 0
            site['subtype_code'] = 0
        site['leak_rate_dist'] = program['emissions']['leak_dists'][int(
            site['subtype_code'])]['dist']
        site['leak_rate_units'] = program['emissions']['leak_dists'][int(
            site['subtype_code'])]['units']

        n_leaks = random.choice(empirical_counts)
        if n_leaks < 0:  # This can happen occasionally during sensitivity analysis
            n_leaks = 0
        site.update({'initial_leaks': n_leaks})
        initial_site_leaks = generate_initial_leaks(program, site)
        site['cum_leaks'] = len(initial_site_leaks)
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
    with open(in_dir / program['infrastructure_file']) as f:
        sites = [{k: v for k, v in row.items()}
                 for row in csv.DictReader(f, skipinitialspace=True)]
    out_sites = []
    for site_or in prog_0_sites:
        new_site = {}
        for site in sites:
            if site_or['facility_ID'] == site['facility_ID']:
                new_site.update(site)
                new_site.update({'cum_leaks': site_or['cum_leaks'],
                                 'initial_leaks': site_or['initial_leaks'],
                                 'leak_rate_dist': site_or['leak_rate_dist'],
                                 'leak_rate_units': site_or['leak_rate_units'],
                                 })
        out_sites.append(new_site)
    return out_sites
