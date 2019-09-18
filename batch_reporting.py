#------------------------------------------------------------------------------
# Name:        Batch reporting
# Purpose:     Creates outputs across multiple programs and simulations
#
# Authors:     Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:     17-09-2019

#------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import math
import os
from datetime import datetime
from datetime import timedelta
from mizani.formatters import date_format
from plotnine import *


class batch_reporting:
    
    def __init__(self, output_directory, start_year, spin_up, ref_program):
        '''
        Prepare output csv files to glean summary statistics and plotting data.
        '''
        self.output_directory = output_directory
        self.start_year = start_year
        self.spin_up = spin_up
        self.ref_program = ref_program
        
        start_date = datetime(self.start_year, 1, 1) + timedelta(days = self.spin_up)
        start_date = start_date.strftime("%m-%d-%Y")  
        
        # Go to directory with program folders
        os.chdir(self.output_directory)
        
        # For each folder, build a dataframe combining all necessary files
        self.directories = next(os.walk('.'))[1]
        file_lists = [[] for i in range(len(self.directories))]
        
        # List files
        for i in range(len(self.directories)):
            path = self.output_directory + self.directories[i]
            for j in os.listdir(path):
                if os.path.isfile(os.path.join(path,j)) and 'timeseries' in j:
                    file_lists[i].append(j)
                    
        # Delete any empty lists (to enable additional folders, e.g. for sensitivity analysis)
        file_lists = [item for item in file_lists if len(item) > 0]
                
        # Read csv files to lists
        all_data = [[] for i in range(len(file_lists))]
        for i in range(len(file_lists)):
            for file in file_lists[i]:
                path = self.output_directory + self.directories[i] + '/' + file
                all_data[i].append(pd.read_csv(path))
                
        # Get vector of dates
        dates = pd.read_csv(self.output_directory + self.directories[0] + '/' + file_lists[0][0])['datetime']
        dates = pd.to_datetime(dates)
        
        mask = (dates > start_date)
        self.dates_trunc = dates.loc[mask]        

############## Build list of emissions dataframes #############################
        self.emission_dfs = [[] for i in range(len(all_data))]
        for i in range(len(all_data)):
            for j in all_data[i]:
                self.emission_dfs[i].append(j["daily_emissions_kg"])
            self.emission_dfs[i] = pd.concat(self.emission_dfs[i], axis = 1, keys = [i for i in range(len(all_data[i]))]) 
            
            # New columns
            self.emission_dfs[i]['program'] = self.directories[i]
            
        # Add dates
        for i in range(len(self.emission_dfs)):        
            self.emission_dfs[i] = pd.concat([self.emission_dfs[i], dates], axis = 1)

            # Axe spinup year
            self.emission_dfs[i]['datetime'] = pd.to_datetime(self.emission_dfs[i]['datetime'])
            mask = (self.emission_dfs[i]['datetime'] > start_date)
            self.emission_dfs[i] = self.emission_dfs[i].loc[mask]
                  
############# Build list of active leak dataframes ############################
        self.active_leak_dfs = [[] for i in range(len(all_data))]
        for i in range(len(all_data)):
            for j in all_data[i]:
                self.active_leak_dfs[i].append(j["active_leaks"])
            self.active_leak_dfs[i] = pd.concat(self.active_leak_dfs[i], axis = 1, keys = [i for i in range(len(all_data[i]))])
            
            # New columns
            self.active_leak_dfs[i]['program'] = self.directories[i]
        
        # Add dates
        for i in range(len(self.active_leak_dfs)):        
            self.active_leak_dfs[i] = pd.concat([self.active_leak_dfs[i], dates], axis = 1)

            # Axe spinup year
            self.active_leak_dfs[i]['datetime'] = pd.to_datetime(self.active_leak_dfs[i]['datetime'])
            mask = (self.active_leak_dfs[i]['datetime'] > start_date)
            self.active_leak_dfs[i] = self.active_leak_dfs[i].loc[mask]
            
