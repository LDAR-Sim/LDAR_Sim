# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.leaks
# Purpose:     Generate Leaks, Generate initial leaks and leak timeseries
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

from datetime import datetime, timedelta

from numpy import random
from utils.distributions import leak_rvs


def generate_leak(program, site, start_date, leak_count, days_active=0):
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
        'tagged': False,
        'component': 'unknown',
        'date_began': start_date,
        'date_tagged': None,
        'tagged_by_company': None,
        'tagged_by_crew': None,
        'init_detect_by': None,
        'init_detect_date': None,
        'requires_shutdown': False,
        'date_repaired': None,
        'repair_delay': None,
    }


def generate_leak_timeseries(program, site, leak_count=0):
    """ Generate a time series of leaks for a single site

    Args:
        program (dict): Program parameter dictionary
        site (dict): Site parameter and variable dictionary
        leak_count (integer): Number of leaks at site, used for creating id

    Returns:
        list: Timeseries of leaks at a site. None is a placeholder for days without leaks
    """
    # Get leak timeseries
    start_date = datetime(*program['start_date'])
    n_timesteps = (datetime(*program['end_date'])-start_date).days
    site_timeseries = []
    for t in range(n_timesteps):
        if random.binomial(1, program['emissions']['LPR']):
            cur_dt = start_date + timedelta(days=t)
            site['cum_leaks'] += 1
            site_timeseries.append(generate_leak(program, site, cur_dt, site['cum_leaks']))
        else:
            site_timeseries.append(None)
    return site_timeseries


def generate_initial_leaks(program, site):
    """ Generate initial leaks at a site

    Args:
        program (dict): Program parameter dictionary
        site (dict): Site parameter and variable dictionary

    Returns:
        list: List of leaks at a site
    """
    # Get distribit
    n_leaks = random.binomial(program['NRd'], program['emissions']['LPR'])
    prog_start_date = datetime(*program['start_date'])
    initial_site_leaks = []
    site.update({'initial_leaks': n_leaks, 'cum_leaks': n_leaks})
    leak_count = 0
    for leak in range(n_leaks):
        leak_count += 1
        days_active = random.randint(0, high=program['NRd'])
        leak_start_date = prog_start_date - timedelta(days=days_active)
        initial_site_leaks.append(
            generate_leak(program, site, leak_start_date, leak_count, days_active))
    return initial_site_leaks
