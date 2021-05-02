# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Sensitivity analysis
# Purpose:     Module to enable sensitivity analysis
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
import numpy as np
import pandas as pd
import os
import time


class Sensitivity:
    def __init__(self, params, timeseries, state):
        """
        Initialize a sensitivity analysis for a given program.

        """
        self.parameters = params
        self.timeseries = timeseries
        self.state = state

        # Make folder for sensitivity analysis outputs
        self.output_directory = os.path.join(
            params['working_directory'],
            'sensitivity_analysis')
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # ------------------------Define SA input parameters----------------------------
        output_file = os.path.join(self.output_directory, 'SA_params.csv')
        param_df = pd.DataFrame()
        if params['simulation'] == '0' and params['sensitivity']['order'] == '1':
            for i in range(params['n_simulations']):
                row = {
                    # General inputs
                    'LSD_outliers': int(np.round(np.random.normal(0, 1))),
                    'LSD_samples':
                    int(np.random.normal(
                        len(state['empirical_leaks']),
                        len(state['empirical_leaks']) / 4)),
                    'LCD_outliers': int(np.round(np.random.normal(0, 1))),
                    'LCD_samples':
                    int(np.random.normal(
                        len(state['empirical_counts']),
                        len(state['empirical_counts']) / 4)),
                    'site_rate_outliers': int(np.round(np.random.normal(0, 1))),
                    'site_rate_samples':
                    int(np.random.normal(
                        len(state['empirical_sites']),
                        len(state['empirical_sites']) / 4)),
                    'offsite_times_outliers': int(np.round(np.random.normal(0, 1))),
                    'offsite_times_samples':
                    int(np.random.normal(
                        len(state['offsite_times']),
                        len(state['offsite_times']) / 4)),

                    'LPR': np.random.gamma(0.8327945, 0.03138632365),
                    'repair_delay': np.random.uniform(0, 100),
                    'operator_strength': np.random.exponential(0.1),
                    'max_det_op': np.random.exponential(1 / 5),
                    'consider_operator': bool(np.random.binomial(1, 0.2)),
                    'consider_daylight': bool(np.random.binomial(1, 0.5)),
                    'consider_venting': bool(np.random.binomial(1, 0.5)),
                    'max_workday': round(np.random.uniform(6, 14)),
                    'start_year': round(np.random.uniform(2003, 2012)),

                    # OGI inputs - only used if called
                    'OGI_n_crews': np.random.poisson(0.5) + 1,
                    'OGI_min_temp': np.random.normal(-20, 10),
                    'OGI_max_wind': np.random.normal(15, 3),
                    'OGI_max_precip': np.random.uniform(0, 0.1),  # in meters
                    'OGI_reporting_delay': np.random.uniform(0, 30),
                    'OGI_time': np.random.uniform(30, 500),
                    'OGI_RS': np.random.uniform(1, 4),
                    'OGI_min_interval': np.random.uniform(0, 90),
                    'OGI_MDL': np.random.uniform(0, 2),

                    # MGL inputs - only used if called
                    'truck_n_crews': np.random.poisson(0.5) + 1,
                    'truck_min_temp': np.random.normal(-20, 10),
                    'truck_max_wind': np.random.normal(15, 3),
                    'truck_max_precip': np.random.uniform(0, 0.1),
                    'truck_reporting_delay': np.random.uniform(0, 30),
                    'truck_time': np.random.uniform(1, 30),
                    'truck_RS': np.random.uniform(1, 4),
                    'truck_min_interval': np.random.uniform(0, 90),
                    'truck_MDL': np.random.uniform(1, 100),  # grams/hour
                    'truck_follow_up_thresh': np.random.uniform(0, 500),
                    'truck_follow_up_prop': np.random.uniform(0.1, 1)
                }
                param_df = param_df.append(pd.DataFrame([row]))
            param_df.to_csv(output_file, index=False)

        while not os.path.exists(output_file):
            time.sleep(1)
        if os.path.isfile(output_file):
            params = pd.read_csv(output_file)
            current_row = params.iloc[int(params['simulation'])]
            self.SA_params = current_row.to_dict()

        # --------------Update model parameters according to SA definition--------------

        params['LPR'] = self.SA_params['LPR']
        params['start_year'] = self.SA_params['start_year']
        params['repair_delay'] = self.SA_params['repair_delay']
        params['operator_strength'] = self.SA_params['operator_strength']
        params['max_det_op'] = self.SA_params['max_det_op']
        params['consider_operator'] = self.SA_params['consider_operator']
        params['consider_daylight'] = self.SA_params['consider_daylight']
        params['consider_venting'] = self.SA_params['consider_venting']

        # Modify input distributions
        state['empirical_leaks'] = self.adjust_distribution(
            state['empirical_leaks'],
            self.SA_params['LSD_outliers'],
            self.SA_params['LSD_samples'])
        state['empirical_counts'] = self.adjust_distribution(
            state['empirical_counts'],
            self.SA_params['LCD_outliers'],
            self.SA_params['LCD_samples'])
        state['offsite_times'] = self.adjust_distribution(
            state['offsite_times'],
            self.SA_params['offsite_times_outliers'],
            self.SA_params['offsite_times_samples'])
        if params['consider_venting']:
            state['empirical_sites'] = self.adjust_distribution(
                state['empirical_sites'],
                self.SA_params['site_rate_outliers'],
                self.SA_params['site_rate_samples'])

        # Set OGI parameters
        methods = params['methods']
        if params['sensitivity']['program'] == 'OGI':
            methods['OGI']['max_workday'] = self.SA_params['max_workday']
            methods['OGI']['n_crews'] = self.SA_params['OGI_n_crews']
            methods['OGI']['min_temp'] = self.SA_params['OGI_min_temp']
            methods['OGI']['max_wind'] = self.SA_params['OGI_max_wind']
            methods['OGI']['max_precip'] = self.SA_params['OGI_max_precip']
            methods['OGI']['min_interval'] = self.SA_params['OGI_min_interval']
            methods['OGI']['reporting_delay'] = self.SA_params['OGI_reporting_delay']
            methods['OGI']['MDL'][0] = self.SA_params['OGI_MDL']

            for site in state['sites']:
                site['OGI_time'] = self.SA_params['OGI_time']
                site['OGI_RS'] = self.SA_params['OGI_RS']

        # Set screening (truck) parameters
        if params['sensitivity']['program'] == 'truck':
            methods['OGI_FU']['max_workday'] = self.SA_params['max_workday']
            methods['OGI_FU']['n_crews'] = self.SA_params['OGI_n_crews']
            methods['OGI_FU']['min_temp'] = self.SA_params['OGI_min_temp']
            methods['OGI_FU']['max_wind'] = self.SA_params['OGI_max_wind']
            methods['OGI_FU']['max_precip'] = self.SA_params['OGI_max_precip']
            methods['OGI_FU']['min_interval'] = self.SA_params['OGI_min_interval']
            methods['OGI_FU']['reporting_delay'] = self.SA_params['OGI_reporting_delay']
            methods['OGI_FU']['MDL'][0] = self.SA_params['OGI_MDL']

            methods['truck']['max_workday'] = self.SA_params['max_workday']
            methods['truck']['min_temp'] = self.SA_params['truck_min_temp']
            methods['truck']['max_wind'] = self.SA_params['truck_max_wind']
            methods['truck']['max_precip'] = self.SA_params['truck_max_precip']
            methods['truck']['min_interval'] = self.SA_params['truck_min_interval']
            methods['truck']['reporting_delay'] = self.SA_params['truck_reporting_delay']
            methods['truck']['MDL'] = self.SA_params['truck_MDL']
            methods['truck']['follow_up_thresh'] = self.SA_params['truck_follow_up_thresh']
            methods['truck']['follow_up_prop'] = self.SA_params['truck_follow_up_prop']

            for site in state['sites']:
                site['OGI_time'] = self.SA_params['OGI_time']
                site['OGI_FU_time'] = self.SA_params['OGI_time']
                site['OGI_RS'] = self.SA_params['OGI_RS']
                site['truck_time'] = self.SA_params['truck_time']
                site['truck_RS'] = self.SA_params['truck_RS']

        return

    # ------------------------------------------------------------------------------

    def write_data(self):
        params = self.parameters
        timeseries = self.timeseries
        state = self.state

        # Build generic output dataframe
        df_dict = {
            # SA inputs
            'program': params['sensitivity']['program'],
            'simulation': params['simulation'],
            'run_time': time.time() - params['start_time'],
            'timesteps': params['timesteps'],
            'spin_up': params['spin_up'],
            'start_year': params['start_year'],
            'LSD_outliers': self.SA_params['LSD_outliers'],
            'LSD_samples': self.SA_params['LSD_samples'],
            'LCD_outliers': self.SA_params['LCD_outliers'],
            'LCD_samples': self.SA_params['LCD_samples'],
            'site_rate_outliers': self.SA_params['site_rate_outliers'],
            'site_rate_samples': self.SA_params['site_rate_samples'],
            'offsite_times_outliers': self.SA_params['offsite_times_outliers'],
            'offsite_times_samples': self.SA_params['offsite_times_samples'],
            'LPR': self.SA_params['LPR'],
            'repair_delay': self.SA_params['repair_delay'],
            'operator_strength': self.SA_params['operator_strength'],
            'max_det_op': self.SA_params['max_det_op'],
            # SA outputs
            'dail_site_em':
                np.mean(np.array(timeseries['daily_emissions_kg']
                                 [params['spin_up']:]) / len(state['sites'])),
            'std_dail_site_em':
                np.std(np.array(timeseries['daily_emissions_kg']
                                [params['spin_up']:]) / len(state['sites'])),
            'cum_repaired_leaks': timeseries['cum_repaired_leaks'][-1:][0],
            'med_active_leaks':
                np.median(np.array(timeseries['active_leaks'][params['spin_up']:])),
            'med_days_active': np.median(pd.DataFrame(state['leaks'])['days_active']),
            'med_leak_rate': np.median(pd.DataFrame(state['leaks'])['rate']),
            'med_vent_rate': np.median(state['empirical_vents']),
            'cum_init_leaks': np.sum(pd.DataFrame(state['sites'])['initial_leaks']),
        }

        # If this is an operator program, you're done - export the data
        if params['sensitivity']['program'] == 'operator':
            self.export_SA(df_dict, self.output_directory, 'sensitivity_operator.csv')

            # Otherwise, this is an LDAR program - add generic inputs
        generic_dict = {
            'max_workday': self.SA_params['max_workday'],
            'consider_operator': self.SA_params['consider_operator'],
            'consider_daylight': self.SA_params['consider_daylight'],
            'consider_venting': self.SA_params['consider_venting']
        }
        df_dict.update(generic_dict)

        # If this is an OGI program, add relevant variables to dictionary before exporting
        if params['sensitivity']['program'] == 'OGI':
            OGI_dict = {
                # New OGI inputs
                'OGI_n_crews': self.SA_params['OGI_n_crews'],
                'OGI_min_temp': self.SA_params['OGI_min_temp'],
                'OGI_max_wind': self.SA_params['OGI_max_wind'],
                'OGI_max_precip': self.SA_params['OGI_max_precip'],
                'OGI_min_interval': self.SA_params['OGI_min_interval'],
                'OGI_reporting_delay': self.SA_params['OGI_reporting_delay'],
                'OGI_MDL': self.SA_params['OGI_MDL'],
                'OGI_time': self.SA_params['OGI_time'],
                'OGI_RS': self.SA_params['OGI_RS'],

                # New OGI outputs
                'OGI_cum_program_cost':
                    np.sum(np.array(timeseries['OGI_cost'][params['spin_up']:])),
                'OGI_prop_sites_avail': np.mean(
                    np.array(timeseries['OGI_prop_sites_avail'][params['spin_up']:])),
                'OGI_cum_missed_leaks':
                    np.sum(pd.DataFrame(state['sites'])['OGI_missed_leaks']),
                'OGI_cum_surveys':
                    np.sum(pd.DataFrame(state['sites'])['OGI_surveys_conducted'])
            }

            df_dict.update(OGI_dict)
            self.export_SA(df_dict, self.output_directory, 'sensitivity_OGI.csv')

        # If this is a screening (truck) program, add relevant variables to dictionary
        #  before exporting
        if params['sensitivity']['program'] == 'truck':
            truck_dict = {
                # New OGI_FU inputs
                'OGI_FU_n_crews': self.SA_params['OGI_n_crews'],
                'OGI_FU_min_temp': self.SA_params['OGI_min_temp'],
                'OGI_FU_max_wind': self.SA_params['OGI_max_wind'],
                'OGI_FU_max_precip': self.SA_params['OGI_max_precip'],
                'OGI_FU_min_interval': self.SA_params['OGI_min_interval'],
                'OGI_FU_reporting_delay': self.SA_params['OGI_reporting_delay'],
                'OGI_FU_MDL': self.SA_params['OGI_MDL'],
                'OGI_FU_time': self.SA_params['OGI_time'],

                # New truck inputs
                'truck_n_crews': self.SA_params['truck_n_crews'],
                'truck_min_temp': self.SA_params['truck_min_temp'],
                'truck_max_wind': self.SA_params['truck_max_wind'],
                'truck_max_precip': self.SA_params['truck_max_precip'],
                'truck_min_interval': self.SA_params['truck_min_interval'],
                'truck_reporting_delay': self.SA_params['truck_reporting_delay'],
                'truck_MDL': self.SA_params['truck_MDL'],
                'truck_follow_up_thresh': self.SA_params['truck_follow_up_thresh'],
                'truck_follow_up_prop': self.SA_params['truck_follow_up_prop'],
                'truck_time': self.SA_params['truck_time'],
                'truck_RS': self.SA_params['truck_RS'],

                # New OGI_FU outputs
                'OGI_FU_cum_program_cost': np.sum(
                    np.array(timeseries['OGI_FU_cost'][params['spin_up']:])),
                'OGI_FU_prop_sites_avail': np.mean(
                    np.array(timeseries['OGI_FU_prop_sites_avail'][params['spin_up']:])),
                'OGI_FU_cum_missed_leaks':
                    np.sum(pd.DataFrame(state['sites'])['OGI_FU_missed_leaks']),
                'OGI_FU_cum_surveys':
                    np.sum(pd.DataFrame(state['sites'])['OGI_FU_surveys_conducted']),

                # New truck outputs
                'truck_cum_program_cost':
                    np.sum(np.array(timeseries['truck_cost'][params['spin_up']:])),
                'truck_prop_sites_avail':
                    np.mean(np.array(timeseries['truck_prop_sites_avail'][params['spin_up']:])),
                'truck_cum_missed_leaks':
                    np.sum(pd.DataFrame(state['sites'])['truck_missed_leaks']),
                'truck_cum_surveys':
                    np.sum(pd.DataFrame(state['sites'])['truck_surveys_conducted']),
                'truck_cum_eff_flags':
                    np.sum(np.array(timeseries['truck_eff_flags'][params['spin_up']:]))
            }

            df_dict.update(truck_dict)
            self.export_SA(df_dict, self.output_directory, 'sensitivity_truck.csv')

        return (df_dict)

    def adjust_distribution(self, distribution, outliers, samples):
        if outliers < 0:
            for i in range(abs(outliers)):
                distribution = np.delete(distribution, np.where(distribution == max(distribution)))
        if outliers > 0:
            for i in range(outliers):
                new_value = max(distribution) * 2
                distribution = np.append(distribution, new_value)
        while samples < 10:
            samples = int(np.random.normal(len(distribution), len(distribution) / 4))
        distribution = np.random.choice(distribution, samples)
        return distribution

    def export_SA(self, dictionary, output_directory, name):
        if 'write_results_postsim' in self.parameters['sensitivity']:
            export_data = self.parameters['sensitivity']['write_results_postsim']
        else:
            export_data = True

        if export_data:
            df_new = pd.DataFrame([dictionary])
            output_file = os.path.join(output_directory, name)
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index=False)
            elif os.path.exists(output_file):
                for attempts in range(int(1e10)):
                    try:
                        df_old = pd.read_csv(output_file)
                        break
                    except:  # noqa HBD - probably IOError
                        continue

                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index=False)
        return
