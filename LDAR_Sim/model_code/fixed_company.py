# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        fixed company
# Purpose:     Company managing fixed agents
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

from fixed_crew import fixed_crew
import numpy as np
import math
from generic_functions import get_prop_rate


class fixed_company:
    def __init__(self, state, parameters, config, timeseries, module_name):
        """
        Initialize a company to manage the fixed crews (e.g. a contracting company).

        """
        self.name = config['label']
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            start_date=self.state['t'].start_date,
            consider_weather=parameters['consider_weather'])
        self.timeseries['fixed_prop_sites_avail'] = []
        self.timeseries['fixed_cost'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['fixed_eff_flags'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['fixed_flags_redund1'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['fixed_flags_redund2'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['fixed_flags_redund3'] = np.zeros(self.parameters['timesteps'])

        # Assign the correct follow-up threshold
        if self.config['follow_up_thresh'][1] == "absolute":
            self.config['follow_up_thresh'] = self.config['follow_up_thresh'][0]
        elif self.config['follow_up_thresh'][1] == "proportion":
            self.config['follow_up_thresh'] = get_prop_rate(
                self.config['follow_up_thresh'][0],
                self.state['empirical_leaks'])
        else:
            print('Follow-up threshold type not recognized. Must be "absolute" or "proportion".')

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))

        # Initialize the individual fixed crews (the agents) - each is a single fixed sensor
        for site in self.state['sites']:
            n_fixed = int(site['fixed_sensors'])
            for i in range(n_fixed):
                self.crews.append(
                    fixed_crew(
                        state, parameters, config, timeseries, site, self.deployment_days,
                        id=site['facility_ID'] + '-' + str(i + 1)))
                self.timeseries['fixed_cost'][self.state['t'].current_timestep] += \
                    self.parameters['methods']['fixed']['up_front_cost']

        return

    def deploy_crews(self):
        """
        The fixed company tells all the crews to get to work.
        """
        self.candidate_flags = []
        for i in self.crews:
            if self.deployment_days[i.site['lon_index'],
                                    i.site['lat_index'],
                                    self.state['t'].current_timestep]:
                i.work_a_day(self.candidate_flags)
                i.days_skipped = 0
            else:
                i.days_skipped += 1

        # Flag sites according to the flag ratio
        if len(self.candidate_flags) > 0:
            self.flag_sites()

        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'],
                                    site['lat_index'],
                                    self.state['t'].current_timestep]:
                available_sites += 1
        prop_avail = available_sites / len(self.state['sites'])
        self.timeseries['fixed_prop_sites_avail'].append(prop_avail)

        return

    def flag_sites(self):
        """
        Flag the most important sites for follow-up.

        """
        # First, figure out how many sites you're going to choose
        n_sites_to_flag = len(self.candidate_flags) * self.config['follow_up_prop']
        n_sites_to_flag = int(math.ceil(n_sites_to_flag))

        sites_to_flag = []
        measured_rates = []

        for i in self.candidate_flags:
            measured_rates.append(i['measured_rate'])
        measured_rates.sort(reverse=True)
        target_rates = measured_rates[:n_sites_to_flag]

        for i in self.candidate_flags:
            if i['measured_rate'] in target_rates:
                sites_to_flag.append(i)

        for i in sites_to_flag:
            site = i['site']
            leaks_present = i['leaks_present']
            site_cum_rate = i['site_cum_rate']
            venting = i['venting']

            # If the site is already flagged, your flag is redundant
            if site['currently_flagged']:
                self.timeseries['fixed_flags_redund1'][self.state['t'].current_timestep] += 1

            elif not site['currently_flagged']:
                # Flag the site for follow up
                site['currently_flagged'] = True
                site['date_flagged'] = self.state['t'].current_date
                site['flagged_by'] = self.config['label']
                self.timeseries['fixed_eff_flags'][self.state['t'].current_timestep] += 1

                # Does the chosen site already have tagged leaks?
                redund2 = False
                for leak in leaks_present:
                    if leak['date_tagged'] is not None:
                        redund2 = True

                if redund2:
                    self.timeseries['fixed_flags_redund2'][self.state['t'].current_timestep] += 1

                # Would the site have been chosen without venting?
                if self.parameters['consider_venting']:
                    if (site_cum_rate - venting) < self.config['follow_up_thresh']:
                        self.timeseries['fixed_flags_redund3'][
                            self.state['t'].current_timestep] += 1

    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs)
        for each site.
        """

        for site in self.state['sites']:
            site['fixed_prop_DDs'] = self.DD_map[site['lon_index'], site['lat_index']]
            site['fixed_MCB'] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
