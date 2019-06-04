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
from scipy import stats

def batch_plots(output_directory):
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
        
        # New columns: mean, 2.5% quantile, 97.5% quantile, program name
        dfs[i]['mean'] = dfs[i].mean(axis = 1)
        dfs[i]['low'] = dfs[i].quantile(0.05, axis=1)
        dfs[i]['high'] = dfs[i].quantile(0.95, axis=1)
        dfs[i]['program'] = os.listdir()[i]
        
        # Add the date
        dfs[i] = pd.concat([dfs[i], dates], axis = 1)
        
        # Reshape
        dfs[i] = pd.melt(dfs[i], id_vars = ['datetime', 'mean', 'low', 'high', 'program'])
   
    # Combine dataframes into single dataframe for plotting
    df = dfs[0]
    for i in dfs[1:]:
        df = df.append(i, ignore_index = True)
         
    # Make plots from list of dataframes - one entry per dataframe
    theme_set(theme_linedraw())
    plot1 = (ggplot(None) + aes('datetime', 'value', group = 'program') +
            geom_ribbon(df, aes(ymin = 'low', ymax = 'high', fill = 'program'), alpha = 0.2) +
            geom_line(df, aes('datetime', 'mean', colour = 'program'), size = 1) +
            ylab('Daily emissions (kg)') + xlab('') +
            scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
            scale_x_datetime(labels = date_format('%Y')) +
            scale_y_continuous(trans='log10') +  labs(color = 'Program', fill = 'Program') +
            theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
            panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
            panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
            panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))
        )                         
    plot1.save(output_directory + 'program_comparison.png', width = 7, height = 3, dpi = 900)

        
        
        