################ Build list of repaired leak dataframes #######################
        self.repair_leak_dfs = [[] for i in range(len(all_data))]
        for i in range(len(all_data)):
            for j in all_data[i]:
                self.repair_leak_dfs[i].append(j["cum_repaired_leaks"])
            self.repair_leak_dfs[i] = pd.concat(self.repair_leak_dfs[i], axis = 1, keys = [i for i in range(len(all_data[i]))]) 
                        
            # New columns
            self.repair_leak_dfs[i]['program'] = self.directories[i]        
        
        # Add dates
        for i in range(len(self.repair_leak_dfs)):        
            self.repair_leak_dfs[i] = pd.concat([self.repair_leak_dfs[i], dates], axis = 1)

            # Axe spinup year
            self.repair_leak_dfs[i]['datetime'] = pd.to_datetime(self.repair_leak_dfs[i]['datetime'])    
            mask = (self.repair_leak_dfs[i]['datetime'] > start_date)
            self.repair_leak_dfs[i] = self.repair_leak_dfs[i].loc[mask]

        return

    def program_report(self):
        '''
        Output a spreadsheet for each program with descriptive statistics.
        '''        
        for i in range(len(self.active_leak_dfs)):
            data = [
                    {'mean': self.active_leak_dfs[i].describe().loc['50%'].mean(),
                     'median': self.active_leak_dfs[i].describe().loc['50%'].median(),
                     'std': self.active_leak_dfs[i].describe().loc['50%'].std(),
                     'min': self.active_leak_dfs[i].describe().loc['50%'].min(),
                     'max': self.active_leak_dfs[i].describe().loc['50%'].max()},
                    {'mean': self.emission_dfs[i].describe().loc['50%'].mean(),
                     'median': self.emission_dfs[i].describe().loc['50%'].median(),
                     'std': self.emission_dfs[i].describe().loc['50%'].std(),
                     'min': self.emission_dfs[i].describe().loc['50%'].min(),
                     'max': self.emission_dfs[i].describe().loc['50%'].max()},
                    {'mean': self.repair_leak_dfs[i].describe().loc['50%'].mean(),
                     'median': self.repair_leak_dfs[i].describe().loc['50%'].median(),
                     'std': self.repair_leak_dfs[i].describe().loc['50%'].std(),
                     'min': self.repair_leak_dfs[i].describe().loc['50%'].min(),
                     'max': self.repair_leak_dfs[i].describe().loc['50%'].max()}
                    ]            
            output_df = pd.DataFrame(data)
            output_df.rename(index={0:'median active leaks', 1:'median daily emissions', 2: 'cumulative repaired leaks'}, inplace=True)
            output_df.to_csv(self.output_directory + self.active_leak_dfs[i]['program'].iloc[0] + '_descriptives.csv', index = True)
            
                        
        return
    
   
    def batch_report(self):
        '''
        Output a spreadsheet comparing programs.
        '''                
        # Read in all the descriptive files
        descriptive_files = {}
        for i in os.listdir():
            if i.endswith('_descriptives.csv'):
                descriptive_files[i[:-17]] = pd.read_csv(i, index_col = 0)
        
        # Separate the reference program and the programs to compare to it
        ref = None
        alts = {}
        for i in descriptive_files:
            if i == self.ref_program:
                ref = descriptive_files[i]
            else:
                alts[i] = descriptive_files[i]
            
        output_df = pd.DataFrame()
        
        for i in alts:
            dif = alts[i] - ref
            dif['alt program'] = i
            dif['reference'] = self.ref_program
            dif['comparison'] = 'difference (alt-ref)'
            
            rat = alts[i] / ref
            rat['alt program'] = i
            rat['reference'] = self.ref_program
            rat['comparison'] = 'ratio (alt/ref)'     
            
            output_df = output_df.append([dif, rat])
        
        output_df.to_csv(self.output_directory + 'program_comparisons.csv', index = True)       

        return
    

    def batch_plots(self):
        
        dfs = self.emission_dfs
        
        for i in range(len(dfs)):
            n_cols = dfs[i].shape[1]
            dfs[i]['mean'] = dfs[i].iloc[:,0:n_cols].mean(axis = 1)
            dfs[i]['std'] = dfs[i].iloc[:,0:n_cols].std(axis = 1)
            dfs[i]['low'] = dfs[i].iloc[:,0:n_cols].quantile(0.025, axis=1)
            dfs[i]['high'] = dfs[i].iloc[:,0:n_cols].quantile(0.975, axis=1)
            dfs[i]['program'] = self.directories[i] 
        
        # Move reference program to the top of the list
        for i, df in enumerate(dfs):
            if df['program'].iloc[0] == self.ref_program:
                dfs.insert(0, dfs.pop(i))

        # Arrange dfs for plot 1
        dfs_p1 = dfs.copy()
        for i in range(len(dfs_p1)):                 
            # Reshape
            dfs_p1[i] = pd.melt(dfs_p1[i], id_vars = ['datetime', 'mean', 'std', 'low', 'high', 'program'])
       
        # Combine dataframes into single dataframe for plotting
        df_p1 = dfs_p1[0]
        for i in dfs_p1[1:]:
            df_p1 = df_p1.append(i, ignore_index = True)
    
        # Find values to set plot scale min and max
        min_mean = df_p1['mean'].min()
        max_mean = df_p1['mean'].max()
        exp_min = math.floor(math.log10(min_mean))
        exp_max = math.ceil(math.log10(max_mean))
        y_min = 10**exp_min
        y_max = 10**exp_max
        
        # Make plots from list of dataframes - one entry per dataframe
        theme_set(theme_linedraw())
        plot1 = (ggplot(None) + aes('datetime', 'value', group = 'program') +
                geom_ribbon(df_p1, aes(ymin = 'low', ymax = 'high', fill = 'program'), alpha = 0.2) +
                geom_line(df_p1, aes('datetime', 'mean', colour = 'program'), size = 1) +
                ylab('Daily emissions (kg)') + xlab('') +
                scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
                scale_x_datetime(labels = date_format('%Y')) +
                scale_y_continuous(trans = 'log10') +
                coord_cartesian(ylim = (y_min, y_max)) +
                labs(color = 'Program', fill = 'Program') +
                theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
                panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
                panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
                panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))
            )                         
        plot1.save(self.output_directory + 'program_comparison.png', width = 7, height = 3, dpi = 900)
        
        
        # Build relative mitigation plots
        dfs_p2 = dfs.copy()  
            
        for i in dfs_p2[1:]:
            i['mean_dif'] = 0
            i['std_dif'] = 0
            i['mean_ratio'] = 0
            i['std_ratio'] = 0
            for j in range(len(i)):
                ref_mean = dfs_p2[0].loc[dfs_p2[0].index[j], 'mean']
                ref_std = dfs_p2[0].loc[dfs_p2[0].index[j], 'std']
                alt_mean = i.loc[i.index[j], 'mean']
                alt_std = i.loc[i.index[j], 'std']
                difs = []
                ratios = []
                
                for k in range(100):
                    ref = np.random.normal(loc = ref_mean, scale = ref_std)
                    alt = np.random.normal(loc = alt_mean, scale = alt_std)
                    dif = alt - ref
                    ratio = alt/ref
                    difs.append(dif)
                    ratios.append(ratio)
                    
                i.loc[i.index[j], 'mean_dif'] = np.mean(difs)
                i.loc[i.index[j], 'std_dif'] = np.std(difs)
                i.loc[i.index[j], 'mean_ratio'] = np.mean(ratios)
                i.loc[i.index[j], 'std_ratio'] = np.std(ratios)
                        
        # Build plotting dataframe
        df_p2 = self.dates_trunc.copy().to_frame()
        df_p2['program'] = dfs_p2[1]['program']
        df_p2['mean_dif'] = dfs_p2[1]['mean_dif']
        df_p2['std_dif'] = dfs_p2[1]['std_dif']
        df_p2['mean_ratio'] = dfs_p2[1]['mean_ratio']
        df_p2['std_ratio'] = dfs_p2[1]['std_ratio']
        
        df_p2['low_dif'] = dfs_p2[1]['mean_dif'] - 2*dfs_p2[1]['std_dif']
        df_p2['high_dif'] = dfs_p2[1]['mean_dif'] + 2*dfs_p2[1]['std_dif']
        df_p2['low_ratio'] = dfs_p2[1]['mean_ratio'] - 2*dfs_p2[1]['std_ratio']
        df_p2['high_ratio'] = dfs_p2[1]['mean_ratio'] + 2*dfs_p2[1]['std_ratio']
        
        pd.options.mode.chained_assignment = None
        for i in dfs_p2[2:]:
            i['low_dif'] = i['mean_dif'] - 2*i['std_dif']
            i['high_dif'] = i['mean_dif'] + 2*i['std_dif']
            i['low_ratio'] = i['mean_ratio'] - 2*i['std_ratio']
            i['high_ratio'] = i['mean_ratio'] + 2*i['std_ratio']
            short_df = i[['program','mean_dif', 'std_dif', 'low_dif', 'high_dif', 'mean_ratio', 'std_ratio', 'low_ratio', 'high_ratio']]
            short_df['datetime'] = np.array(self.dates_trunc)
            df_p2 = df_p2.append(short_df, ignore_index = True)
                    
        # Make plot 2    
        plot2 = (ggplot(None) + aes('datetime', 'mean_dif', group = 'program') +
            geom_ribbon(df_p2, aes(ymin = 'low_dif', ymax = 'high_dif', fill = 'program'), alpha = 0.2) +
            geom_line(df_p2, aes('datetime', 'mean_dif', colour = 'program'), size = 1) +
            ylab('Daily emissions difference (kg)') + xlab('') +
            scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
            scale_x_datetime(labels = date_format('%Y')) +
            ggtitle('Differences of individual days may be unstable for small sample sizes. \nBetter to take ratio of mean daily emissions over entire timeseries.') +
    #        scale_y_continuous(trans='log10') +  
            labs(color = 'Program', fill = 'Program') +
            theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
            panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
            panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
            panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))
        )                         
        plot2.save(self.output_directory + 'relative_mitigation.png', width = 7, height = 3, dpi = 900)    
            
    
        y_min = 0
        y_max = 3      
        # Make plot 3    
        plot3 = (ggplot(None) + aes('datetime', 'mean_ratio', group = 'program') +
            geom_ribbon(df_p2, aes(ymin = 'low_ratio', ymax = 'high_ratio', fill = 'program'), alpha = 0.2) +
            geom_line(df_p2, aes('datetime', 'mean_ratio', colour = 'program'), size = 1) +
            geom_hline(yintercept = 1, size = 0.5, colour = 'blue') +
            ylab('Daily emissions ratio (kg)') + xlab('') +
            scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
            scale_x_datetime(labels = date_format('%Y')) +
            ggtitle('Ratios of individual days may be unstable for small sample sizes. \nIf unstable, need more simulations (or more sites). \nLook also at ratio of mean daily emissions over entire timeseries.') +
            coord_cartesian(ylim = (y_min, y_max)) +
    #        scale_y_continuous(trans='log10') +  
            labs(color = 'Program', fill = 'Program') +
            theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
            panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
            panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
            panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))
        )                         
        plot3.save(self.output_directory + 'relative_mitigation2.png', width = 7, height = 3, dpi = 900)           
                    
        return
    
    
    
    
    
    
    
    