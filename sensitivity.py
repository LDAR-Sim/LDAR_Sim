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
                
            return

    def write_data (self):
        
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
            output_file = os.path.join(self.parameters['working_directory'], self.parameters['output_folder'], 'sensitivity_operator.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
                

            

            
            
            
            
            