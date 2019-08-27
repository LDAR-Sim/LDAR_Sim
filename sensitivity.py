#------------------------------------------------------------------------------
# Name:         LDAR-Sim Sensitivity Analysis - Operator
#
# Authors:      Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:      2019-Jul-02
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import os
import time

class sensitivity:
    def __init__ (self, parameters, timeseries, state):
        '''
        Initialize a sensitivity analysis for a given program.

        '''   
        self.parameters = parameters
        self.timeseries = timeseries
        self.state = state

        # Make folder for sensitivity analysis outputs
        self.output_directory = os.path.join(self.parameters['working_directory'], self.parameters['output_folder'], 'sensitivity_analysis')
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory) 
        
#------------------------Define SA input parameters----------------------------

        self.SA_params = {
        
        # General inputs
        'LSD_outliers': int(np.round(np.random.normal(0, 1))),
        'LSD_samples': int(np.random.normal(len(self.state['empirical_leaks']), len(self.state['empirical_leaks'])/4)),
        
        'LCD_outliers': int(np.round(np.random.normal(0, 1))),
        'LCD_samples': int(np.random.normal(len(self.state['empirical_counts']), len(self.state['empirical_counts'])/4)),
        
        'site_rate_outliers': int(np.round(np.random.normal(0, 1))),
        'site_rate_samples': int(np.random.normal(len(self.state['empirical_sites']), len(self.state['empirical_sites'])/4)),
        
        'LPR': np.random.gamma(1.39, 0.00338),
        'repair_delay': np.random.uniform(0, 100),
        'operator_strength':np.random.exponential(0.1),
        'max_det_op': np.random.exponential(1/10),
        'consider_daylight': bool(np.random.binomial(1, 0.5)),
        'consider_venting': bool(np.random.binomial(1, 0.5)),
        'max_workday': round(np.random.uniform(6, 14)),
        'start_year':round(np.random.uniform(2003, 2012)),

        # OGI inputs - only used if called      
        'OGI_n_crews': np.random.poisson(0.5) + 1,
        'OGI_min_temp': np.random.normal(-20, 10),
        'OGI_max_wind': np.random.normal(15, 3), 
        'OGI_max_precip': np.random.normal(3, 1), # Need to change according to measurement units
        'OGI_reporting_delay': np.random.uniform(0,7),
        'OGI_time': np.random.uniform(30,300),
        'OGI_required_surveys': np.random.uniform(1, 4),
        'OGI_min_interval': np.random.uniform(0, 90),
        'OGI_MDL': np.random.uniform(0, 2.5),
        
        # Aircraft inputs - only used if called
        'aircraft_n_crews': np.random.poisson(0.5) + 1,
        'aircraft_min_temp': np.random.normal(-20, 10),
        'aircraft_max_wind': np.random.normal(15, 3),
        'aircraft_max_precip': np.random.normal(3, 1),
        'aircraft_reporting_delay': np.random.uniform(0,7),
        'aircraft_time': np.random.uniform(1,20),
        'aircraft_required_surveys': np.random.uniform(1, 4),
        'aircraft_min_interval': np.random.uniform(0, 90),
        'aircraft_MDL': np.random.uniform(1000, 10000), # grams/hour
        'aircraft_follow_up_thresh': np.random.uniform(0, 10000)
        }
        
        # If batch, must communicate global parameters to next program
        if self.parameters['sensitivity']['batch'] == [True, 1]:
            self.export_SA (self.SA_params, os.path.join(self.parameters['working_directory'], self.parameters['master_output_folder']), 'batch_params.csv')
        
        # Go find the secret message!
        if self.parameters['sensitivity']['batch'] == [True, 2]:
            B1_params = pd.read_csv(os.path.join(self.parameters['working_directory'], self.parameters['master_output_folder'], 'batch_params.csv'))
            B1_params_row = B1_params.iloc[int(self.parameters['simulation'])]
            B1_dict = B1_params_row.to_dict()
            self.SA_params.update(B1_dict)            
            
            
