# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Satellite company
# Purpose:     Company managing aircraft agents
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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


import numpy as np
from satellite import satellite
from generic_functions import get_prop_rate
import math


class satellite_company:
    def __init__(self, state, parameters, config, timeseries, module_name):
        """
        Initialize a company to manage the satellite
        """
        self.name = 'satellite'
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            start_date=self.state['t'].start_date,
            start_work_hour=24,  # Start hour in day
            consider_weather=parameters['consider_weather'])
        self.timeseries['satellite_prop_sites_avail'] = []
        self.timeseries['satellite_cost'] = np.zeros(
            self.parameters['timesteps'])
        self.timeseries['satellite_eff_flags'] = np.zeros(
            self.parameters['timesteps'])
        self.timeseries['satellite_flags_redund1'] = np.zeros(
            self.parameters['timesteps'])
        self.timeseries['satellite_flags_redund2'] = np.zeros(
            self.parameters['timesteps'])
        self.timeseries['satellite_flags_redund3'] = np.zeros(
            self.parameters['timesteps'])
        self.timeseries['satellite_sites_visited'] = np.zeros(
            self.parameters['timesteps'])

        # Assign the correct follow-up threshold
        if self.config['follow_up_thresh'][1] == "absolute":
            self.config['follow_up_thresh'] = self.config['follow_up_thresh'][0]
        elif self.config['follow_up_thresh'][1] == "proportion":
            self.config['follow_up_thresh'] = get_prop_rate(
                self.config['follow_up_thresh'][0],
                self.state['empirical_leaks'])
        else:
            print(
                'Follow-up threshold type not recognized. Must be "absolute" or "proportion".')

        # Additional variable(s) for each site
        for site in self.state['sites']:
            site.update({'satellite_t_since_last_LDAR': 0})
            site.update({'satellite_surveys_conducted': 0})
            site.update({'attempted_today_satellite?': False})
            site.update({'surveys_done_this_year_satellite': 0})
            site.update({'satellite_missed_leaks': 0})

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))

        # Initialize the individual satellite (the agents)
        for i in range(config['n_crews']):
            self.crews.append(satellite(state, parameters, config,
                                        timeseries, self.deployment_days, id=i + 1))

        return

    def deploy_crews(self):
        """
        The stellite company tells all the crews to get to work.
        """

        self.candidate_flags = []
        for i in self.crews:
            i.work_a_day(self.candidate_flags)

        # Flag sites according to the flag ratio
        if len(self.candidate_flags) > 0:
            self.flag_sites()

        # Update method-specific site variables each day
        for site in self.state['sites']:
            site['satellite_t_since_last_LDAR'] += 1
            site['attempted_today_satellite?'] = False

        if self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
            for site in self.state['sites']:
                site['surveys_done_this_year_satellite'] = 0

        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'],
                                    site['lat_index'],
                                    self.state['t'].current_timestep]:
                available_sites += 1
        prop_avail = available_sites / len(self.state['sites'])
        self.timeseries['satellite_prop_sites_avail'].append(prop_avail)

        return

    def flag_sites(self):
        """
        Flag the most important sites for follow-up.

        """
        # First, figure out how many sites you're going to choose
        n_sites_to_flag = len(self.candidate_flags) * \
            self.config['follow_up_ratio']
        n_sites_to_flag = int(math.ceil(n_sites_to_flag))

        sites_to_flag = []
        measured_rates = []

        for i in self.candidate_flags:
            measured_rates.append(i['site_measured_rate'])
        measured_rates.sort(reverse=True)
        target_rates = measured_rates[:n_sites_to_flag]

        for i in self.candidate_flags:
            if i['site_measured_rate'] in target_rates:
                sites_to_flag.append(i)

        for i in sites_to_flag:
            site = i['site']
            leaks_present = i['leaks_present']
            site_true_rate = i['site_true_rate']
            venting = i['venting']

            # If the site is already flagged, your flag is redundant
            if site['currently_flagged']:
                self.timeseries['satellite_flags_redund1'][self.state['t'].current_timestep] += 1

            elif not site['currently_flagged']:
                # Flag the site for follow up
                site['currently_flagged'] = True
                site['date_flagged'] = self.state['t'].current_date
                site['flagged_by'] = self.config['label']
                self.timeseries['satellite_eff_flags'][self.state['t'].current_timestep] += 1

                # Does the chosen site already have tagged leaks?
                redund2 = False
                for leak in leaks_present:
                    if leak['date_tagged'] is not None:
                        redund2 = True

                if redund2:
                    self.timeseries['satellite_flags_redund2'][self.state['t'].current_timestep] \
                        += 1

                # Would the site have been chosen without venting?
                if self.parameters['consider_venting']:
                    if (site_true_rate - venting) < self.config['follow_up_thresh']:
                        self.timeseries['satellite_flags_redund3'][
                            self.state['t'].current_timestep] += 1

    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs)
        for each site.
        """

        for site in self.state['sites']:
            site['satellite_prop_DDs'] = self.DD_map[site['lon_index'],
                                                     site['lat_index']]
            site['satellite_MCB'] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
