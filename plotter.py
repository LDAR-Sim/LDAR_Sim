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

    # Following plots require playing with the data a bit    
    leaks_active = leak_df[leak_df.status == 'active'].sort_values('rate', ascending = False)
    leaks_repaired = leak_df[leak_df.status == 'repaired'].sort_values('rate', ascending = False)
    
    leaks_active['cum_frac_leaks'] = list(np.arange(0, 1, 1/len(leaks_active)))
    leaks_active['cum_rate'] = np.cumsum(leaks_active['rate'])
    leaks_active['cum_frac_rate'] = leaks_active['cum_rate']/max(leaks_active['cum_rate'])
    
    leaks_repaired['cum_frac_leaks'] = list(np.linspace(0, 1, len(leaks_repaired)))
    leaks_repaired['cum_rate'] = np.cumsum(leaks_repaired['rate'])
    leaks_repaired['cum_frac_rate'] = leaks_repaired['cum_rate']/max(leaks_repaired['cum_rate'])

    leaks_df_2 = leaks_active.append(leaks_repaired)
    
    plot_leak_2 = (ggplot(leaks_df_2, aes('cum_frac_leaks', 'cum_frac_rate', colour = 'status')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1),
            legend_position = (0.7, 0.3),
            legend_title = element_blank()) +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative leak rate fraction') +
      ggtitle('Fractional cumulative distribution'))
   
    plot_leak_2.save(filename = 'plot_leak_2.png', width = 4, height = 4, dpi = 300)
        
    plot_leak_3 = (ggplot(leaks_df_2, aes('cum_frac_leaks', 'cum_rate', colour = 'status')) +
      geom_line(size = 2) + theme_xkcd() +
      theme(panel_border = element_rect(colour = "black", fill = None, size=1),
            legend_position = (0.6, 0.6),
            legend_direction = 'horizontal',
            legend_title = element_blank()) +
      scale_y_continuous(trans='log10') +
      xlab('Cumulative fraction of leak sources') +
      ylab('Cumulative emissions (kg/day)') +
      ggtitle('Absolute cumulative distribution')) 
   
    plot_leak_3.save(filename = 'plot_leak_3.png', width = 4, height = 4, dpi = 300)
  
    return


