# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.mobile_company
# Purpose:     Mobile company specific deployment classes and methods (ie. Scheduling)
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
import pandas as pd
from utils.scheduling_utils import is_leap_year
from methods.crew import BaseCrew
from sklearn.cluster import KMeans


def make_crews(
        crews,
        config,
        state,
        program_parameters,
        virtual_world,
        simulation_settings,
        timeseries,
        deployment_days
):
    """ Generate crews using BaseCrew class.

    Args:
        crews (list): List of crews
        config (dict): Method parameters
        state (dict): Current state of LDAR-Sim
        program_parameters (dict): Program parameters
        virtual_world (dict): Dictionary tracking virtual world properties
        simulation_setting (dict): setting informing simulation properties
        timeseries (dict): Timeseries
        deployment_days (list): days method can be deployed based on weather

    --- Required in module.company.BaseCompany ---
    """
    for i in range(config['n_crews']):
        crews.append(
            BaseCrew(
                state,
                program_parameters,
                virtual_world,
                simulation_settings,
                config,
                timeseries,
                deployment_days,
                id=i + 1
            )
        )


class Schedule():
    def __init__(self, config, program_parameters, state):
        self.program_parameters = program_parameters
        self.config = config
        self.state = state

    def assign_agents(self):
        """ If route planning is enabled, use k-means clustering to split site into N clusters
            N equals to the number of crews.

            The goal is to improve the coordination of LDAR crews when there are
            more than one crew. The crews will only visit the site corresponding to their IDs.
            e.g., crew_ID 0 will only visit site in cluster 0

            This functionality is only used when geography and route_planning are both enabled.

            Returns:
                create a crew_ID related label for each site
        """
        if self.config['scheduling']['route_planning']:
            # Use clustering analysis to assign facilities to each agent,
            # if 2+ agents are available
            if self.config['n_crews'] > 1:
                lats = []
                lons = []
                ID = []
                for site in self.state['sites']:
                    ID.append(site['facility_ID'])
                    lats.append(site['lat'])
                    lons.append(site['lon'])
                # a temporary dataframe created for storing ID, coordinates of sites
                sdf = pd.DataFrame({"ID": ID, 'lon': lons, 'lat': lats})
                locs = sdf[['lat', 'lon']].values
                num = self.config['n_crews']
                #  run K-means clustering by using dataframe
                kmeans = KMeans(n_clusters=num, random_state=0).fit(locs)
                label = kmeans.labels_
            else:
                label = np.zeros(len(self.state['sites']))

            for i in range(len(self.state['sites'])):
                self.state['sites'][i]['crew_ID'] = label[i]

    def get_due_sites(self, site_pool):
        """ Retrieve a site list of sites due for screen / survey

            If the method is a followup, return sites that have passed
            the reporting delay window.

            If the method is not followup return sites that have passed
            the minimum survey interval, and that still require surveys
            in the current year.

        Args:
            site_pool (dict): List of sites
        Returns:
            out_sites (dict): List of sites ready for survey.
        """
        name = self.config['label']
        days_since_LDAR = '{}_t_since_last_LDAR'.format(name)
        survey_done_this_year = '{}_surveys_done_this_year'.format(name)
        survey_min_interval = '{}_min_int'.format(name)
        survey_frequency = '{}_RS'.format(name)
        survey_time = '{}_time'.format(name)
        meth = self.program_parameters['methods']

        if self.config['is_follow_up']:
            # filter then sort
            out_sites = list(
                sorted((s for s in self.state['sites']
                        if s['facility_ID'] in site_pool
                        and ((self.state['t'].current_date - s['date_flagged']).days
                        >= meth[s['flagged_by']]['reporting_delay'])),
                       key=lambda x: x[days_since_LDAR], reverse=True))
            # filter again for if preferred followup method is equivalent to method
            out_sites = list(
                sorted(
                    (s for s in out_sites
                     if s['preferred_FU_method'] is None or
                     s['preferred_FU_method'] == self.config['label']
                     ), key=lambda x: x[days_since_LDAR], reverse=True
                )
            )
        else:
            missing_days = 0
            missing_days_array = np.zeros(12)
            current_month = self.state['t'].current_date.month
            for s in range(1, current_month+1):
                if s not in meth[name]["scheduling"]["deployment_months"]:
                    missing_days = missing_days + (365/12)
                    missing_days_array[s-1] = (365/12) + 1 if is_leap_year(
                        self.state['t'].current_date.year) and s == 2 else (365/12)
            missing_days = math.floor(missing_days)

            days_since_LDAR = '{}_t_since_last_LDAR'.format(name)

            # filter then sort
            # Sort by:
            #   if surveys done is less than the total surveys needed for that year
            #               AND
            #   days since last survey is greater or equal to
            #   the minimum time interval between surveys
            #       - should be the next survey
            #               OR
            #   minimum days have passed between surveys
            #       - survey needs to be forced to happen
            out_sites = list(
                sorted((s for s in site_pool
                        if ((s[survey_done_this_year] < int(s[survey_frequency])) and
                            (
                            (
                                (
                                    s[days_since_LDAR] +
                                    math.floor(s[survey_time]/60/self.config['max_workday']) -
                                    np.sum(
                                        missing_days_array[
                                            math.ceil(
                                                (
                                                    (self.state['t'].current_timestep -
                                                     s[days_since_LDAR]) % 365
                                                )/(365/12)
                                            ):current_month
                                        ]
                                    )
                                ) >= max(
                                    [int(s[survey_min_interval]),
                                     s['{}_min_time_bt_surveys'.format(name)]]
                                )
                            ) or
                            (
                                s[survey_done_this_year] * max(
                                    [int(s[survey_min_interval]),
                                     s['{}_min_time_bt_surveys'.format(name)]]
                                ) +
                                missing_days +
                                s['{}_min_time_bt_surveys'.format(
                                    name)] < self.state['t'].current_timestep % 365
                            )
                        ))),
                       key=lambda x: x[days_since_LDAR], reverse=True
                       )
            )

        return out_sites

    def get_working_crews(self, site_pool, n_crews):
        """ Get number of working crews that day. Based on estimate
            that a crew can do 3 sites per day.
        Args:
            site_pool (dict): List of sites
            n_crews (int): Number of crews

        Returns:
            int: Number of crews to deploy that day.
        """
        n_sites = len(site_pool)
        n_working_crews = math.ceil(n_sites/self.config['est_site_p_day'])
        # cap working crews at max number of crews
        if n_working_crews > n_crews:
            n_working_crews = n_crews
        return n_working_crews

    def get_crew_site_list(self, site_pool, crew_ID, n_crews, crews=None):
        """ This function divides the site pool among all crews. Ordering
            of sites is not changed by function.
        Args:
            site_pool (dict): List of sites
            crew_num (int): Integer index of crew
            n_crews (int): Number of crews
            crews (dict): List of crew instances- not used in mobile but
                          required for other methods

        Returns:
            dict: Crew site list (subset of site_pool)
        """
        if self.config['scheduling']['route_planning']:
            # divides the site pool based on clustering analysis
            crew_site_list = [
                site for site in site_pool if site['crew_ID'] == crew_ID]
        else:
            # This offsets by the crew number and increments by the
            # number of crews, n_crews= 3 ,  site_pool = [site[0], site[3], site[6]...]
            if len(site_pool) > 0:
                crew_site_list = site_pool[crew_ID::n_crews]
        return crew_site_list
