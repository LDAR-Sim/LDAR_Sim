# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim
# Purpose:     Primary module of LDAR-Sim
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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

import pandas as pd
import numpy as np
import csv
import os
import datetime
import sys
import random
from sensitivity import Sensitivity
from operator_agent import OperatorAgent
from plotter import make_plots
from daylight_calculator import DaylightCalculatorAve
from generic_functions import make_maps
from leak_processing.distributions import fit_dist, dist_rvs


class LdarSim:
    def __init__(self, state, params, timeseries):
        """
        Construct the simulation.
        """

        self.state = state
        self.parameters = params
        self.timeseries = timeseries
        self.active_leaks = []

        # Read in data files
        state['empirical_counts'] = np.array(pd.read_csv(
            params['working_directory'] + params['count_file']).iloc[:, 0])
        state['empirical_leaks'] = np.array(pd.read_csv(
            params['working_directory'] + params['leak_file']).iloc[:, 0])
        state['empirical_sites'] = np.array(pd.read_csv(
            params['working_directory'] + params['vent_file']).iloc[:, 0])
        state['offsite_times'] = np.array(pd.read_csv(
            params['working_directory'] + params['t_offsite_file']).iloc[:, 0])
        if "leak_size_dist" in params:
            # Currently Accepts only lognormal leak distributions
            _, mu, sigma = params['leak_size_dist']
            state['leak_distribution'] = fit_dist(mu=mu, sigma=sigma)
        else:
            state['leak_distribution'] = fit_dist(samples=state['empirical_leaks'])
        if 'max_leak_size' in params:
            state['max_rate'] = params['max_leak_size']
        else:
            state['max_rate'] = max(state['empirical_leaks'])
        if "leak_size_dist_togpsec" in params:
            state['leak_size_scaler'] = params['leak_size_scaler']
        else:
            state['leak_size_scaler'] = 1
        if "consider_weather" in params:
            state['consider_weather'] = params['consider_weather']

        # Read in the sites as a list of dictionaries
        with open(params['working_directory'] + params['infrastructure_file']) as f:
            state['sites'] = [{k: v for k, v in row.items()}
                              for row in csv.DictReader(f, skipinitialspace=True)]

        # Sample sites
        if params['site_samples'][0]:
            state['sites'] = random.sample(
                state['sites'],
                params['site_samples'][1])

        if params['subtype_times'][0]:
            subtype_times = pd.read_csv(params['subtype_times'][1])
            cols_to_add = subtype_times.columns[1:].tolist()
            for col in cols_to_add:
                for site in state['sites']:
                    site[col] = subtype_times.loc[subtype_times['subtype_code'] ==
                                                  int(site['subtype_code']), col].iloc[0]

        # Shuffle all the entries to randomize order for identical 't_Since_last_LDAR' values
        random.shuffle(state['sites'])

        # Additional variable(s) for each site
        for site in state['sites']:
            site.update({'total_emissions_kg': 0})
            site.update({'active_leaks': 0})
            site.update({'repaired_leaks': 0})
            site.update({'currently_flagged': False})
            site.update({'flagged_by': None})
            site.update({'date_flagged': None})
            site.update({'lat_index': min(
                range(len(state['weather'].latitude)), key=lambda i: abs(
                    state['weather'].latitude[i] - float(site['lat'])))})
            site.update({'lon_index': min(
                range(len(state['weather'].longitude)), key=lambda i: abs(
                    state['weather'].longitude[i] - float(site['lon']) % 360))})

            # Check to make sure site is within range of grid-based data
            if float(site['lat']) > max(state['weather'].latitude):
                sys.exit(
                    'Simulation terminated: One or more sites is too '
                    'far North and is outside the spatial bounds of '
                    'your weather data!')
            if float(site['lat']) < min(state['weather'].latitude):
                sys.exit(
                    'Simulation terminated: One or more sites is too '
                    'far South and is outside the spatial bounds of '
                    'your weather data!')
            if float(site['lon']) > max(state['weather'].longitude):
                sys.exit(
                    'Simulation terminated: One or more sites is too '
                    'far East and is outside the spatial bounds of '
                    'your weather data!')
            if float(site['lon']) < min(state['weather'].longitude):
                sys.exit(
                    'Simulation terminated: One or more sites is too'
                    'far West and is outside the spatial bounds of '
                    'your weather data!')

        # Additional timeseries variables
        timeseries['total_daily_cost'] = np.zeros(params['timesteps'])
        timeseries['repair_cost'] = np.zeros(params['timesteps'])
        timeseries['verification_cost'] = np.zeros(params['timesteps'])
        timeseries['operator_redund_tags'] = np.zeros(self.parameters['timesteps'])
        timeseries['operator_tags'] = np.zeros(self.parameters['timesteps'])

        # Configure sensitivity analysis, if requested (code block must remain here -
        # after site initialization and before method initialization)
        if params['sensitivity']['perform']:
            self.sensitivity = Sensitivity(params, timeseries, state)

        # Initialize method(s) to be used; append to state
        for m in params['methods']:
            try:
                company_name = str(m) + '_company'
                module = __import__(company_name)
                func = getattr(module, company_name)
                state['methods'].append(
                    func(state, params, params['methods'][m], timeseries))
            except AttributeError:
                print('Cannot add this method: ' + m)

        # Generate initial leak count for each site
        for site in state['sites']:
            n_leaks = random.choice(state['empirical_counts'])
            if n_leaks < 0:  # This can happen occasionally during sensitivity analysis
                n_leaks = 0
            site.update({'initial_leaks': n_leaks})
            state['init_leaks'].append(site['initial_leaks'])

        # For each leak, create a dictionary and populate values for relevant keys
        for site in state['sites']:
            if site['initial_leaks'] > 0:
                for leak in range(site['initial_leaks']):
                    leaksize = dist_rvs(state['leak_distribution'], state['max_rate'],
                                        state['leak_size_scaler'])
                    state['leaks'].append({
                        'leak_ID': site['facility_ID'] + '_' + str(len(state['leaks']) + 1)
                        .zfill(10),
                        'facility_ID': site['facility_ID'],
                        'rate': leaksize,
                        'lat': float(site['lat']) + np.random.normal(0, 0.0001),
                        'lon': float(site['lon']) + np.random.normal(0, 0.0001),
                        'status': 'active',
                        'tagged': False,
                        'days_active': 0,
                        'component': 'unknown',
                        'date_began': state['t'].current_date,
                        'date_tagged': None,
                        'tagged_by_company': None,
                        'tagged_by_crew': None,
                        'requires_shutdown': False,
                        'date_repaired': None,
                        'repair_delay': None,
                    })

        # Initialize operator
        if params['consider_operator']:
            state['operator'] = OperatorAgent(timeseries, params, state)

        # If working without methods (operator only), need to get the first day going
        if not bool(params['methods']):
            state['t'].current_date = state['t'].current_date.replace(hour=1)

        # Initialize daylight
        calculate_daylight = False
        for m in params['methods']:
            if params['methods'][m]['consider_daylight']:
                calculate_daylight = True
        if calculate_daylight:
            state['daylight'] = DaylightCalculatorAve(state, params)

        # Initialize empirical distribution of vented emissions
        if params['consider_venting']:
            state['empirical_vents'] = []

            # Run Monte Carlo simulations to get distribution of vented emissions
            for i in range(1000):
                n_mc_leaks = random.choice(state['empirical_counts'])
                mc_leaks = []
                for leak in range(n_mc_leaks):
                    leaksize = dist_rvs(state['leak_distribution'], state['max_rate'],
                                        state['leak_size_scaler'])
                    mc_leaks.append(n_mc_leaks=leaksize)

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
        self.find_leaks()  # Find leaks
        self.repair_leaks()  # Repair leaks
        self.report()  # Assemble any reporting about model state
        return

    def update_state(self):
        """
        update the state of active leaks
        """
        self.active_leaks = []
        for leak in self.state['leaks']:
            if leak['status'] == 'active':
                leak['days_active'] += 1
                self.active_leaks.append(leak)

                # Tag by operator if leak is due for NR
                if leak['days_active'] == self.parameters['NRd']:
                    if leak['tagged']:
                        self.timeseries['operator_redund_tags'][
                            self.state['t'].current_timestep] += 1

                    elif not leak['tagged']:
                        # Add these leaks to the 'tag pool'
                        leak['tagged'] = True
                        leak['date_tagged'] = self.state['t'].current_date
                        leak['tagged_by_company'] = 'operator'
                        leak['tagged_by_crew'] = 1
                        self.state['tags'].append(leak)
                        self.timeseries['operator_tags'][self.state['t'].current_timestep] += 1

        self.timeseries['active_leaks'].append(len(self.active_leaks))
        self.timeseries['datetime'].append(self.state['t'].current_date)

    def add_leaks(self):
        """
        add new leaks to the leak pool
        """
        # First, determine whether each site gets a new leak or not
        for site in self.state['sites']:
            n_leaks = np.random.binomial(1, self.parameters['LPR'])
            if n_leaks == 0:
                site.update({'n_new_leaks': 0})
            else:
                site.update({'n_new_leaks': n_leaks})

        # For each leak, create a dictionary and populate values for relevant keys
        for site in self.state['sites']:
            if site['n_new_leaks'] > 0:
                for leak in range(site['n_new_leaks']):
                    leaksize = dist_rvs(self.state['leak_distribution'], self.state['max_rate'],
                                        self.state['leak_size_scaler'])
                    self.state['leaks'].append({
                        'leak_ID': site['facility_ID'] + '_' + str(len(self.state['leaks']) + 1)
                        .zfill(10),
                        'facility_ID': site['facility_ID'],
                        'rate': leaksize,
                        'lat': float(site['lat']),
                        'lon': float(site['lon']),
                        'status': 'active',
                        'days_active': 0,
                        'tagged': False,
                        'component': 'unknown',
                        'date_began': self.state['t'].current_date,
                        'date_tagged': None,
                        'tagged_by_company': None,
                        'tagged_by_crew': None,
                        'requires_shutdown': False,
                        'date_repaired': None,
                        'repair_delay': None,
                    })

        return

    def find_leaks(self):
        """
        Loop over all your methods in the simulation and ask them to find some leaks.
        """

        for m in self.state['methods']:
            m.find_leaks()

        if self.parameters['consider_operator']:
            if self.state['t'].current_date.weekday() == 0:
                self.state['operator'].work_a_day()

        return

    def repair_leaks(self):
        """
        Repair tagged leaks and remove from tag pool.
        """
        params = self.parameters
        timeseries = self.timeseries
        state = self.state

        for tag in state['tags']:
            if tag['tagged_by_company'] != 'operator':
                if (state['t'].current_date - tag['date_tagged']).days \
                    >= (params['repair_delay'] + params[
                        'methods'][tag['tagged_by_company']]['reporting_delay']):
                    tag['status'] = 'repaired'
                    tag['tagged'] = False
                    tag['date_repaired'] = state['t'].current_date
                    tag['repair_delay'] = (tag['date_repaired'] - tag['date_tagged']).days
                    timeseries['repair_cost'][state['t'].current_timestep] += params['repair_cost']
                    timeseries['total_daily_cost'][state['t'].current_timestep] \
                        += params['repair_cost'] + params['verification_cost']
                    timeseries['verification_cost'][
                        state['t'].current_timestep] += params['verification_cost']
            elif tag['tagged_by_company'] == 'operator':
                if (state['t'].current_date - tag['date_tagged']).days >= params['repair_delay']:
                    tag['status'] = 'repaired'
                    tag['tagged'] = False
                    tag['date_repaired'] = state['t'].current_date
                    tag['repair_delay'] = (tag['date_repaired'] - tag['date_tagged']).days
                    timeseries['repair_cost'][state['t'].current_timestep] += params['repair_cost']
                    timeseries['total_daily_cost'][state['t'].current_timestep] \
                        += params['repair_cost'] + params['verification_cost']

            state['tags'] = [tag for tag in state['tags'] if tag['status'] == 'active']

        return

    def report(self):
        """
        Daily reporting of leaks, repairs, and emissions.
        """
        timeseries = self.timeseries
        state = self.state

        # Update timeseries
        timeseries['new_leaks'].append(sum([d['n_new_leaks'] for d in state['sites']]))
        timeseries['cum_repaired_leaks'].append(
            sum([d['status'] == 'repaired' for d in state['leaks']]))
        # convert g/s to kg/day
        timeseries['daily_emissions_kg'].append(sum([d['rate'] for d in self.active_leaks]) * 86.4)
        timeseries['n_tags'].append(len(state['tags']))
        timeseries['rolling_cost_estimate'].append(
            sum(timeseries['total_daily_cost']) /
            (len(timeseries['rolling_cost_estimate']) + 1) * 365 / 200)

        return

    def finalize(self):
        """
        Compile and write output files.
        """
        params = self.parameters

        if params['write_data']:
            # Attribute individual leak emissions to site totals
            for leak in self.state['leaks']:
                # convert g/s to kg/day
                tot_emissions_kg = leak['days_active'] * leak['rate'] * 86.4
                for site in self.state['sites']:
                    if site['facility_ID'] == leak['facility_ID']:
                        site['total_emissions_kg'] += tot_emissions_kg
                        if leak['status'] == 'active':
                            site['active_leaks'] += 1
                        elif leak['status'] == 'repaired':
                            site['repaired_leaks'] += 1
                        break

            # Generate some dataframes
            for site in self.state['sites']:
                del site['n_new_leaks']

            leak_df = pd.DataFrame(self.state['leaks'])
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
            leaks_active = leak_df[leak_df.status == 'active'].sort_values('rate', ascending=False)
            leaks_repaired = leak_df[leak_df.status
                                     == 'repaired'].sort_values('rate', ascending=False)

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
                params['output_directory'] + '/leaks_output_' + params
                ['simulation'] + '.csv', index=False)
            time_df.to_csv(
                params['output_directory'] + '/timeseries_output_' + params
                ['simulation'] + '.csv', index=False)
            site_df.to_csv(
                params['output_directory'] + '/sites_output_' + params
                ['simulation'] + '.csv', index=False)

            # Write metadata
            f_name = "{}/metadata_{}.txt".format(params['output_directory'], params['simulation'])
            metadata = open(f_name, 'w')
            metadata.write(str(params) + '\n' + str(datetime.datetime.now()))
            metadata.close()

        # Make maps and append site-level DD and MCB data
        if params['make_maps']:
            if params['simulation'] == '0':
                for m in self.state['methods']:
                    make_maps(m, site_df)
                    m.site_reports()

        # Make plots
        if params['make_plots']:
            make_plots(
                leak_df, time_df, site_df, params['simulation'],
                params['spin_up'],
                params['output_directory'])

        # Write sensitivity analysis data, if requested
        if params['sensitivity']['perform']:
            sim_summary = self.sensitivity.write_data()
        else:
            sim_summary = {}

        # Return to original working directory
        os.chdir(params['working_directory'])
        os.chdir('..')

        return(sim_summary)
