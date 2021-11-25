# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim
# Purpose:     Primary module of LDAR-Sim
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


import datetime
import random
import sys
import warnings

import numpy as np
import pandas as pd
from math import floor
from daylight_calculator import DaylightCalculatorAve
from geography.vector import grid_contains_point
from initialization.campaigns import init_campaigns
from initialization.leaks import generate_initial_leaks, generate_leak
from initialization.sites import generate_sites
from initialization.update_methods import (est_n_crews, est_site_p_day,
                                           est_t_bw_sites)
from methods.company import BaseCompany
from numpy.random import binomial, choice
from plotter import make_plots
from utils.attribution import update_tag
from utils.distributions import leak_rvs
# from utils.generic_functions import make_maps, flatten_dict

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class LdarSim:
    def __init__(self, global_params, state, params, timeseries):
        """
        Construct the simulation.
        """

        self.state = state
        self.global_params = global_params
        self.parameters = params
        self.timeseries = timeseries
        self.active_leaks = []

        #  --- state variables ---
        state['candidate_flags'] = {}
        # Read in data files
        if params['emissions']['leak_file'] is not None:
            state['empirical_leaks'] = np.array(pd.read_csv(
                params['input_directory'] / params['emissions']['leak_file']))
        if params['emissions']['vent_file'] is not None:
            state['empirical_sites'] = np.array(pd.read_csv(
                params['input_directory'] / params['emissions']['vent_file']))
        if params['economics']['repair_costs']['file'] is not None:
            params['economics']['repair_costs']['vals'] = np.array(pd.read_csv(
                params['input_directory'] / params['economics']['repair_costs']['file']))
            # Read in the sites as a list of dictionaries
        if len(state['sites']) < 1:
            state['sites'], _, _ = generate_sites(params, params['input_directory'])
        state['max_leak_rate'] = params['emissions']['max_leak_rate']
        state['t'].set_UTC_offset(state['sites'])

        # Sample sites if they havent been provided from pregeneration step
        if not params['pregenerate_leaks']:
            if params['site_samples'] is not None:
                state['sites'] = random.sample(
                    state['sites'],
                    params['site_samples'])
            if params['subtype_times_file'] is not None:
                subtype_times_file = pd.read_csv(
                    params['input_directory'] / params['subtype_times_file'])
                cols_to_add = subtype_times_file.columns[1:].tolist()
                for col in cols_to_add:
                    for site in state['sites']:
                        site[col] = subtype_times_file.loc[subtype_times_file['subtype_code'] ==
                                                           int(site['subtype_code']), col].iloc[0]
            # Shuffle all the entries to randomize order for identical 't_Since_last_LDAR' values
            random.shuffle(state['sites'])

        n_subtype_rs = {}
        sites_per_subtype = {}
        # Additional variable(s) for each site
        for site in state['sites']:
            if site['subtype_code'] not in n_subtype_rs:
                n_subtype_rs.update({site['subtype_code']: {'natural': -1}})
                sites_per_subtype.update({site['subtype_code']: 0})
                add_subtype = True
            else:
                add_subtype = False
            sites_per_subtype[site['subtype_code']] += 1
            n_rs = n_subtype_rs[site['subtype_code']]
            for m_label, m_obj in params['methods'].items():
                # Site parameter overwrite of RS and Time (used for sensitivity analysis)
                m_RS = '{}_RS'.format(m_label)
                if m_RS in m_obj:
                    site[m_RS] = m_obj[m_RS]
                m_time = '{}_time'.format(m_label)
                if m_time in m_obj:
                    site[m_time] = m_obj[m_time]
                if add_subtype:
                    if m_RS in site:
                        # if scheduled capture the RS value
                        n_subtype_rs[site['subtype_code']].update({m_label: site[m_RS]})
                    else:
                        # If set rs value to -1 (used for tracking later)
                        n_subtype_rs[site['subtype_code']].update({m_label: -1})
                        # If the value changes set to None
                elif m_RS in site and (n_rs[m_label] != site[m_RS] or n_rs[m_label] is None):
                    n_subtype_rs[site['subtype_code']].update({m_label: None})
                # Get min interval based on RS. a 95% ajustment is used to add a grace period
                # prior to the next campaign period were surveys can start earlier
                # Calculate the site minimum interval
                if m_RS in site and site[m_RS] != 0:
                    site['{}_min_int'.format(m_label)] = floor(365/site[m_RS])  # *0.95
                # Automatically assign 1 crew to followup if left unspecified
                elif m_obj['n_crews'] is None:
                    m_obj['n_crews'] = 1
            if params['pregenerate_leaks']:
                initial_leaks = params['initial_leaks'][site['facility_ID']]
                n_leaks = len(params['initial_leaks'][site['facility_ID']])
            else:
                initial_leaks = generate_initial_leaks(params, site)
                n_leaks = len(initial_leaks)
            site.update({
                'total_emissions_kg': 0,
                'active_leaks': initial_leaks,
                'repaired_leaks': [],
                'tags': [],
                'initial_leak_cnt': n_leaks,
                'currently_flagged': False,
                'flagged_by': None,
                'date_flagged': None,
                'crew_ID': None,
                'lat_index': min(
                    range(len(state['weather'].latitude)),
                    key=lambda i: abs(state['weather'].latitude[i] - float(site['lat']))),
                'lon_index': min(
                    range(len(state['weather'].longitude)),
                    key=lambda i: abs(state['weather'].longitude[i] - float(site['lon']) % 360))
            })
            in_grid, exit_msg = grid_contains_point(
                [site['lat'], site['lon']],
                [state['weather'].latitude, state['weather'].longitude])
            if not in_grid:
                sys.exit(exit_msg)

        self.state['campaigns'] = init_campaigns(n_subtype_rs, sites_per_subtype,
                                                 self.state['t'].timesteps)

        #  --- timeseries variables ---
        timeseries['total_daily_cost'] = np.zeros(params['timesteps'])
        timeseries['repair_cost'] = np.zeros(params['timesteps'])
        timeseries['verification_cost'] = np.zeros(params['timesteps'])
        timeseries['natural_redund_tags'] = np.zeros(self.parameters['timesteps'])
        timeseries['natural_tags'] = np.zeros(self.parameters['timesteps'])
        timeseries['new_leaks'] = np.zeros(self.parameters['timesteps'])
        timeseries['cum_repaired_leaks'] = np.zeros(self.parameters['timesteps'])
        timeseries['daily_emissions_kg'] = np.zeros(self.parameters['timesteps'])
        timeseries['n_tags'] = np.zeros(self.parameters['timesteps'])
        timeseries['rolling_cost_estimate'] = np.zeros(self.parameters['timesteps'])

        # Initialize method(s) to be used; append to state
        calculate_daylight = False
        for m_label, m_obj in params['methods'].items():
            # Update method parameters
            m_obj_wr = params['methods'][m_label]
            if m_obj['scheduling']['route_planning']:
                m_obj_wr['t_bw_sites']['vals'] = est_t_bw_sites(m_obj, state['sites'])
            if m_obj['n_crews'] is None:
                m_obj_wr['n_crews'] = est_n_crews(m_obj, state['sites'])
            m_obj_wr['est_site_p_day'] = est_site_p_day(m_obj, state['sites'])
            if m_obj['t_bw_sites']['file'] is not None:
                m_obj_wr['t_bw_sites']['vals'] = np.array(pd.read_csv(
                    params['input_directory'] / m_obj['t_bw_sites']['file']).iloc[:, 0])
            if m_obj['consider_daylight']:
                calculate_daylight = True
            try:
                state['methods'].append(
                    BaseCompany(state, params, m_obj, timeseries, m_label))
            except AttributeError:
                print('Cannot add this method: ' + m_label)

        # Initialize daylight
        if calculate_daylight:
            state['daylight'] = DaylightCalculatorAve(state, params)

        # If working without methods (operator only), need to get the first day going
        if not bool(params['methods']):
            state['t'].current_date = state['t'].current_date.replace(hour=1)

        # Initialize empirical distribution of vented emissions
        if params['emissions']['consider_venting']:
            state['empirical_vents'] = []

            # Run Monte Carlo simulations to get distribution of vented emissions
            for i in range(1000):
                n_mc_leaks = random.choice(range(20))
                mc_leaks = []
                for leak in range(n_mc_leaks):
                    if params['emissions']['leak_file'] is not None:
                        leaksize = random.choice(state['empirical_leaks'])
                    else:
                        leaksize = leak_rvs(
                            site['leak_rate_dist'],
                            params['emissions']['max_leak_rate'],
                            site['leak_rate_units'])
                    mc_leaks.append(leaksize)

                mc_leak_total = sum(mc_leaks)
                mc_site_total = random.choice(state['empirical_sites'])
                mc_vent_total = mc_site_total - mc_leak_total
                state['empirical_vents'].append(mc_vent_total)

            # Change negatives to zero
            state['empirical_vents'] = [0 if i < 0 else i for i in state['empirical_vents']]
        return

    def update(self):
        """
        this rolls the model forward one timestep
        returns nothing
        """

        self.update_state()  # Update state of sites and leaks
        self.add_leaks()  # Add leaks to the leak pool
        self.deploy_crews()  # Find leaks
        self.repair_leaks()  # Repair leaks
        self.report()  # Assemble any reporting about model state
        return

    def update_state(self):
        """
        update the state of active leaks
        """
        self.active_leaks = []
        for site in self.state['sites']:
            for leak in site['active_leaks']:
                leak['days_active'] += 1
                self.active_leaks.append(leak)

                # Tag by natural if leak is due for NR
                if leak['days_active'] == self.parameters['NRd']:
                    update_tag(leak, site, self.timeseries, self.state['t'],
                               self.state['campaigns'], 'natural')

        self.timeseries['active_leaks'].append(len(self.active_leaks))
        self.timeseries['datetime'].append(self.state['t'].current_date)
        #
        for s_t in self.state['campaigns']:
            for m in self.state['campaigns'][s_t]:
                m_camp = self.state['campaigns'][s_t][m]
                if m_camp['current_campaign'] < m_camp['n_campaigns'] \
                        and m_camp['ts_start'][m_camp['current_campaign']] \
                        == self.state['t'].current_timestep:
                    m_camp['current_campaign'] += 1

    def add_leaks(self):
        """
        add new leaks to the leak pool
        """
        # First, determine whether each site gets a new leak or not
        params = self.parameters
        for site in self.state['sites']:
            new_leak = None
            sidx = site['facility_ID']
            if params['pregenerate_leaks']:
                new_leak = params['leak_timeseries'][sidx][self.state['t'].current_timestep]
            elif binomial(1, self.parameters['emissions']['LPR']):
                new_leak = generate_leak(
                    params, site, self.state['t'].current_date, site['cum_leaks'])
            if new_leak is not None:
                site.update({'n_new_leaks': 1})
                site['cum_leaks'] += 1
                site['active_leaks'].append(new_leak)
            else:
                site.update({'n_new_leaks': 0})
        return

    def deploy_crews(self):
        """
        Loop over all your methods in the simulation and ask them to find some leaks.
        """

        for m in self.state['methods']:
            m.deploy_crews()

        return

    def repair_leaks(self):
        """
        Repair tagged leaks and remove from tag pool.
        """
        cur_date = self.state['t'].current_date
        params = self.parameters
        timeseries = self.timeseries
        state = self.state
        for site in state['sites']:
            has_repairs = False
            for lidx, lk in enumerate(site['active_leaks']):
                repair = False
                if lk['tagged']:
                    # if company is natural then repair immediately
                    if lk['tagged_by_company'] == 'natural':
                        repair = True
                    elif (cur_date - lk['date_tagged']).days \
                            >= (params['repair_delay']
                                + params['methods'][lk['tagged_by_company']]['reporting_delay']):
                        repair = True

                # Repair Leaks
                if repair:
                    has_repairs = True
                    lk['status'] = 'repaired'
                    lk['date_repaired'] = state['t'].current_date
                    lk['repair_delay'] = (lk['date_repaired'] - lk['date_tagged']).days
                    repair_cost = int(choice(params['economics']['repair_costs']['vals']))
                    timeseries['repair_cost'][state['t'].current_timestep] += repair_cost
                    timeseries['verification_cost'][
                        state['t'].current_timestep] += params['economics']['verification_cost']
                    timeseries['total_daily_cost'][state['t'].current_timestep] \
                        += repair_cost + params['economics']['verification_cost']
            # Update site leaks
            if has_repairs:
                site['repaired_leaks'] += [lk for lk in site['active_leaks']
                                           if lk['status'] == 'repaired']
                site['active_leaks'] = [lk for lk in site['active_leaks']
                                        if lk['status'] != 'repaired']

        return

    def report(self):
        """
        Daily reporting of leaks, repairs, and emissions.
        """
        timeseries = self.timeseries
        state = self.state
        new_leaks = 0
        cum_repaired_leaks = 0
        daily_emissions_kg = 0
        # Update timeseries
        for site in state['sites']:
            new_leaks += site['n_new_leaks']
            cum_repaired_leaks += len(site['repaired_leaks'])
            # n_tags += site['n_new_leaks']
            # convert g/s to kg/day
            daily_emissions_kg += sum([lk['rate'] for lk in site['active_leaks']]) * 86.4
        cur_ts = [state['t'].current_timestep]
        timeseries['new_leaks'][cur_ts] = new_leaks
        timeseries['cum_repaired_leaks'][cur_ts] = cum_repaired_leaks
        timeseries['daily_emissions_kg'][cur_ts] = daily_emissions_kg
        timeseries['rolling_cost_estimate'][cur_ts] = sum(timeseries['total_daily_cost']) \
            / (len(timeseries['rolling_cost_estimate']) + 1) * 365 / 200
        # timeseries['n_tags'][state['t'].current_timestep] = len(state['tags'])
        return

    def finalize(self):
        """
        Compile and write output files.
        """
        params = self.parameters
        leaks = []
        if self.global_params['write_data']:
            # Attribute individual leak emissions to site totals
            for site in self.state['sites']:
                site['active_leak_cnt'] = len(site['active_leaks'])
                site['repaired_leak_cnt'] = len(site['repaired_leaks'])
                site['active_leak_emis'] = sum([lk['days_active'] * lk['rate'] * 86.4
                                                for lk in site['active_leaks']])
                site['repaired_leak_emis'] = sum([lk['days_active'] * lk['rate'] * 86.4
                                                  for lk in site['repaired_leaks']])
                site['mitigated_leak_emis_kg'] = sum(
                    [(self.parameters['NRd'] - lk['days_active']) * lk['rate'] * 86.4
                     for lk in site['repaired_leaks']])
                site['total_emissions_kg'] = site['active_leak_emis'] + site['repaired_leak_emis']

                leaks += site['active_leaks'] + site['repaired_leaks']
                del site['n_new_leaks']

            # campaign_df = pd.DataFrame(flatten_dict(self.state['campaigns'], parent_key='sub'))
            leak_df = pd.DataFrame(leaks)
            time_df = pd.DataFrame(self.timeseries)
            site_df = pd.DataFrame(self.state['sites'])

            # Create some new variables for plotting
            site_df['cum_frac_sites'] = list(site_df.index)
            site_df['cum_frac_sites'] = site_df['cum_frac_sites'] / max(site_df['cum_frac_sites'])
            site_df['cum_frac_emissions'] = np.cumsum(
                sorted(site_df['total_emissions_kg'], reverse=True))
            site_df['cum_frac_emissions'] = site_df['cum_frac_emissions'] \
                / max(site_df['cum_frac_emissions'])
            site_df['mean_rate_kg_day'] = site_df['total_emissions_kg'] / params['timesteps']
            leaks_active = leak_df[leak_df.status != 'repaired'] \
                .sort_values('rate', ascending=False)
            leaks_repaired = leak_df[leak_df.status == 'repaired'] \
                .sort_values('rate', ascending=False)

            leaks_active['cum_frac_leaks'] = list(np.linspace(0, 1, len(leaks_active)))
            leaks_active['cum_rate'] = np.cumsum(leaks_active['rate'])
            leaks_active['cum_frac_rate'] = leaks_active['cum_rate'] / max(leaks_active['cum_rate'])

            if len(leaks_repaired) > 0:
                leaks_repaired['cum_frac_leaks'] = list(np.linspace(0, 1, len(leaks_repaired)))
                leaks_repaired['cum_rate'] = np.cumsum(leaks_repaired['rate'])
                leaks_repaired['cum_frac_rate'] = leaks_repaired['cum_rate'] \
                    / max(leaks_repaired['cum_rate'])

            leak_df = leaks_active.append(leaks_repaired)

            # Write csv files
            leak_df.to_csv(
                params['output_directory']
                / 'leaks_output_{}.csv'.format(params['simulation']), index=False)
            time_df.to_csv(
                params['output_directory']
                / 'timeseries_output_{}.csv'.format(params['simulation']), index=False)

            site_df.to_csv(
                params['output_directory']
                / 'sites_output_{}.csv'.format(params['simulation']), index=False)

            # campaign_df.to_csv(
            #     params['output_directory']
            #     / 'campaigns_output_{}.csv'.format(params['simulation']), index=False)

            # Write metadata
            f_name = params['output_directory'] / "metadata_{}.txt".format(params['simulation'])
            metadata = open(f_name, 'w')
            metadata.write(str(params) + '\n' + str(datetime.datetime.now()))
            metadata.close()

        # Make maps and append site-level DD and MCB data
        if self.global_params['make_maps']:
            if params['simulation'] == '0':
                for m in self.state['methods']:
                    make_maps(m, site_df)
                    m.site_reports()

        # Make plots
        if self.global_params['make_plots']:
            make_plots(
                leak_df, time_df, site_df, params['simulation'],
                params['output_directory'])

        sim_summary = {
            'meta': params,
            'leaks': leak_df,
            'timeseries': time_df,
            'sites': site_df,
            #  'campaigns': campaign_df,
            'program_name': params['program_name'],
            'p_params': params,
        }

        return(sim_summary)
