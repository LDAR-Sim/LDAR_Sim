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

class sensitivity:
    def __init__ (self, parameters, timeseries, state):
        '''
        Initialize a sensitivity analysis.

        '''   
        self.parameters = parameters
        self.timeseries = timeseries
        self.state = state
        
        if self.parameters['sensitivity'][1] == 'operator':

            self.sens_params = {
            'LSD_shift': np.random.normal(0, 0.5),
            'LSD_stretch': np.random.normal(1, 0.2),
            'LSD_outliers': int(np.round(np.random.normal(0, 1))),
            
            'LCD_shift': int(np.round(np.random.normal(0, 2))),
            'LCD_stretch': np.random.normal(1, 0.2),
            'LCD_outliers': int(np.round(np.random.normal(0, 1))),
            
            'site_rate_shift': np.random.normal(0, 0.5),
            'site_rate_stretch': np.random.normal(1, 0.2),
            'site_rate_outliers': int(np.round(np.random.normal(0, 1))),
            
            'repair_delay': np.random.uniform(0, 100),
            'LPR': np.random.triangular(0.000133, 0.00133, 0.0133),
            'max_det_op': np.random.beta(1, 10)
            }  
            
            # Set scalar parameters
            self.parameters['LPR'] = self.sens_params['LPR']
            self.parameters['repair_delay'] = self.sens_params['repair_delay']
            self.parameters['max_det_op'] = self.sens_params['max_det_op']
            
            # Modify input distributions - leak rates
            self.state['empirical_leaks'] = (self.state['empirical_leaks'] + self.sens_params['LSD_shift']) * self.sens_params['LSD_stretch']
            if self.sens_params['LSD_outliers'] < 0:
                for i in range(abs(self.sens_params['LSD_outliers'])):
                    self.state['empirical_leaks'] = np.delete(self.state['empirical_leaks'], np.where(self.state['empirical_leaks'] == max(self.state['empirical_leaks'])))
                
            if self.sens_params['LSD_outliers'] > 0:
                for i in range(self.sens_params['LSD_outliers']):
                    new_value = max(self.state['empirical_leaks']) * 2
                    self.state['empirical_leaks'] = np.append(self.state['empirical_leaks'], new_value)
                        
            # Modify input distributions - leak counts
            self.state['empirical_counts'] = ((self.state['empirical_counts'] + self.sens_params['LCD_shift']) * self.sens_params['LCD_stretch']).astype(int)
            if self.sens_params['LCD_outliers'] < 0:
                for i in range(abs(self.sens_params['LCD_outliers'])):
                    self.state['empirical_counts'] = np.delete(self.state['empirical_counts'], np.where(self.state['empirical_counts'] == max(self.state['empirical_counts'])))
                
            if self.sens_params['LCD_outliers'] > 0:
                for i in range(self.sens_params['LCD_outliers']):
                    new_value = max(self.state['empirical_counts']) * 2
                    self.state['empirical_counts'] = np.append(self.state['empirical_counts'], new_value)
            
            # Modify input distributions - site emissions (for venting)
            if self.parameters['consider_venting'] == True:
                self.state['empirical_sites'] = (self.state['empirical_sites'] + self.sens_params['site_rate_shift']) * self.sens_params['site_rate_stretch']
                if self.sens_params['site_rate_outliers'] < 0:
                    for i in range(abs(self.sens_params['site_rate_outliers'])):
                        self.state['empirical_sites'] = np.delete(self.state['empirical_sites'], np.where(self.state['empirical_sites'] == max(self.state['empirical_sites'])))
                
                if self.sens_params['site_rate_outliers'] > 0:
                    for i in range(self.sens_params['site_rate_outliers']):
                        new_value = max(self.state['empirical_sites']) * 2
                        self.state['empirical_sites'] = np.append(self.state['empirical_sites'], new_value)
                      
        
        if self.parameters['sensitivity'][1] == 'OGI':
            self.sens_params = {
            'consider_daylight': bool(np.random.binomial(1, 0.5)),
            'n_crews': 1,
            'min_temp': 1,
            'max_wind': 1,
            'max_precip': 1,
            'min_interval': 1,
            'max_workday': 10,  
            'reporting_delay': 1,
            'OGI_time': 100,
            'OGI_required_surveys': 1 ,
            'MDL': [np.random.uniform(0, 2), 0.01]
            }     

            # Set scalar parameters
            self.parameters['consider_daylight'] = self.sens_params['consider_daylight']
            self.parameters['methods']['OGI']['min_temp'] = self.sens_params['min_temp']
            self.parameters['methods']['OGI']['max_wind'] = self.sens_params['max_wind']
            self.parameters['methods']['OGI']['max_precip'] = self.sens_params['max_precip']
            self.parameters['methods']['OGI']['min_interval'] = self.sens_params['min_interval']
            self.parameters['methods']['OGI']['max_workday'] = self.sens_params['max_workday']
            self.parameters['methods']['OGI']['reporting_delay'] = self.sens_params['reporting_delay']
            self.parameters['methods']['OGI']['MDL'] = self.sens_params['MDL']

            for site in self.state['sites']:
                site['OGI_time'] = self.sens_params['OGI_time']
                site['OGI_required_surveys'] = self.sens_params['OGI_required_surveys']

            return

    def write_data (self):
        
        # Make folder for sensitivity analysis outputs
        output_directory = os.path.join(self.parameters['working_directory'], self.parameters['master_output_folder'], 'sensitivity_analysis')
        if not os.path.exists(output_directory):
            os.makedirs(output_directory) 
        
        if self.parameters['sensitivity'][1] == 'operator':
            
            # Build output dataframe
            df_dict = {
                    # Sensitivity input variables here
                    'simulation': [self.parameters['simulation']],
                    'LSD_shift': [self.sens_params['LSD_shift']],
                    'LSD_stretch': [self.sens_params['LSD_stretch']],
                    'LSD_outliers': [self.sens_params['LSD_outliers']],
                    'LCD_shift': [self.sens_params['LCD_shift']],
                    'LCD_stretch': [self.sens_params['LCD_stretch']],
                    'LCD_outliers': [self.sens_params['LCD_outliers']],
                    'site_rate_shift': [self.sens_params['site_rate_shift']],
                    'site_rate_stretch': [self.sens_params['site_rate_stretch']],
                    'site_rate_outliers': [self.sens_params['site_rate_outliers']],
                    'repair_delay': [self.sens_params['repair_delay']],
                    'LPR': [self.sens_params['LPR']],
                    'max_det_op': [self.sens_params['max_det_op']],

                    # Output metrics here
                    'dail_site_em_mean': np.mean(np.array(self.timeseries['daily_emissions_kg'])/len(self.state['sites'])),
                    'dail_site_em_std': np.std(np.array(self.timeseries['daily_emissions_kg'])/len(self.state['sites'])),
                    }
            
            # Build a dataframe for export
            df_new = pd.DataFrame(df_dict)  
            
            # Set output file name
            output_file = os.path.join(output_directory, 'sensitivity_operator.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
                
                
        if self.parameters['sensitivity'][1] == 'reference':
            
            # Sensitivity input variables here
            OGI_times = []
            for site in self.state['sites']:
                OGI_times.append(float(site['OGI_time']))
            mean_OGI_time = np.mean(OGI_times)

            OGI_surveys = []
            for site in self.state['sites']:
                OGI_surveys.append(float(site['OGI_required_surveys']))
            mean_OGI_required_surveys = np.mean(OGI_surveys)
            
            df_dict = {
            'simulation': [self.parameters['simulation']],
            'consider_daylight': [self.parameters['consider_daylight']],
            'n_crews': [self.parameters['methods']['OGI']['n_crews']],
            'min_temp': [self.parameters['methods']['OGI']['min_temp']],
            'max_wind': [self.parameters['methods']['OGI']['max_wind']],
            'max_precip': [self.parameters['methods']['OGI']['max_precip']],
            'min_interval': [self.parameters['methods']['OGI']['min_interval']],
            'max_workday': [self.parameters['methods']['OGI']['max_workday']],  
            'reporting_delay': [self.parameters['methods']['OGI']['reporting_delay']],
            'MDL': [self.parameters['methods']['OGI']['MDL'][0]],
            'MDL_std': [self.parameters['methods']['OGI']['MDL'][1]],            
            'mean_OGI_time': [mean_OGI_time],
            'mean_OGI_required_surveys': [mean_OGI_required_surveys],
           
            # Output metrics here
            'dail_site_em_mean': np.mean(np.array(self.timeseries['daily_emissions_kg'])/len(self.state['sites'])),
            'dail_site_em_std': np.std(np.array(self.timeseries['daily_emissions_kg'])/len(self.state['sites']))
                }

            # Build a dataframe for export
            df_new = pd.DataFrame(df_dict)  
            
            # Set output file name
            output_file = os.path.join(output_directory, 'sensitivity_reference.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
                        
        
        if self.parameters['sensitivity'][1] == 'OGI':
            
            # Sensitivity input variables here
            OGI_times = []
            for site in self.state['sites']:
                OGI_times.append(float(site['OGI_time']))
            mean_OGI_time = np.mean(OGI_times)

            OGI_surveys = []
            for site in self.state['sites']:
                OGI_surveys.append(float(site['OGI_required_surveys']))
            mean_OGI_required_surveys = np.mean(OGI_surveys)

            df_dict = {
            'simulation': [self.parameters['simulation']],
            'consider_daylight': [self.sens_params['consider_daylight']],
            'n_crews': [self.sens_params['n_crews']],
            'min_temp': [self.sens_params['min_temp']],
            'max_wind': [self.sens_params['max_wind']],
            'max_precip': [self.sens_params['max_precip']],
            'min_interval': [self.sens_params['min_interval']],
            'max_workday': [self.sens_params['max_workday']],  
            'reporting_delay': [self.sens_params['reporting_delay']],
            'MDL': [self.sens_params['MDL'][0]],
            'MDL_std': [self.sens_params['MDL'][1]],
            'mean_OGI_time': mean_OGI_time,
            'mean_OGI_required_surveys': mean_OGI_required_surveys,
            
            # Output metrics here
            'dail_site_em_mean': np.mean(np.array(self.timeseries['daily_emissions_kg'])/len(self.state['sites'])),
            'dail_site_em_std': np.std(np.array(self.timeseries['daily_emissions_kg'])/len(self.state['sites']))
                }

            # Build a dataframe for export
            df_new = pd.DataFrame(df_dict)  
            
            # Set output file name
            output_file = os.path.join(output_directory, 'sensitivity_OGI.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
            
            
            # Finally, can load the two csv files we just exported and process into main results
            df_ref = pd.read_csv(os.path.join(output_directory, 'sensitivity_reference.csv'))
            df_OGI = pd.read_csv(os.path.join(output_directory, 'sensitivity_OGI.csv'))
            
            if len(df_ref) == len(df_OGI):
            
                # Build new dataframe
                df_combine = {
                'simulation': list(df_OGI['simulation']),
                'consider_daylight': list(df_OGI['consider_daylight']),
                'n_crews_dif': list(df_ref['n_crews'] - df_OGI['n_crews']),
                'min_temp_dif': list(df_ref['min_temp'] - df_OGI['min_temp']),
                'max_wind_dif': list(df_ref['max_wind'] - df_OGI['max_wind']),
                'max_precip_dif': list(df_ref['max_precip'] - df_OGI['max_precip']),
                'min_interval_dif': list(df_ref['min_interval'] - df_OGI['min_interval']),
                'max_workday_dif': list(df_ref['max_workday'] - df_OGI['max_workday']),  
                'reporting_delay_dif': list(df_ref['reporting_delay'] - df_OGI['reporting_delay']),
                'MDL_dif': list(df_ref['MDL'] - df_OGI['MDL']),
                'MDL_std_dif': list(df_ref['MDL_std'] - df_OGI['MDL_std']),
                'mean_OGI_time_dif': list(df_ref['mean_OGI_time'] - df_OGI['mean_OGI_time']),
                'mean_OGI_required_surveys_dif': list(df_ref['mean_OGI_required_surveys'] - df_OGI['mean_OGI_required_surveys']),
                
                'dail_site_em_mean_dif': list(df_ref['dail_site_em_mean'] - df_OGI['dail_site_em_mean']),
                'dail_site_em_std_dif': list(df_ref['dail_site_em_std'] - df_OGI['dail_site_em_std'])
                    }
    
                # Export
                df_new = pd.DataFrame(df_combine)            
                output_file = os.path.join(output_directory, 'comparison.csv')                        
                df_new.to_csv(output_file, index = False)                                                                                   

            return
            

            
            
            
            
            