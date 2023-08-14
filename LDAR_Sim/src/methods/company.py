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
from datetime import timedelta
from importlib import import_module

import numpy as np
from methods.deployment.generic_funcs import get_deployment_dates
from utils.attribution import update_flag
from utils.generic_functions import get_prop_rate


class BaseCompany:
    """ Base companies are used by methods to generate crews, company-level scheduling,
        deploy crews, flag sites and carry out reporting.
    """

    def __init__(
            self,
            state,
            program_parameters,
            virtual_world,
            simulation_settings,
            config,
            timeseries,
            module_name
    ):
        """
        Initialize a company to manage the crews (e.g. a contracting company).

        """
        self.name, self.state, = config['label'], state
        self.program_parameters = program_parameters
        self.consider_venting = virtual_world['emissions']['consider_venting']
        self.config = config
        self.timeseries = timeseries
        self.site_watchlist = {}
        self.crews = []
        deploy_mod = import_module('methods.deployment.{}_company'.format(
            self.config['deployment_type'].lower()))
        Schedule = getattr(deploy_mod, 'Schedule')
        self.schedule = Schedule(config, program_parameters, state)
        self.deployment_years, self.deployment_months = get_deployment_dates(
            config, state)
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            config=config,
            start_date=self.state['t'].start_date,
            start_work_hour=8,  # Start hour in day
            consider_weather=virtual_world['consider_weather'])

        # --- init time series ---
        n_ts = virtual_world['timesteps']
        self.timeseries['{}_prop_sites_avail'.format(
            self.name)] = np.zeros(n_ts)
        self.timeseries['{}_cost'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_sites_visited'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_travel_time'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_survey_time'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_redund_tags'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_missed_leaks'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_sites_vis_w_leaks'.format(
            self.name)] = np.zeros(n_ts)
        self.timeseries['{}_eff_flags'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_n_tags'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_flags_redund1'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_flags_redund2'.format(self.name)] = np.zeros(n_ts)
        self.timeseries['{}_flag_wo_vent'.format(self.name)] = np.zeros(n_ts)

        if self.config["measurement_scale"] != 'component':
            # Assign the correct follow-up threshold
            if self.config['follow_up']['threshold_type'] == "absolute":
                self.config['follow_up']['thresh'] = self.config['follow_up']['threshold']
            elif self.config['follow_up']['threshold_type'] == "proportion":
                self.config['follow_up']['thresh'] = get_prop_rate(
                    self.config['follow_up']['proportion'],
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
            survey_min_interval = '{}_min_int'.format(self.name)
            if survey_min_interval in site:
                t_since_last_LDAR = site[survey_min_interval]
            else:
                t_since_last_LDAR = 0
            site.update({'{}_t_since_last_LDAR'.format(
                self.name): t_since_last_LDAR})
            site.update({'{}_surveys_conducted'.format(self.name): 0})
            site.update({'{}_attempted_today?'.format(self.name): False})
            site.update({'{}_surveys_done_this_year'.format(self.name): 0})
            site.update({'{}_missed_leaks'.format(self.name): 0})

        make_crew_loc = import_module('methods.deployment.{}_company'.format(
            self.config['deployment_type'].lower()))
        make_crews = getattr(make_crew_loc, 'make_crews')
        make_crews(
            self.crews,
            config,
            state,
            program_parameters,
            virtual_world,
            simulation_settings,
            timeseries,
            self.deployment_days
        )
        for idx, cnt in enumerate(self.crews):
            self.timeseries['{}_cost'.format(self.name)][self.state['t'].current_timestep] += \
                self.config['cost']['upfront']

        self.schedule.assign_agents()

    def deploy_crews(self):
        """
        The company tells all the crews to get to work.
        """
        # NOTE: crew checks weather conditions at start of the day
        c_date = self.state['t'].current_date
        if c_date.month in self.deployment_months and c_date.year in self.deployment_years:
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
                n_working_crews = self.schedule.get_working_crews(
                    site_pool, self.config['n_crews'])
            for idx in range(n_working_crews):
                # Triage sites to crew
                crew_site_list = self.schedule.get_crew_site_list(site_pool, idx,
                                                                  n_working_crews, self.crews)
                # Send crew to site
                if len(crew_site_list) > 0:
                    self.crews[idx].work_a_day(
                        crew_site_list, self.candidate_flags)
            if len(self.candidate_flags) > 0:
                self.candidates_to_watchlist()

            # Calculate proportion sites available based on weather of site
            available_sites = sum([1 for site in self.state['sites']
                                   if self.deployment_days[site['lon_index'], site['lat_index'],
                                                           self.state['t'].current_timestep]])
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
            if self.state['t'].current_date.day == 31 \
                    and self.state['t'].current_date.month == 12:
                site[sites_this_year] = 0

        # Daily check of watchlist
        if len(self.site_watchlist) > 0:
            self.flag_sites()

        # Update followup specific parameters
        if self.config['is_follow_up']:
            self.state['flags'] = [site['facility_ID'] for site in self.state['sites']
                                   if site['currently_flagged']]
        return

    def candidates_to_watchlist(self):
        """
        Add candidate sites to watchlist, and calculate a site emission rate if there are
        multiple emissions measurements. The watchlist allows companies to keep track of
        candidate site surveys. This is utilized by a company when a follow_up_delay
        is greater than zero, as multiple surveys can be done for each site before a site
        is flagged.

        If an instant repair threshold is utilized and a sites  emissions rate is greater than
        the instant followup threshold, the site will be immediately flagged.

        """
        site_wl = self.site_watchlist

        # Go through each Candidate site, and add it to the watchlist
        # A watchlist keeps track of sites with leaks that have not yet been flagged
        for site in self.candidate_flags:
            facility_ID = site['site']['facility_ID']
            # Get instant follow-up sites and init follow-up sites based on follow_up delay
            if self.config['follow_up']['instant_threshold'] \
                    and site['site_measured_rate'] > self.config['follow_up']['instant_threshold']:
                self.flag_site(site)
                # Remove the site from the watchlist if it needs an instant followup
                if facility_ID in site_wl:
                    site_wl.pop(facility_ID)
            elif facility_ID not in site_wl:
                site_wl.update(
                    {facility_ID: {
                        'site': site['site'],
                        'dates': [self.state['t'].current_date],
                        'measured_emis_rates': [site['site_measured_rate']],
                        'measured_vent_rates': [site['vent_rate']],
                        'site_measured_rate': site['site_measured_rate'],
                        'vent_rate': site['vent_rate']
                    }})
            else:
                site_wl[facility_ID]['dates'].append(
                    self.state['t'].current_date)
                site_wl[facility_ID]['measured_emis_rates'].append(
                    site['site_measured_rate'])
                site_wl[facility_ID]['measured_vent_rates'].append(
                    site['vent_rate'])
                # Calculate effective emissions and vent rates
                site_wl[facility_ID]['site_measured_rate'] = self.aggregate_by(
                    site_wl[facility_ID]['measured_emis_rates'],
                    self.config['follow_up']['redundancy_filter']
                )
                site_wl[facility_ID]['vent_rate'] = self.aggregate_by(
                    site_wl[facility_ID]['measured_vent_rates'],
                    self.config['follow_up']['redundancy_filter']
                )

        # Sort Watchlist by emissions rate
        # This ensures that the leakiest sites are at the top of the dictionary
        # so proportional site followup can be performed without resorting everyday
        # within the flag_sites function.
        site_wl = {k: v for k, v in sorted(
            site_wl.items(),
            key=lambda x: x[1]['site_measured_rate'],
            reverse=True)
        }

    def flag_site(self, site):
        """ Flag a single site and check for leak redundancy

        Args:
            site (dict): a dictionary which must have a site style dict,
                         (state['sites']) a site_measured_rate, and a site
                         vent rate
        """
        self.site_watchlist.pop(site['site']['facility_ID'], None)
        update_flag(self.config, site, self.timeseries, self.state['t'], self.state['campaigns'],
                    self.name, self.consider_venting)

    def flag_sites(self):
        """
        Performs followup proportion and threshold checks on all sites for watchlist sites
        past follow-up delay / grace period.

        """
        site_wl = self.site_watchlist
        first_survey_time = min(site['dates'][0]
                                for sidx, site in site_wl.items())
        can_flag_date = first_survey_time + \
            timedelta(days=self.config['follow_up']['delay'])
        # If the delay / grace period has passed since the first leak reported in the watchlist
        # start surveys. Date is used to ignore the hour Leak was detected and focus on the day
        # instead.
        if self.state['t'].current_date.date() >= can_flag_date.date():
            # Get portion of sites and threshold filtered sited
            if self.config['follow_up']['interaction_priority'] == 'proportion':
                prop_to_flag = int(math.ceil(
                    len(site_wl) * self.config['follow_up']['proportion']))
                # site_wl is an ordered by leak size.
                if prop_to_flag > 0.0:
                    site_wl_subset = list(site_wl.values())[:prop_to_flag]
                    target_sites = [site for site in site_wl_subset
                                    if site['site_measured_rate']
                                    > self.config['follow_up']['threshold']]
            if self.config['follow_up']['interaction_priority'] == 'threshold':
                sites_above_thresh = [site for sdx, site in site_wl.items()
                                      if site['site_measured_rate']
                                      > self.config['follow_up']['threshold']]
                prop_to_flag = int(math.ceil(
                    len(sites_above_thresh) * self.config['follow_up']['proportion']))
                target_sites = sites_above_thresh[:prop_to_flag]
            # Go through all targeted sites and flag them or add them to redundant lists
            for targ_site in target_sites:
                self.flag_site(targ_site)
            # Reset watchlist
            self.site_watchlist = {}

    def aggregate_by(self, list, filter):
        '''
        Gets the effective aggregated value from a list based on an input filter
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
