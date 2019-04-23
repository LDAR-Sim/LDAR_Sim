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

def make_plots(leak_df, time_df, site_df):
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
    
    plot_time_1.save("plot_time_1.png", width=10, height=3, dpi=300)    
    
    plot_time_2 = (ggplot(time_df_adj, aes('datetime', 'active_leaks')) +
      geom_line(size = 2) + theme_xkcd() +
      ggtitle('Number of active leaks at all sites') +
      ylab('') +
      xlab('') + 
      theme(panel_border = element_rect(colour = "black", fill = None, size = 1),
            axis_text_x = element_text(angle = 90))) 
    
    plot_time_2.save("plot_time_2.png", width = 10, height = 3, dpi = 300)        
    
    # Site-level plots
    site_df['x'] = list(site_df.index)
    site_df['x'] = site_df['x']/max(site_df['x'])
    site_df['y'] = np.cumsum(sorted(site_df['total_emissions_kg'], reverse = True))
    site_df['y'] = site_df['y']/max(site_df['y'])
    
    plot_site_1 = (ggplot(site_df, aes('x', 'y')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1)) +
      xlab('Cumulative fraction of sites') +
      ylab('Cumulative fraction of emissions') +
      ggtitle('Empirical cumulative distribution of site-level emissions'))
    
    plot_site_1.save(filename = 'plot_site_1.png', width = 10, height = 3, dpi = 300)
  
    # Leak plots    
    plot_leak_1 = (ggplot(leak_df, aes('days_active')) + geom_histogram(colour = 'gray') +
      theme_xkcd() + 
      theme(panel_border = element_rect(colour = "black", fill = None, size = 1)) +
      ggtitle('Distribution of leak duration') +
      xlab('Number of days the leak was active') + ylab('Count'))
    plot_leak_1.save(filename = 'plot_leak_1.png', width = 5, height = 4, dpi = 300)

    # Final plot requires playing with the data a bit    
    leaks_active = leak_df[leak_df.status == 'active']
    leaks_repaired = leak_df[leak_df.status == 'repaired']

    leaks_active['x'] = list(leaks_active.index)
    leaks_active['x'] = leaks_active['x']/max(leaks_active['x'])
    leaks_active['y'] = np.cumsum(sorted(leaks_active['rate'], reverse = True))
    leaks_active['y'] = leaks_active['y']/max(leaks_active['y'])
    
    leaks_repaired['x'] = list(leaks_repaired.index)
    leaks_repaired['x'] = leaks_repaired['x']/max(leaks_repaired['x'])
    leaks_repaired['y'] = np.cumsum(sorted(leaks_repaired['rate'], reverse = True))
    leaks_repaired['y'] = leaks_repaired['y']/max(leaks_repaired['y'])

    leaks_df_2 = leaks_active.append(leaks_repaired)
    
    plot_leak_2 = (ggplot(leaks_df_2, aes('x', 'y', colour = 'status')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1)) +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative leak rate fraction') +
      ggtitle('Empirical cumulative distributions of active and repaired leaks'))
    
    plot_leak_2.save(filename = 'plot_leak_2.png', width = 7, height = 3, dpi = 300)
  
    
    
    
    warnings.filterwarnings('default')
    return



