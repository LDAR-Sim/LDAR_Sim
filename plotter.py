#------------------------------------------------------------------------------
# Name:        Plotter
# Purpose:     Generic standard plotting outputs for each run of model
#
# Authors:     Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:     22-04-2019

#------------------------------------------------------------------------------
from plotnine import *
import numpy as np
import warnings
from mizani.formatters import date_format

def make_plots(leak_df, time_df, site_df, sim_n, spin_up, output_directory):
    """
    This function makes a set of standard plots to output at end of simulation.
    """
    # Temporarily mute warnings
    warnings.filterwarnings('ignore')
    theme_set(theme_linedraw())
    
    # Chop off spin-up year (only for plots, still exists in raw output)
    time_df_adj = time_df.iloc[spin_up:,]

    # Timeseries plots
    plot_time_1 = (ggplot(time_df_adj, aes('datetime', 'daily_emissions_kg')) +
      geom_line(size = 2) + 
      ggtitle('Daily emissions from all sites (kg)') +
      ylab('') +
      xlab('') + 
      scale_x_datetime(labels = date_format('%Y')) +
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))) 
    
    plot_time_1.save(output_directory + '/plot_time_emissions_' + sim_n + '.png', width=10, height=3, dpi=300)    
    
    plot_time_2 = (ggplot(time_df_adj, aes('datetime', 'active_leaks')) +
      geom_line(size = 2) + 
      ggtitle('Number of active leaks at all sites') +
      ylab('') +
      xlab('') + 
      scale_x_datetime(labels = date_format('%Y')) +
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5))) 
    
    plot_time_2.save(output_directory + '/plot_time_active_' + sim_n + '.png', width = 10, height = 3, dpi = 300)        
    
    # Site-level plots
    plot_site_1 = (ggplot(site_df, aes('cum_frac_sites', 'cum_frac_emissions')) +
      geom_line(size = 2) + 
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5)) +
      xlab('Cumulative fraction of sites') +
      ylab('Cumulative fraction of emissions') +
      ggtitle('Empirical cumulative distribution of site-level emissions'))
    
    plot_site_1.save(output_directory + '/site_cum_dist_' + sim_n + '.png', width = 5, height = 4, dpi = 300)
  
    # Leak plots    
    plot_leak_1 = (ggplot(leak_df, aes('days_active')) + geom_histogram(colour = 'gray') +
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5)) +
      ggtitle('Distribution of leak duration') +
      xlab('Number of days the leak was active') + ylab('Count'))
    plot_leak_1.save(output_directory + '/leak_active_hist' + sim_n + '.png', width = 5, height = 4, dpi = 300)

    plot_leak_2 = (ggplot(leak_df, aes('cum_frac_leaks', 'cum_frac_rate', colour = 'status')) +
      geom_line(size = 2) + 
      scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5)) +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative leak rate fraction') +
      ggtitle('Fractional cumulative distribution'))
   
    plot_leak_2.save(output_directory + '/leak_cum_dist1_' + sim_n + '.png', width = 4, height = 4, dpi = 300)
        
    plot_leak_3 = (ggplot(leak_df, aes('cum_frac_leaks', 'cum_rate', colour = 'status')) +
      geom_line(size = 2) + 
      scale_colour_hue(h = 0.15, l = 0.25, s = 0.9) +
        theme(panel_border = element_rect(colour = "black", fill = None, size = 2), 
        panel_grid_minor_x = element_blank(), panel_grid_major_x = element_blank(),
        panel_grid_minor_y = element_line(colour = 'black', linewidth = 0.5, alpha = 0.3), 
        panel_grid_major_y = element_line(colour = 'black', linewidth = 1, alpha = 0.5)) +
      scale_y_continuous(trans='log10') +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative emissions (kg/day)') +
      ggtitle('Absolute cumulative distribution')) 
   
    plot_leak_3.save(output_directory + '/leak_cum_dist2_' + sim_n + '.png', width = 4, height = 4, dpi = 300)
  
    return



