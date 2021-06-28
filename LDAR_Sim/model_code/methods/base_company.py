# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Test company
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
import pandas as pd
from sklearn.cluster import KMeans

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

        self.timeseries['{}_sites_visited'.format(self.name)] = np.zeros(
            self.parameters['timesteps'])
        # Additional variable(s) for each site
        for site in self.state['sites']:
            site.update({'{}_t_since_last_LDAR'.format(self.name): 0})
            site.update({'{}_surveys_conducted'.format(self.name): 0})
            site.update({'{}_attempted_today?'.format(self.name): False})
            site.update({'{}_surveys_done_this_year'.format(self.name): 0})
            site.update({'{}_missed_leaks'.format(self.name): 0})

        # Use clustering analysis to assign facilities to each agent, if 2+ agents are aviable
        if self.config['n_crews'] > 1:
            Lats = []
            Lons = []
            ID = []
            for site in self.state['sites']:
                ID.append(site['facility_ID'])
                Lats.append(site['lat'])
                Lons.append(site['lon'])
            sdf = pd.DataFrame({"ID": ID,
                                'lon': Lons,
                                'lat': Lats})
            X = sdf[['lat', 'lon']].values
            num = config['n_crews']
            kmeans = KMeans(n_clusters=num, random_state=0).fit(X)
            label = kmeans.labels_
        else:
            label = np.zeros(len(self.state['sites']))

        for i in range(len(self.state['sites'])):
            self.state['sites'][i]['label'] = label[i]

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
        # scheduling['deployment_time_intervals'] defines whether to deploy tech at specific time
        # scheduling['deployment_years'] defines specific years to deploy technology
        # scheduling['depolyment_months'] defines specific month to deply technology

        self.scheduling = self.config['scheduling']
        if self.scheduling['route_planning'] and self.scheduling['deployment_time_intervals']:
            required_year = self.scheduling['deployment_years']
            required_month = self.scheduling['depolyment_months']
        else:
            required_year = list(
                range(self.state['t'].start_date.year, self.state['t'].end_date.year+1))
            required_month = list(range(1, 13))

        if self.state['t'].current_date.month in required_month \
                and self.state['t'].current_date.year in required_year:
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

                # Update method-specific site variables each day
            for site in self.state['sites']:
                site['{}_t_since_last_LDAR'.format(self.name)] += 1
                site['{}_attempted_today?'.format(self.name)] = False

            if self.config['is_follow_up']:
                self.state['flags'] = [flag for flag in self.state['sites']
                                       if flag['currently_flagged']]
            elif self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
                for site in self.state['sites']:
                    site['{}_surveys_done_this_year'.format(self.name)] = 0

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