#--------------Update model parameters according to SA definition--------------

        self.parameters['LPR'] = self.SA_params['LPR']
        self.parameters['start_year'] = self.SA_params['start_year']
        self.parameters['repair_delay'] = self.SA_params['repair_delay']
        self.parameters['operator_strength'] = self.SA_params['operator_strength']
        self.parameters['max_det_op'] = self.SA_params['max_det_op']
        self.parameters['consider_daylight'] = self.SA_params['consider_daylight']
        self.parameters['consider_venting'] = self.SA_params['consider_venting']
        
        # Modify input distributions
        self.adjust_distribution(self.state['empirical_leaks'], self.SA_params['LSD_outliers'], self.SA_params['LSD_samples'])
        self.adjust_distribution(self.state['empirical_counts'], self.SA_params['LCD_outliers'], self.SA_params['LCD_samples'])
        if self.parameters['consider_venting'] == True:
            self.adjust_distribution(self.state['empirical_sites'], self.SA_params['site_rate_outliers'], self.SA_params['site_rate_samples'])
        
        # Set OGI parameters                      
        if self.parameters['sensitivity']['program'] == 'OGI':
            self.parameters['methods']['OGI']['max_workday'] = self.SA_params['max_workday']
            self.parameters['methods']['OGI']['n_crews'] = self.SA_params['OGI_n_crews']
            self.parameters['methods']['OGI']['min_temp'] = self.SA_params['OGI_min_temp']
            self.parameters['methods']['OGI']['max_wind'] = self.SA_params['OGI_max_wind']
            self.parameters['methods']['OGI']['max_precip'] = self.SA_params['OGI_max_precip']
            self.parameters['methods']['OGI']['min_interval'] = self.SA_params['OGI_min_interval']
            self.parameters['methods']['OGI']['reporting_delay'] = self.SA_params['OGI_reporting_delay']
            self.parameters['methods']['OGI']['MDL'][0] = self.SA_params['OGI_MDL']
    
            for site in self.state['sites']:
                site['OGI_time'] = self.SA_params['OGI_time']
                site['OGI_required_surveys'] = self.SA_params['OGI_required_surveys']

        # Set screening (aircraft) parameters                      
        if self.parameters['sensitivity']['program'] == 'aircraft':
            self.parameters['methods']['OGI_FU']['max_workday'] = self.SA_params['max_workday']
            self.parameters['methods']['OGI_FU']['n_crews'] = self.SA_params['OGI_n_crews']
            self.parameters['methods']['OGI_FU']['min_temp'] = self.SA_params['OGI_min_temp']
            self.parameters['methods']['OGI_FU']['max_wind'] = self.SA_params['OGI_max_wind']
            self.parameters['methods']['OGI_FU']['max_precip'] = self.SA_params['OGI_max_precip']
            self.parameters['methods']['OGI_FU']['min_interval'] = self.SA_params['OGI_min_interval']
            self.parameters['methods']['OGI_FU']['reporting_delay'] = self.SA_params['OGI_reporting_delay']
            self.parameters['methods']['OGI_FU']['MDL'][0] = self.SA_params['OGI_MDL']
            
            self.parameters['methods']['aircraft']['max_workday'] = self.SA_params['max_workday']
            self.parameters['methods']['aircraft']['min_temp'] = self.SA_params['aircraft_min_temp']
            self.parameters['methods']['aircraft']['max_wind'] = self.SA_params['aircraft_max_wind']
            self.parameters['methods']['aircraft']['max_precip'] = self.SA_params['aircraft_max_precip']
            self.parameters['methods']['aircraft']['min_interval'] = self.SA_params['aircraft_min_interval']
            self.parameters['methods']['aircraft']['reporting_delay'] = self.SA_params['aircraft_reporting_delay']
            self.parameters['methods']['aircraft']['MDL'] = self.SA_params['aircraft_MDL']
            self.parameters['methods']['aircraft']['follow_up_thresh'] = self.SA_params['aircraft_follow_up_thresh']
            
            for site in self.state['sites']:
                site['OGI_time'] = self.SA_params['OGI_time']
                site['OGI_required_surveys'] = self.SA_params['OGI_required_surveys']
                site['aircraft_time'] = self.SA_params['aircraft_time']
                site['aircraft_required_surveys'] = self.SA_params['aircraft_required_surveys']
            
        return

