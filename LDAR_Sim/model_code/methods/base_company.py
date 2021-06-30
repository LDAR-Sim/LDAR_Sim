# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Travel Base Company
# Purpose:     Company managing crew agents agents
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

import math
import numpy as np

from generic_functions import get_prop_rate


class company:
    """
    Base class company function. Changes made here will affect any Inheriting
    classes. To us base class, import and use as argument arguement. ie.

    from methods.base_company import company
    class aircraft (company):
        def __init__(self, **kwargs):
            super(aircraft, self).__init__(**kwargs)
        ...

    overwrite methods by creating methods in the inheriting class
    after the __init__ function.
    """

    def __init__(self, state, parameters, config, timeseries):
        """
        Initialize a company to manage the crews (e.g. a contracting company).

        """
        self.name = config['name']
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        # HBD -- This should be done somewhere else
        if 'scheduling' in self.config:
            self.scheduling = self.config['scheduling']
        else:
            self.scheduling = {}

        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            start_date=self.state['t'].start_date,
            start_work_hour=8,  # Start hour in day
            consider_weather=parameters['consider_weather'])
        self.timeseries['{}_prop_sites_avail'.format(self.name)] = []
        self.timeseries['{}_cost'.format(self.name)] = np.zeros(self.parameters['timesteps'])
        if not config['is_screening']:
            self.timeseries['{}_redund_tags'.format(self.name)] = np.zeros(
                self.parameters['timesteps'])
        else:
            self.timeseries['{}_eff_flags'.format(self.name)] = np.zeros(
                self.parameters['timesteps'])
            self.timeseries['{}_flags_redund1'.format(self.name)] = np.zeros(
                self.parameters['timesteps'])
            self.timeseries['{}_flags_redund2'.format(self.name)] = np.zeros(
                self.parameters['timesteps'])
            self.timeseries['{}_flags_redund3'.format(self.name)] = np.zeros(
                self.parameters['timesteps'])
            # Assign the correct follow-up threshold
            if self.config['follow_up_thresh'][1] == "absolute":
                self.config['follow_up_thresh'] = self.config['follow_up_thresh'][0]
            elif self.config['follow_up_thresh'][1] == "proportion":
                self.config['follow_up_thresh'] = get_prop_rate(
                    self.config['follow_up_thresh'][0],
                    self.state['empirical_leaks'])
            else:
                print('Follow-up thresh type not recognized. Must be "absolute" or "proportion".')

        # if user does not specify deployment interval, set to all months/years
        if 'deployment_years' in self.scheduling and len(self.scheduling['deployment_years']) > 0:
            self.deployment_years = self.scheduling['deployment_years']
        else:
            self.deployment_years = list(
                range(self.state['t'].start_date.year, self.state['t'].end_date.year+1))

        if 'deployment_months' in self.scheduling and len(self.scheduling['deployment_months']) > 0:
            self.deployment_months = self.scheduling['deployment_months']
        else:
            self.deployment_months = list(range(1, 13))

        self.timeseries['{}_sites_visited'.format(self.name)] = np.zeros(
            self.parameters['timesteps'])

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))
        return

    def find_leaks(self):
        """
        The company tells all the crews to get to work.
        """
        # ----Scheduling----
        if self.state['t'].current_date.month in self.deployment_months \
                and self.state['t'].current_date.year in self.deployment_years:
            if self.config['is_screening']:
                self.candidate_flags = []
                for i in self.crews:
                    i.work_a_day(self.candidate_flags)
                # Flag sites according to the flag ratio
                if len(self.candidate_flags) > 0:
                    self.flag_sites()
            else:
                for i in self.crews:
                    i.work_a_day()

            # Calculate proportion sites available
            available_sites = 0
            for site in self.state['sites']:
                if self.deployment_days[site['lon_index'],
                                        site['lat_index'],
                                        self.state['t'].current_timestep]:
                    available_sites += 1
            prop_avail = available_sites / len(self.state['sites'])
            self.timeseries['{}_prop_sites_avail'.format(self.name)].append(prop_avail)
        else:
            self.timeseries['{}_prop_sites_avail'.format(self.name)].append(0)
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
            measured_rates.append(i['site_measured_rate'])
        measured_rates.sort(reverse=True)
        target_rates = measured_rates[: n_sites_to_flag]

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
                self.timeseries['{}_flags_redund1'.format(
                    self.name)][self.state['t'].current_timestep] += 1

            elif not site['currently_flagged']:
                # Flag the site for follow up
                site['currently_flagged'] = True
                site['date_flagged'] = self.state['t'].current_date
                site['flagged_by'] = self.config['name']
                self.timeseries['{}_eff_flags'.format(
                    self.name)][self.state['t'].current_timestep] += 1

                # Does the chosen site already have tagged leaks?
                redund2 = False
                for leak in leaks_present:
                    if leak['date_tagged'] is not None:
                        redund2 = True

                if redund2:
                    self.timeseries['{}_flags_redund2'.format(
                        self.name)][self.state['t'].current_timestep] += 1

                # Would the site have been chosen without venting?
                if self.parameters['consider_venting']:
                    if (site_true_rate - venting) < self.config['follow_up_thresh']:
                        self.timeseries['{}_flags_redund3'.format(self.name)][
                            self.state['t'].current_timestep] += 1

    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs)
        for each site.
        """

        for site in self.state['sites']:
            site['{}_prop_DDs'.format(
                self.name)] = self.DD_map[site['lon_index'], site['lat_index']]
            site['{}_MCB'.format(self.name)] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
