from datetime import datetime, timedelta
from utils.distributions import leak_rvs
from numpy import random


def generate_leak(program, site, current_date, leak_count):
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
        'facility_ID': site['facility_ID'],
        'equipment_group': random.randint(1, int(site['equipment_groups'])+1),
        'rate': leak_rate,
        'lat': float(site['lat']),
        'lon': float(site['lon']),
        'status': 'active',
        'days_active': 0,
        'tagged': False,
        'component': 'unknown',
        'date_began': current_date,
        'date_tagged': None,
        'tagged_by_company': None,
        'tagged_by_crew': None,
        'requires_shutdown': False,
        'date_repaired': None,
        'repair_delay': None,
    }


def generate_leak_timeseries(program, site, leak_count=0):
    # Get distribit
    start_date = datetime(*program['start_date'])
    n_timesteps = (datetime(*program['end_date'])-start_date).days
    site_timeseries = []
    for t in range(n_timesteps):
        if random.binomial(1, program['LPR']):
            cur_dt = start_date + timedelta(days=t)
            site['cum_leaks'] += 1
            site_timeseries.append(generate_leak(program, site, cur_dt, site['cum_leaks']))
        else:
            site_timeseries.append(None)
    return site_timeseries


def generate_initial_leaks(program, site):
    # Get distribit
    start_date = datetime(*program['start_date'])
    leak_count = 0
    initial_site_leaks = []
    for leak in range(site['initial_leaks']):
        leak_count += 1
        initial_site_leaks.append(generate_leak(program, site, start_date, leak_count))
    return initial_site_leaks
