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
from initialization.emissions import FugitiveEmission


def generate_leak(
        virtual_world,
        site,
        start_date,
        sim_start_date,
        leak_count,
        nrd
) -> FugitiveEmission:
    """ Generate a single leak at a site

    Args:
        program (dict): Program parameter dictionary
        site (dict): Site parameter and variable dictionary
        start_date (datetime): Leak start date
        leak_count (integer): Number of leaks at site, used for creating id
        days_active (int, optional): Days the leak has been active. Defaults to 0.

    Returns:
        Emissions: Emissions object
    """
    if virtual_world['emissions']['leak_file'] \
            and virtual_world['emissions']['leak_file_use'] == 'sample':
        leak_rate = random.choice(virtual_world['emissions']['empirical_leaks'])
    elif 'leak_rate_source' in site and site['leak_rate_source'] == 'sample':
        leak_rate = random.choice(site['empirical_leak_rates'])
    else:
        leak_rate = leak_rvs(
            site['leak_rate_dist'],
            virtual_world['emissions']['max_leak_rate'],
            site['leak_rate_units'])
    return FugitiveEmission(
        emission_n=leak_count,
        site_id=str(site['facility_ID']),
        rate=leak_rate,
        start_date=start_date,
        simulation_sd=sim_start_date,
        repairable=True,
        equipment_group=random.randint(1, int(site["equipment_groups"]) + 1),
        repair_delay=site['repair_delay'],
        repair_cost=200,
        nrd=nrd
    )


def generate_leak_timeseries(
    virtual_world,
    site,
    start_date,
    end_date,
    leak_count=0
) -> list[FugitiveEmission]:
    """ Generate a time series of leaks for a single site
    Args:
        virtual_world (dict): Virtual world parameter dictionary
        site (dict): Site parameter and variable dictionary
        leak_count (integer): Number of leaks at site, used for creating id
    Returns:
        list: Timeseries of leaks at a site. None is a placeholder for days without leaks
    """
    LPR = None
    nrd = None
    if virtual_world['subtype_file'] is not None:
        LPR = site['LPR']
        nrd = site['NRd']
    else:
        LPR = virtual_world['emissions']['LPR']
        nrd = virtual_world['NRd']
    # Get leak timeseries
    start_date = datetime(*start_date)
    n_timesteps = (datetime(*end_date)-start_date).days
    site_timeseries = []
    for t in range(n_timesteps):
        if random.binomial(1, LPR):
            cur_dt = start_date + timedelta(days=t)
            site['cum_leaks'] += 1
            site_timeseries.append(
                generate_leak(
                    virtual_world,
                    site,
                    cur_dt,
                    start_date,
                    site['cum_leaks'],
                    nrd
                )
            )
        else:
            site_timeseries.append(None)
    return site_timeseries


def generate_initial_leaks(
    virtual_world,
    site,
    start_date,
) -> list[FugitiveEmission]:
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
    for leak in range(n_leaks):
        days_active = random.randint(0, high=init_max_days_active)
        leak_start_date = prog_start_date - timedelta(days=days_active)
        initial_site_leaks.append(
            generate_leak(
                virtual_world,
                site,
                leak_start_date,
                prog_start_date,
                leak,
                NRd
            )
        )
    return initial_site_leaks
