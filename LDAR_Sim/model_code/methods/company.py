# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.company
# Purpose:     Initialize companies, generate crews, deploy crews and reporting
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
from importlib import import_module
from generic_functions import get_prop_rate


class BaseCompany:
    """ Base companies are used by methods to generate crews, company-level scheduling,
        deploy crews, flag sites and carry out reporting.
    """

    def __init__(self, state, parameters, config, timeseries, module_name):
        """
        Initialize a company to manage the crews (e.g. a contracting company).

        """
        self.name, self.state, = config['label'], state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        deploy_mod = import_module('methods.deployment.{}_company'.format(
            self.config['deployment_type'].lower()))
        Schedule = getattr(deploy_mod, 'Schedule')
        self.schedule = Schedule(config, parameters, state)
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            start_date=self.state['t'].start_date,
            start_work_hour=8,  # Start hour in day
            consider_weather=parameters['consider_weather'])

        # --- init time series ---
        n_ts = parameters['timesteps']
        self.timeseries['{}_prop_sites_avail'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_cost'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_sites_visited'.format(self.name)] = np.zeros(n_ts)
        if self.config["measurement_scale"] == 'component':
            # If the technology is for flagging
            self.timeseries['{}_redund_tags'.format(self.name)] = np.zeros(n_ts)
        else:
            self.timeseries['{}_eff_flags'.format(self.name)] = np.zeros(n_ts)
            self.timeseries['{}_flags_redund1'.format(self.name)] = np.zeros(n_ts)
            self.timeseries['{}_flags_redund2'.format(self.name)] = np.zeros(n_ts)
            self.timeseries['{}_flags_redund3'.format(self.name)] = np.zeros(n_ts)
            # Assign the correct follow-up threshold
            if self.config['follow_up_thresh'][1] == "absolute":
                self.config['follow_up_thresh'] = self.config['follow_up_thresh'][0]
            elif self.config['follow_up_thresh'][1] == "proportion":
                self.config['follow_up_thresh'] = get_prop_rate(
                    self.config['follow_up_thresh'][0],
                    self.state['empirical_leaks'])
            else:
                print(
                    'Follow-up thresh type not recognized. Must be "absolute" or "proportion".')

        # ---Init 2D matrices to store deployment day (DD) counts and MCBs ---
        self.DD_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))

        # --- init site specific variables ---
        for site in self.state['sites']:
            site.update({'{}_t_since_last_LDAR'.format(self.name): 0})
            site.update({'{}_surveys_conducted'.format(self.name): 0})
            site.update({'{}_attempted_today?'.format(self.name): False})
            site.update({'{}_surveys_done_this_year'.format(self.name): 0})
            site.update({'{}_missed_leaks'.format(self.name): 0})

        make_crew_loc = import_module('methods.deployment.{}_company'.format(
            self.config['deployment_type'].lower()))
        make_crews = getattr(make_crew_loc, 'make_crews')
        make_crews(self.crews, config, state, parameters, timeseries, self.deployment_days)
        self.schedule.assign_agents()
        self.schedule.get_deployment_dates()

    def deploy_crews(self):
        """
        The company tells all the crews to get to work.
        """
        # NOTE: crew checks weather conditions at start of the day
        if self.schedule.in_deployment_period(self.state['t'].current_date):
            self.candidate_flags = []
            if self.config['is_follow_up']:
                site_pool = self.state['flags']
            else:
                site_pool = self.state['sites']
            # Get sites that are ready, in order of most to least neglected
            site_pool = self.schedule.get_due_sites(site_pool)
            # Get number of crews working that day based on number of sites ready for visit
            if self.config['deployment_type'] == 'stationary':
                n_working_crews = int(self.site['fixed_sensors'])
            else:
                n_working_crews = self.schedule.get_working_crews(site_pool, self.config['n_crews'])
            for idx in range(n_working_crews):
                # Triage sites to crew
                crew_site_list = self.schedule.get_crew_site_list(site_pool, idx, n_working_crews)
                # Send crew to site
                if len(crew_site_list) > 0:
                    self.crews[idx].work_a_day(crew_site_list, self.candidate_flags)
            if len(self.candidate_flags) > 0:
                self.flag_sites()

            # Calculate proportion sites available based on weather of site
            available_sites = 0
            for site in self.state['sites']:
                if self.deployment_days[site['lon_index'],
                                        site['lat_index'],
                                        self.state['t'].current_timestep]:
                    available_sites += 1
            prop_avail = available_sites / len(self.state['sites'])
            self.timeseries['{}_prop_sites_avail'.format(
                self.name)][self.state['t'].current_timestep] = prop_avail
        else:
            self.timeseries['{}_prop_sites_avail'.format(
                self.name)][self.state['t'].current_timestep] = 0

        # Update time series stats

        days_since_LDAR = '{}_t_since_last_LDAR'.format(self.name)
        attempted_today = '{}_attempted_today?'.format(self.name)
        sites_this_year = '{}_surveys_done_this_year'.format(self.name)
        for site in self.state['sites']:

            site[days_since_LDAR] += 1
            site[attempted_today] = False
            if self.state['t'].current_date.day == 1 \
                    and self.state['t'].current_date.month == 1:
                site[sites_this_year] = 0

        # Update followup specific parameters
        if self.config['is_follow_up']:
            self.state['flags'] = [flag for flag in self.state['sites']
                                   if flag['currently_flagged']]
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
                site['flagged_by'] = self.config['label']
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
            site['{}_MCB'.format(
                self.name)] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
