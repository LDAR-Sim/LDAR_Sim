#------------------------------------------------------------------------------
# Name:        Plotter
# Purpose:     Generic standard plotting outputs for each run of model
#
# Authors:     Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:     27-05-2019

#------------------------------------------------------------------------------
from plotnine import *
import numpy as np
import warnings
import os
import pandas as pd
import csv
from mizani.breaks import date_breaks
from mizani.formatters import date_format
from datetime import datetime
from datetime import timedelta
from scipy import stats
import math


def batch_plots(output_directory, start_year, spin_up, ref_program):
    """
    This function makes equivalence plots comparing programs in batch mode.
    """
    
    # Go to directory with program folders
    os.chdir(output_directory)
    
    # For each folder, build a dataframe combining all necessary files
    num_lists = len(os.listdir())
    file_lists = [[] for i in range(num_lists)]
    
    # List files
    for i in range(len(os.listdir())):
        path = output_directory + os.listdir()[i]
        for j in os.listdir(path):
            if os.path.isfile(os.path.join(path,j)) and 'timeseries' in j:
                file_lists[i].append(j)
                
    # Read csv files to lists
    all_data = [[] for i in range(len(file_lists))]
    for i in range(len(file_lists)):
        for file in file_lists[i]:
            path = output_directory + os.listdir()[i] + '/' + file
            all_data[i].append(pd.read_csv(path))

    # Get vector of dates
    dates = pd.read_csv(output_directory + os.listdir()[0] + '/' + file_lists[0][0])['datetime']
    dates = pd.to_datetime(dates)
        
    # Extract emissions from each csv and combined into df; add dates & new cols
    dfs = [[] for i in range(len(all_data))]
    for i in range(len(all_data)):
        for j in all_data[i]:
            dfs[i].append(j["daily_emissions_kg"])
        dfs[i] = pd.concat(dfs[i], axis = 1, keys = [i for i in range(len(all_data[i]))]) 
        n_cols = dfs[i].shape[1]
        
        # New columns
        dfs[i]['mean'] = dfs[i].iloc[:,0:n_cols].mean(axis = 1)
        dfs[i]['std'] = dfs[i].iloc[:,0:n_cols].std(axis = 1)
#        dfs[i]['std_rol10'] = dfs[i]['std'].rolling(10, center = True).mean()
#        dfs[i]['low'] = dfs[i]['mean'] - 2*dfs[i]['std_rol10']
#        dfs[i]['high'] = dfs[i]['mean'] + 2*dfs[i]['std_rol10']               
#        dfs[i]['low'] = dfs[i]['mean'] - 2*dfs[i]['std']
#        dfs[i]['high'] = dfs[i]['mean'] + 2*dfs[i]['std']
        dfs[i]['low'] = dfs[i].iloc[:,0:n_cols].quantile(0.025, axis=1)
        dfs[i]['high'] = dfs[i].iloc[:,0:n_cols].quantile(0.975, axis=1)
        dfs[i]['program'] = os.listdir()[i]
        
    # Move reference program to the top of the list
    for i, df in enumerate(dfs):
        if df['program'][0] == ref_program:
            dfs.insert(0, dfs.pop(i))
              
    # Arrange dfs for plot 1
    dfs_p1 = dfs.copy()
    for i in range(len(dfs_p1)):        
        # Add the date
        dfs_p1[i] = pd.concat([dfs_p1[i], dates], axis = 1)
        
        # Reshape
        dfs_p1[i] = pd.melt(dfs_p1[i], id_vars = ['datetime', 'mean', 'low', 'high', 'program'])
   
    # Combine dataframes into single dataframe for plotting
    df_p1 = dfs_p1[0]
    for i in dfs_p1[1:]:
        df_p1 = df_p1.append(i, ignore_index = True)

    # Axe spinup year
    df_p1['datetime'] = pd.to_datetime(df_p1['datetime'])
    start_date = datetime(start_year, 1, 1) + timedelta(days = spin_up)
    start_date = start_date.strftime("%m-%d-%Y")    
    mask = (df_p1['datetime'] > start_date)
    df_p1 = df_p1.loc[mask]
    
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
    plot1.save(output_directory + 'program_comparison.png', width = 7, height = 3, dpi = 900)
    
    
    # Build relative mitigation plot
    dfs_p2 = dfs.copy()  
        
    for i in dfs_p2[1:]:
        i['mean_dif'] = 0
        i['std_dif'] = 0
        for j in range(len(i)):
            ref_mean = dfs_p2[0].loc[dfs_p2[0].index[j], 'mean']
            ref_std = dfs_p2[0].loc[dfs_p2[0].index[j], 'std']
            alt_mean = i.loc[i.index[j], 'mean']
            alt_std = i.loc[i.index[j], 'std']
            difs = []
            
            for k in range(100):
                ref = np.random.normal(loc = ref_mean, scale = ref_std)
                alt = np.random.normal(loc = alt_mean, scale = alt_std)
                dif = alt - ref
                difs.append(dif)
                
            i.loc[i.index[j], 'mean_dif'] = np.mean(difs)
            i.loc[i.index[j], 'std_dif'] = np.std(difs)
        
        
    # Build plotting dataframe
    df_p2 = dates.copy().to_frame()
    df_p2['program'] = dfs_p2[1]['program']
    df_p2['mean_dif'] = dfs_p2[1]['mean_dif']
    df_p2['std_dif'] = dfs_p2[1]['std_dif']
    
    df_p2['low'] = dfs_p2[1]['mean_dif'] - 2*dfs_p2[1]['std_dif']
    df_p2['high'] = dfs_p2[1]['mean_dif'] + 2*dfs_p2[1]['std_dif']
    
    pd.options.mode.chained_assignment = None
    for i in dfs_p2[2:]:
        i['low'] = i['mean_dif'] - 2*i['std_dif']
        i['high'] = i['mean_dif'] + 2*i['std_dif']
        short_df = i[['program','mean_dif', 'std_dif', 'low', 'high']]
        short_df['datetime'] = np.array(dates)
        df_p2 = df_p2.append(short_df, ignore_index = True)
        
    # Axe spinup year
    df_p2['datetime'] = pd.to_datetime(df_p2['datetime'])
    start_date = datetime(start_year, 1, 1) + timedelta(days = spin_up)
    start_date = start_date.strftime("%m-%d-%Y")
    mask = (df_p2['datetime'] > start_date)
    df_p2 = df_p2.loc[mask]
        
    
    # Make plot 2    
    plot2 = (ggplot(None) + aes('datetime', 'mean_dif', group = 'program') +
        geom_ribbon(df_p2, aes(ymin = 'low', ymax = 'high', fill = 'program'), alpha = 0.2) +
        geom_line(df_p2, aes('datetime', 'mean_dif', colour = 'program'), size = 1) +
        ylab('Daily emissions difference (kg)') + xlab('') +
        scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
        scale_x_datetime(labels = date_format('%Y')) +
#        scale_y_continuous(trans='log10') +  
        labs(color = 'Program', fill = 'Program') +
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))
    )                         
    plot2.save(output_directory + 'relative_mitigation.png', width = 7, height = 3, dpi = 900)    
        
        
        
        
        
        
        