#------------------------------------------------------------------------------
        
    def write_data (self):
                               
        # Build generic output dataframe
        df_dict = {
        # SA inputs
        'simulation': self.parameters['simulation'],
        'run_time': time.time() - self.parameters['start_time'],
        'timesteps': self.parameters['timesteps'],
        'spin_up': self.parameters['spin_up'],
        'start_year':self.parameters['start_year'],
        'LSD_outliers': self.SA_params['LSD_outliers'],
        'LSD_samples': self.SA_params['LSD_samples'],
        'LCD_outliers': self.SA_params['LCD_outliers'],
        'LCD_samples': self.SA_params['LCD_samples'],
        'site_rate_outliers': self.SA_params['site_rate_outliers'],
        'site_rate_samples': self.SA_params['site_rate_samples'],
        'LPR': self.SA_params['LPR'],
        'repair_delay': self.SA_params['repair_delay'],
        'operator_strength':self.SA_params['operator_strength'],
        'max_det_op': self.SA_params['max_det_op'],

        # SA outputs
        'mean_dail_site_em': np.mean(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
        'std_dail_site_em': np.std(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
        'cum_repaired_leaks': self.timeseries['cum_repaired_leaks'][-1:],
        'med_active_leaks': np.median(np.array(self.timeseries['active_leaks'][self.parameters['spin_up']:])),
        'med_days_active': np.median(pd.DataFrame(self.state['leaks'])['days_active']),
        'med_leak_rate': np.median(pd.DataFrame(self.state['leaks'])['rate']),
        'cum_init_leaks': np.sum(pd.DataFrame(self.state['sites'])['initial_leaks'])
                }

        # If this is an operator program, you're done - export the data
        if self.parameters['sensitivity']['program'] == 'operator':            
            self.export_SA(df_dict, self.output_directory, 'sensitivity_operator.csv')                          
                

        # Otherwise, this is an LDAR program - add generic inputs
        generic_dict = {
                'max_workday': self.SA_params['max_workday'],
                'consider_daylight': self.SA_params['consider_daylight'],
                'consider_venting': self.SA_params['consider_venting']
                }       
        df_dict.update(generic_dict)
        
        # If this is an OGI program, add relevant variables to dictionary before exporting
        if self.parameters['sensitivity']['program'] == 'OGI':
            
            OGI_times = []
            for site in self.state['sites']:
                OGI_times.append(float(site['OGI_time']))
            OGI_mean_time = np.mean(OGI_times)

            OGI_surveys = []
            for site in self.state['sites']:
                OGI_surveys.append(float(site['OGI_required_surveys']))
            OGI_mean_required_surveys = np.mean(OGI_surveys)

            OGI_dict = {
                    # New OGI inputs
                    'OGI_n_crews': self.SA_params['OGI_n_crews'],
                    'OGI_min_temp': self.SA_params['OGI_min_temp'],
                    'OGI_max_wind': self.SA_params['OGI_max_wind'],
                    'OGI_max_precip': self.SA_params['OGI_max_precip'],
                    'OGI_min_interval': self.SA_params['OGI_min_interval'],
                    'OGI_reporting_delay': self.SA_params['OGI_reporting_delay'],
                    'OGI_MDL': self.SA_params['OGI_MDL'],
                    'OGI_mean_time': OGI_mean_time,
                    'OGI_mean_required_surveys': OGI_mean_required_surveys,        
                    
                    # New OGI outputs
                    'OGI_cum_program_cost': np.sum(np.array(self.timeseries['OGI_cost'][self.parameters['spin_up']:])),
                    'OGI_mean_prop_sites_avail': np.mean(np.array(self.timeseries['OGI_prop_sites_avail'][self.parameters['spin_up']:])),      
                    'OGI_cum_missed_leaks': np.sum(pd.DataFrame(self.state['sites'])['OGI_missed_leaks']),
                    'OGI_cum_surveys': np.sum(pd.DataFrame(self.state['sites'])['OGI_surveys_conducted'])
                    }
            
            df_dict.update(OGI_dict)
            self.export_SA(df_dict, self.output_directory, 'sensitivity_OGI.csv')

        # If this is a screening (aircraft) program, add relevant variables to dictionary before exporting
        if self.parameters['sensitivity']['program'] == 'aircraft':

            OGI_FU_times = []
            aircraft_times = []
            for site in self.state['sites']:
                OGI_FU_times.append(float(site['OGI_FU_time']))
                aircraft_times.append(float(site['aircraft_time']))
            OGI_FU_mean_time = np.mean(OGI_FU_times)
            aircraft_mean_time = np.mean(aircraft_times)

            aircraft_surveys = []
            for site in self.state['sites']:
                aircraft_surveys.append(float(site['aircraft_required_surveys']))
            aircraft_mean_required_surveys = np.mean(aircraft_surveys)

            aircraft_dict = {
                    # New OGI_FU inputs
                    'OGI_FU_n_crews': [self.SA_params['OGI_n_crews']],
                    'OGI_FU_min_temp': [self.SA_params['OGI_min_temp']],
                    'OGI_FU_max_wind': [self.SA_params['OGI_max_wind']],
                    'OGI_FU_max_precip': [self.SA_params['OGI_max_precip']],
                    'OGI_FU_min_interval': [self.SA_params['OGI_min_interval']],
                    'OGI_FU_reporting_delay': [self.SA_params['OGI_reporting_delay']],
                    'OGI_FU_MDL': [self.SA_params['OGI_MDL'][0]],
                    'OGI_FU_mean_time': OGI_FU_mean_time,
                    
                    # New aircraft inputs
                    'aircraft_n_crews': [self.SA_params['aircraft_n_crews']],
                    'aircraft_min_temp': [self.SA_params['aircraft_min_temp']],
                    'aircraft_max_wind': [self.SA_params['aircraft_max_wind']],
                    'aircraft_max_precip': [self.SA_params['aircraft_max_precip']],
                    'aircraft_min_interval': [self.SA_params['aircraft_min_interval']],
                    'aircraft_reporting_delay': [self.SA_params['aircraft_reporting_delay']],
                    'aircraft_MDL': [self.SA_params['aircraft_MDL']],
                    'aircraft_mean_time': aircraft_mean_time,
                    'aircraft_mean_required_surveys': aircraft_mean_required_surveys,
                    
                    # New OGI_FU outputs
                    'OGI_FU_cum_program_cost': np.sum(np.array(self.timeseries['OGI_FU_cost'][self.parameters['spin_up']:])),
                    'OGI_FU_mean_prop_sites_avail': np.mean(np.array(self.timeseries['OGI_FU_prop_sites_avail'][self.parameters['spin_up']:])),      
                    'OGI_FU_cum_missed_leaks': np.sum(pd.DataFrame(self.state['sites'])['OGI_FU_missed_leaks']),
                    'OGI_FU_cum_surveys': np.sum(pd.DataFrame(self.state['sites'])['OGI_FU_surveys_conducted']),
                    
                    # New aircraft outputs
                    'aircraft_cum_program_cost': np.sum(np.array(self.timeseries['aircraft_cost'][self.parameters['spin_up']:])),
                    'aircraft_mean_prop_sites_avail': np.mean(np.array(self.timeseries['aircraft_prop_sites_avail'][self.parameters['spin_up']:])),      
                    'aircraft_cum_missed_leaks': np.sum(pd.DataFrame(self.state['sites'])['aircraft_missed_leaks']),
                    'aircraft_cum_surveys': np.sum(pd.DataFrame(self.state['sites'])['aircraft_surveys_conducted'])                    
                    }
            
            df_dict.update(aircraft_dict)
            self.export_SA(df_dict, self.output_directory, 'sensitivity_aircraft.csv')
                                                                                                    
        return
        

        
    def adjust_distribution (self, distribution, outliers, samples):
        if outliers < 0:
            for i in range(abs(outliers)):
                distribution = np.delete(distribution, np.where(distribution == max(distribution)))
        if outliers > 0:
            for i in range(outliers):
                new_value = max(distribution) * 2
                distribution = np.append(distribution, new_value)
        while samples < 10:
            samples = int(np.random.normal(len(distribution), len(distribution)/4))                    
        distribution = np.random.choice(distribution, samples)        
        return


    
    def export_SA (self, dictionary, output_directory, name):
        df_new = pd.DataFrame([dictionary])              
        output_file = os.path.join(output_directory, name)            
        if not os.path.exists(output_file):
            df_new.to_csv(output_file, index = False)                
        elif os.path.exists(output_file):
            df_old = pd.read_csv(output_file)
            df_old = df_old.append(df_new)
            df_old.to_csv(output_file, index = False)        
        return

