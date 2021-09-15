# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.company
# Purpose:     Initialize companies, generate crews, deploy crews and reporting
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
        self.site_watchlist = {}
        self.crews = []
        deploy_mod = import_module('methods.deployment.{}_company'.format(
            self.config['deployment_type'].lower()))
        Schedule = getattr(deploy_mod, 'Schedule')
        self.schedule = Schedule(config, parameters, state)
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            config=config,
            start_date=self.state['t'].start_date,
            start_work_hour=8,  # Start hour in day
            consider_weather=parameters['consider_weather'])

        # --- init time series ---
        n_ts = parameters['timesteps']
        self.timeseries['{}_prop_sites_avail'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_cost'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_sites_visited'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_travel_time'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_survey_time'.format(self.name)] = np.zeros(n_ts)
        if self.config["measurement_scale"] == 'component':
            # If the technology is for flagging
            self.timeseries['{}_redund_tags'.format(self.name)] = np.zeros(n_ts)
        else:
            self.timeseries['{}_eff_flags'.format(self.name)] = np.zeros(n_ts)
            self.timeseries['{}_flags_redund1'.format(self.name)] = np.zeros(n_ts)
            self.timeseries['{}_flags_redund2'.format(self.name)] = np.zeros(n_ts)
            self.timeseries['{}_flag_wo_vent'.format(self.name)] = np.zeros(n_ts)

            # Assign the correct follow-up threshold

            if self.config['follow_up']['threshold_type'] == "absolute":
                self.config['follow_up']['thresh'] = self.config['follow_up']['threshold']
            elif self.config['follow_up']['threshold_type'] == "proportion":
                self.config['follow_up']['thresh'] = get_prop_rate(
                    self.config['follow_up']['proportion'],
                    self.state['empirical_leaks'])
            else:
                print('Follow-up thresh type not recognized. Must be "absolute" or "proportion".')

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
        for idx, cnt in enumerate(self.crews):
            self.timeseries['{}_cost'.format(self.name)][self.state['t'].current_timestep] += \
                self.config['cost']['upfront']

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
            # Get sites that are ready for survey
            site_pool = self.schedule.get_due_sites(site_pool)
            # Get number of crews working that day based on number of sites ready for visit
            if self.config['deployment_type'] == 'stationary':
                # assume all crews/sensors are working
                n_working_crews = len(self.crews)
            else:
                n_working_crews = self.schedule.get_working_crews(site_pool, self.config['n_crews'])
            for idx in range(n_working_crews):
                # Triage sites to crew
                crew_site_list = self.schedule.get_crew_site_list(site_pool, idx,
                                                                  n_working_crews, self.crews)
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
        site_wl = self.site_watchlist
        # Go through Each Candidate site, and add it to the watchlist
        # A watchlist keeps track of sites with leaks that have not yet been flagged
        for site in self.candidate_flags:
            facility_ID = site['site']['facility_ID']
            if facility_ID not in site_wl:
                site_wl.update(
                    {facility_ID: {
                        'site': site['site'],
                        'dates': [self.state['t'].current_date],
                        'measured_emis_rates': [site['site_measured_rate']],
                        'measured_vent_rates': [site['venting']],
                        'effective_emis_rate': site['site_measured_rate'],
                        'effective_vent_rate': site['venting']
                    }})
            else:
                site_wl[facility_ID]['dates'].append(self.state['t'].current_date)
                site_wl[facility_ID]['measured_emis_rates'].append(site['site_measured_rate'])
                site_wl[facility_ID]['measured_vent_rates'].append(site['venting'])
                # Calculate effective emissions and vent rates
                site_wl[facility_ID]['effective_leak_rate'] = self.aggregate_by(
                    site_wl[facility_ID]['measured_emis_rates'],
                    self.config['follow_up']['redundancy_filter']
                )
                site_wl[facility_ID]['effective_vent_rate'] = self.aggregate_by(
                    site_wl[facility_ID]['measured_vent_rates'],
                    self.config['follow_up']['redundancy_filter']
                )

        # Sort Watchlist by emissions rate
        site_wl = {k: v for k, v in sorted(
            site_wl.items(),
            key=lambda x: x[1]['effective_emis_rate'],
            reverse=True)
        }

        # Get instant follow-up sites and init follow-up sites based on follow_up delay
        IFU_sites = []
        if self.config['follow_up']['instant_threshold']:
            target_sites = []
            for sdx, site in site_wl.items():
                if site['effective_emis_rate'] > self.config['follow_up']['instant_threshold']:
                    IFU_sites.append(site)
                elif len(site['measured_emis_rates']) > self.config['follow_up']['delay']:
                    target_sites.append(site)
        else:
            target_sites = [site for sdx, site in site_wl.items()
                            if len(site['measured_emis_rates'])
                            > self.config['follow_up']['delay']]

        # Get portion of sites and threshold filtered sited
        if self.config['follow_up']['interaction_priority'] == 'proportion':
            n_sites_to_flag = len(target_sites) * self.config['follow_up']['proportion']
            n_sites_to_flag = int(math.ceil(n_sites_to_flag))
            target_sites = [site for site in target_sites[:n_sites_to_flag]
                            if site['effective_emis_rate']
                            > self.config['follow_up']['threshold']]
        else:
            target_sites = [site for site in target_sites
                            if site['effective_emis_rate'] > self.config['follow_up']['threshold']]
            n_sites_to_flag = len(target_sites) * self.config['follow_up']['proportion']
            n_sites_to_flag = int(math.ceil(n_sites_to_flag))
            target_sites = target_sites[:n_sites_to_flag]

        # Move IFU Sites to front of queue
        target_sites = IFU_sites + target_sites

        # Go through all targeted sites and flag them or add them to redundant lists
        for targ_site in target_sites:
            site_obj = targ_site['site']
            site_true_rate = targ_site['effective_emis_rate']
            venting = targ_site['effective_vent_rate']
            site_wl.pop(site_obj['facility_ID'])

            # If the site is already flagged, your flag is redundant
            if site_obj['currently_flagged']:
                self.timeseries['{}_flags_redund1'.format(
                    self.name)][self.state['t'].current_timestep] += 1
            else:
                # Flag the site for follow up
                site_obj['currently_flagged'] = True
                site_obj['date_flagged'] = self.state['t'].current_date
                site_obj['flagged_by'] = self.config['label']
                self.timeseries['{}_eff_flags'.format(
                    self.name)][self.state['t'].current_timestep] += 1

                # Redand2 is hard to keep track of with multiple sets of serveys
                # Disable for now

                # # Does the chosen site already have tagged leaks?
                # redund2 = False
                # for leak in site_obj['leaks_present']:
                #     if leak['date_tagged'] is not None:
                #         redund2 = True
                # if redund2:
                #     self.timeseries['{}_flags_redund2'.format(
                #         self.name)][self.state['t'].current_timestep] += 1

                # Would the site have been chosen without venting?
                if self.parameters['consider_venting']:
                    if (site_true_rate - venting) < self.config['follow_up']['thresh']:
                        self.timeseries['{}_flag_wo_vent'.format(self.name)][
                            self.state['t'].current_timestep] += 1

    def aggregate_by(self, list, filter):
        '''
        Gets the affective aggregated value from a list based on an input filter
        Values of the filter can be 'recent', 'max', or 'mean'

        '''
        if filter == 'recent':
            return list[-1]
        elif filter == 'max':
            return max(list)
        elif filter == 'mean':
            return np.average(list)

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
