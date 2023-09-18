# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.leaks
# Purpose:     Generate Leaks, Generate initial leaks and leak timeseries
#
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

from datetime import datetime, timedelta

from numpy import random
from utils.distributions import leak_rvs


def generate_leak(program, site, start_date, leak_count, days_active=0, day_ts_began=0):
    """ Generate a single leak at a site

    Args:
        program (dict): Program parameter dictionary
        site (dict): Site parameter and variable dictionary
        start_date (datetime): Leak start date
        leak_count (integer): Number of leaks at site, used for creating id
        days_active (int, optional): Days the leak has been active. Defaults to 0.

    Returns:
        dict: Leak object
    """
    if program['emissions']['leak_file'] \
            and program['emissions']['leak_file_use'] == 'sample':
        leak_rate = random.choice(program['emissions']['empirical_leaks'])
    elif 'leak_rate_source' in site and site['leak_rate_source'] == 'sample':
        leak_rate = random.choice(site['empirical_leak_rates'])
    else:
        leak_rate = leak_rvs(
            site['leak_rate_dist'],
            program['emissions']['max_leak_rate'],
            site['leak_rate_units'])
    return {
        'leak_ID': '{}_{}'.format(site['facility_ID'], str(leak_count).zfill(10)),
        'facility_ID': str(site['facility_ID']),
        'equipment_group': random.randint(1, int(site['equipment_groups'])+1),
        'rate': leak_rate,
        'lat': float(site['lat']),
        'lon': float(site['lon']),
        'status': 'active',
        'days_active': days_active,
        'volume': None,
        'estimated_volume': None,
        'estimated_volume_b': None,
        'measured_rate': None,
        'tagged': False,
        'component': 'unknown',
        'date_began': start_date,
        'day_ts_began': day_ts_began,
        'estimated_date_began': None,
        'date_tagged': None,
        'tagged_by_company': None,
        'tagged_by_crew': None,
        'init_detect_by': None,
        'init_detect_date': None,
        'requires_shutdown': False,
        'date_repaired': None,
        'repair_delay': None,
    }


def generate_leak_timeseries(virtual_world, site, start_date, end_date, leak_count=0):
    """ Generate a time series of leaks for a single site
    Args:
        virtual_world (dict): Virtual world parameter dictionary
        site (dict): Site parameter and variable dictionary
        leak_count (integer): Number of leaks at site, used for creating id
    Returns:
        list: Timeseries of leaks at a site. None is a placeholder for days without leaks
    """
    LPR = None
    if virtual_world['subtype_file'] is not None:
        LPR = site['LPR']
    else:
        LPR = virtual_world['emissions']['LPR']
    # Get leak timeseries
    start_date = datetime(*start_date)
    n_timesteps = (datetime(*end_date)-start_date).days
    site_timeseries = []
    for t in range(n_timesteps):
        if random.binomial(1, LPR):
            cur_dt = start_date + timedelta(days=t)
            site['cum_leaks'] += 1
            site_timeseries.append(generate_leak(
                virtual_world, site, cur_dt, site['cum_leaks'], day_ts_began=t))
        else:
            site_timeseries.append(None)
    return site_timeseries


def generate_initial_leaks(virtual_world, site, start_date):
    """ Generate initial leaks at a site
    Args:
        virtual_world (dict): Virtual world parameters dictionary
        site (dict): Site parameter and variable dictionary
    Returns:
        list: List of leaks at a site
    """
    NRd = None
    LPR = None
    if virtual_world['subtype_file'] is not None:
        NRd = site['NRd']
        LPR = site['LPR']
    else:
        NRd = virtual_world['NRd']
        LPR = virtual_world['emissions']['LPR']

    if virtual_world['n_init_days'] is not None:
        init_max_days_active = virtual_world['n_init_days']
    else:
        init_max_days_active = NRd

    if virtual_world['n_init_leaks_prob'] is not None:
        n_leaks = random.binomial(init_max_days_active, virtual_world['n_init_leaks_prob'])
    else:
        n_leaks = random.binomial(init_max_days_active, LPR)

    prog_start_date = datetime(*start_date)

    initial_site_leaks = []
    site.update({'initial_leaks': n_leaks, 'cum_leaks': n_leaks})
    leak_count = 0
    for leak in range(n_leaks):
        leak_count += 1
        days_active = random.randint(0, high=init_max_days_active)
        leak_start_date = prog_start_date - timedelta(days=days_active)
        initial_site_leaks.append(
            generate_leak(virtual_world, site, leak_start_date, leak_count, days_active))
    return initial_site_leaks
