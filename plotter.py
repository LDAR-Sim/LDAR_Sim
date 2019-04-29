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

def make_plots(leak_df, time_df, site_df, sim_n):
    """
    This function makes a set of standard plots to output at end of simulation.
    """
    # Temporarily mute warnings
    warnings.filterwarnings('ignore')
    
    # Chop off spin-up year (only for plots, still exists in raw output)
    time_df_adj = time_df.iloc[365:,]

    # Timeseries plots
    plot_time_1 = (ggplot(time_df_adj, aes('datetime', 'daily_emissions_kg')) +
      geom_line(size = 2) + theme_xkcd() +
      ggtitle('Daily emissions from all sites (kg)') +
      ylab('') +
      xlab('') + 
      theme(panel_border = element_rect(colour = "black", fill = None, size = 1),
            axis_text_x = element_text(angle = 90))) 
    
    plot_time_1.save('plot_time_emissions_' + sim_n + '.png', width=10, height=3, dpi=300)    
    
    plot_time_2 = (ggplot(time_df_adj, aes('datetime', 'active_leaks')) +
      geom_line(size = 2) + theme_xkcd() +
      ggtitle('Number of active leaks at all sites') +
      ylab('') +
      xlab('') + 
      theme(panel_border = element_rect(colour = "black", fill = None, size = 1),
            axis_text_x = element_text(angle = 90))) 
    
    plot_time_2.save('plot_time_active_' + sim_n + '.png', width = 10, height = 3, dpi = 300)        
    
    # Site-level plots
    plot_site_1 = (ggplot(site_df, aes('cum_frac_sites', 'cum_frac_emissions')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1)) +
      xlab('Cumulative fraction of sites') +
      ylab('Cumulative fraction of emissions') +
      ggtitle('Empirical cumulative distribution of site-level emissions'))
    
    plot_site_1.save(filename = 'site_cum_dist_' + sim_n + '.png', width = 10, height = 3, dpi = 300)
  
    # Leak plots    
    plot_leak_1 = (ggplot(leak_df, aes('days_active')) + geom_histogram(colour = 'gray') +
      theme_xkcd() + 
      theme(panel_border = element_rect(colour = "black", fill = None, size = 1)) +
      ggtitle('Distribution of leak duration') +
      xlab('Number of days the leak was active') + ylab('Count'))
    plot_leak_1.save(filename = 'leak_active_hist' + sim_n + '.png', width = 5, height = 4, dpi = 300)

    plot_leak_2 = (ggplot(leak_df, aes('cum_frac_leaks', 'cum_frac_rate', colour = 'status')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1),
            legend_position = (0.7, 0.3),
            legend_title = element_blank()) +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative leak rate fraction') +
      ggtitle('Fractional cumulative distribution'))
   
    plot_leak_2.save(filename = 'leak_cum_dist1_' + sim_n + '.png', width = 4, height = 4, dpi = 300)
        
    plot_leak_3 = (ggplot(leak_df, aes('cum_frac_leaks', 'cum_rate', colour = 'status')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1),
            legend_position = (0.6, 0.6),
            legend_direction = 'horizontal',
            legend_title = element_blank()) +
      scale_y_continuous(trans='log10') +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative emissions (kg/day)') +
      ggtitle('Absolute cumulative distribution')) 
   
    plot_leak_3.save(filename = 'leak_cum_dist2_' + sim_n + '.png', width = 4, height = 4, dpi = 300)
  
    return



