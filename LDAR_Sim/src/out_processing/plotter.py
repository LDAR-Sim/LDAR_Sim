# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Plotter
# Purpose:     Generate standard plots for each run of LDAR-Sim
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------
import warnings

import plotnine as pn
from mizani.formatters import date_format


def make_plots(leak_df, time_df, site_df, sim_n, output_directory):
    """
    This function makes a set of standard plots to output at end of simulation.
    """
    # Temporarily mute warnings
    warnings.filterwarnings('ignore')
    pn.theme_set(pn.theme_linedraw())

    # Timeseries plots
    plot_time_1 = (
        pn.ggplot(time_df, pn.aes('datetime', 'daily_emissions_kg')) +
        pn.geom_line(size=2) +
        pn.ggtitle('Daily emissions from all sites (kg)') +
        pn.ylab('') +
        pn.xlab('') +
        pn.scale_x_datetime(labels=date_format('%Y')) +
        pn.theme(
            panel_border=pn.element_rect(colour="black", fill=None, size=2),
            panel_grid_minor_x=pn.element_blank(),
            panel_grid_major_x=pn.element_blank(),
            panel_grid_minor_y=pn.element_line(colour='black', linewidth=0.5, alpha=0.3),
            panel_grid_major_y=pn.element_line(colour='black', linewidth=1, alpha=0.5))
    )

    plot_time_1.save(output_directory / 'plot_time_emissions_{}.png'.format(sim_n),
                     width=10, height=3, dpi=300, verbose=False)

    plot_time_2 = (
        pn.ggplot(time_df, pn.aes('datetime', 'active_leaks')) +
        pn.geom_line(size=2) +
        pn.ggtitle('Number of active leaks at all sites') +
        pn.ylab('') +
        pn.xlab('') +
        pn.scale_x_datetime(labels=date_format('%Y')) +
        pn.theme(panel_border=pn.element_rect(colour="black", fill=None, size=2),
                 panel_grid_minor_x=pn.element_blank(), panel_grid_major_x=pn.element_blank(),
                 panel_grid_minor_y=pn.element_line(colour='black', linewidth=0.5, alpha=0.3),
                 panel_grid_major_y=pn.element_line(colour='black', linewidth=1, alpha=0.5)))

    plot_time_2.save(output_directory / 'plot_time_active_{}.png'.format(sim_n),
                     width=10, height=3, dpi=300, verbose=False)

    # Site-level plots
    plot_site_1 = (
        pn.ggplot(site_df, pn.aes('cum_frac_sites', 'cum_frac_emissions')) +
        pn.geom_line(size=2) +
        pn.theme(panel_border=pn.element_rect(colour="black", fill=None, size=2),
                 panel_grid_minor_x=pn.element_blank(), panel_grid_major_x=pn.element_blank(),
                 panel_grid_minor_y=pn.element_line(colour='black', linewidth=0.5, alpha=0.3),
                 panel_grid_major_y=pn.element_line(colour='black', linewidth=1, alpha=0.5)) +
        pn.xlab('Cumulative fraction of sites') +
        pn.ylab('Cumulative fraction of emissions') +
        pn.ggtitle('Empirical cumulative distribution of site-level emissions'))

    plot_site_1.save(output_directory / 'site_cum_dist_{}.png'.format(sim_n),
                     width=5, height=4, dpi=300, verbose=False)

    # Leak plots
    plot_leak_1 = (
        pn.ggplot(leak_df, pn.aes('days_active')) + pn.geom_histogram(colour='gray') +
        pn.theme(panel_border=pn.element_rect(colour="black", fill=None, size=2),
                 panel_grid_minor_x=pn.element_blank(), panel_grid_major_x=pn.element_blank(),
                 panel_grid_minor_y=pn.element_line(colour='black', linewidth=0.5, alpha=0.3),
                 panel_grid_major_y=pn.element_line(colour='black', linewidth=1, alpha=0.5)) +
        pn.ggtitle('Distribution of leak duration') +
        pn.xlab('Number of days the leak was active') + pn.ylab('Count'))
    plot_leak_1.save(output_directory / 'leak_active_hist{}.png'.format(sim_n),
                     width=5, height=4, dpi=300, verbose=False)

    plot_leak_2 = (
        pn.ggplot(leak_df, pn.aes('cum_frac_leaks', 'cum_frac_rate', colour='status')) +
        pn.geom_line(size=2) +
        pn.scale_colour_hue(h=0.15, l=0.25, s=0.9) +
        pn.theme(panel_border=pn.element_rect(colour="black", fill=None, size=2),
                 panel_grid_minor_x=pn.element_blank(), panel_grid_major_x=pn.element_blank(),
                 panel_grid_minor_y=pn.element_line(colour='black', linewidth=0.5, alpha=0.3),
                 panel_grid_major_y=pn.element_line(colour='black', linewidth=1, alpha=0.5)) +
        pn.xlab('Cumulative fraction of leak sources') +
        pn.ylab('Cumulative leak rate fraction') +
        pn.ggtitle('Fractional cumulative distribution'))

    plot_leak_2.save(output_directory / 'leak_cum_dist1_{}.png'.format(sim_n),
                     width=4, height=4, dpi=300, verbose=False)

    plot_leak_3 = (
        pn.ggplot(leak_df, pn.aes('cum_frac_leaks', 'cum_rate', colour='status')) +
        pn.geom_line(size=2) +
        pn.scale_colour_hue(h=0.15, l=0.25, s=0.9) +
        pn.theme(panel_border=pn.element_rect(colour="black", fill=None, size=2),
                 panel_grid_minor_x=pn.element_blank(), panel_grid_major_x=pn.element_blank(),
                 panel_grid_minor_y=pn.element_line(colour='black', linewidth=0.5, alpha=0.3),
                 panel_grid_major_y=pn.element_line(colour='black', linewidth=1, alpha=0.5)) +
        pn.scale_y_continuous(trans='log10') +
        pn.xlab('Cumulative fraction of leak sources') +
        pn.ylab('Cumulative emissions (kg/day)') +
        pn.ggtitle('Absolute cumulative distribution'))

    plot_leak_3.save(output_directory / 'leak_cum_dist2_{}.png'.format(sim_n),
                     width=4, height=4, dpi=300, verbose=False)

    return
