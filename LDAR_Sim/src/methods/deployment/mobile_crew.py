# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.mobile_crew
# Purpose:     Mobile crew specific deployment classes and methods (ie. Scheduling)
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


import numpy as np
import pandas as pd
from datetime import timedelta
from geography.homebase import find_homebase, find_homebase_opt
from geography.distance import get_distance
from methods.deployment.generic_funcs import get_work_hours


class Schedule():

    def __init__(self, id, lat, lon, state, config, parameters, deployment_days, home_bases=None):
        self.parameters = parameters
        self.config = config
        self.state = state
        self.deployment_days = deployment_days
        self.crew_lat = lat
        self.crew_lon = lon
        self.work_hours = None
        self.start_hour = None
        self.end_hour = None
        self.allowed_end_time = None
        self.last_site_travel_home_min = None
        self.rollover = None  # (rollover_site_plan)
        self.travel_all_day = False
        self.scheduling = self.config['scheduling']
        # define a list of home bases for crew and redefine the the initial location of crew
        if self.scheduling['route_planning']:
            hb_file = self.parameters['input_directory'] / self.scheduling['home_bases_files']
            HB = pd.read_csv(hb_file, sep=',')
            self.crew_lon = self.scheduling['LDAR_crew_init_location'][0]
            self.crew_lat = self.scheduling['LDAR_crew_init_location'][1]
            self.home_bases = list(zip(HB['lon'], HB['lat']))

    def start_day(self, site_pool):
        """ Start day method. Initialize time to account for work hours, and set
            the crews location. The site pool , or sites that are ready for survey
            are passed from the company to the crew in the order of neglect. Here,
            the crew estimates the time required to travel and perform survey for
            sites, and sets an itinerary or list of site plans.

            If route planning is enabled, the itinerary is optimized by travel times
            regardless of neglect. If not enabled, the itinerary is set by filling
            the day with available sites in the order provided by the company.

        Args:
            site_pool (list): List of sites ready for survey.

        Returns:
            list: Daily itinerary:
                {'site': (dict),
                'go_to_site: (boolean),
                'LDAR_mins': (int) travel to and work-onsite mins,
                'travel_to_mins': (int) travel to mins,
                'travel_home_mins': (int) travel_home_mins,
                'remaining_mins':(int)  minutes remaining in survey at site
                }
        """

        start_lon, start_lat = self.crew_lon, self.crew_lat
        site_plans_today = []
        self.travel_all_day = False
        self.work_hours, self.start_hour, self.end_hour = get_work_hours(self.config, self.state)
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(self.start_hour))  # Set start of work
        est_mins_remaining = (self.end_hour - self.start_hour)*60

        # ---- Go through Sites and get travel times ----
        # 1) Route Planning - add them to a temporary site plan list.
        #      Choose site from site plan list based on travel time.
        #      Remove choosen site from site pool, then get new travel
        #      times and repeat (using while loop).
        # 2) No Route Planning - Fill the day with sites visits and
        #      return the days site plan.

        exit_flag = True
        site_cnt = 0
        # While loop is only needed for
        while est_mins_remaining > 0 and len(site_pool) > 0:
            site_plans_tmp = []
            for sidx, site in enumerate(site_pool):
                site_cnt += 1
                site_plan = self.plan_visit(site, est_mins_remaining=est_mins_remaining)
                # site plans are dicts that include  site, LDAR_minsand go_to_site keys.
                # Site plan can be empty if weather does not permit travel
                if site_plan and site_plan['go_to_site']:
                    if self.config['scheduling']['route_planning']:
                        site_plans_tmp.append(site_plan)
                    else:
                        # The site order will not change if route_planning is not used
                        site_plans_today.append(site_plan)
                        est_mins_remaining -= site_plan['LDAR_mins']
                        # # The following will allow the program to keep trying sites
                        # # even after one has failed, in case there is another site
                        # # that mets the criterea
                        # if est_mins_remaining <= 0:
                        #     # if the day has been filled with surveys exit for and while
                        #     # loop
                        #     exit_flag = True
                        #     break
                        exit_flag = False
                else:
                    exit_flag = True
                    break

            # If there is no route planning and the day has been filled with surveys
            # or all of the sites have been checked, exit the while loop
            if not self.config['scheduling']['route_planning'] \
                    and (exit_flag or sidx == len(site_pool) - 1):
                break

            # if a crew has sites they can go to then choose site from list
            if self.config['scheduling']['route_planning']:
                if len(site_plans_tmp) > 0:
                    # choose a site to visit (rollover site, route planning site
                    # or longest time without survey)
                    site_plan = self.choose_site(site_plans_tmp)
                    site_plans_today.append(site_plan)
                    est_mins_remaining -= site_plan['LDAR_mins']
                    site_ID = site_plan['site']['facility_ID']
                    # remove choosen site from site pool
                    site_pool = [s for s in site_pool if s['facility_ID'] != site_ID]
                    self.crew_lon = site_plan['site']['lon']
                    self.crew_lat = site_plan['site']['lat']
                else:
                    break
        # -----------------------------

        # add a site to the rollover list if there are still remainin mins in survey
        if len(site_plans_today) > 0:
            if site_plans_today[-1]['remaining_mins'] > 0:
                self.rollover = site_plans_today[-1]
        else:
            self.travel_all_day = True
        # The crew does not actually travel this is only done for planning purposes
        self.crew_lon, self.crew_lat = start_lon, start_lat

        return site_plans_today

    def end_day(self, site_pool, itinerary):
        """ Travel home; update time to travel to homebase
        """
        if self.config['scheduling']['route_planning']:
            if self.travel_all_day:
                self.next_travel_all_day_site = site_pool[0]
                self.choose_accommodation(site=self.next_travel_all_day_site)
            else:
                self.choose_accommodation()
        elif len(itinerary) > 0:
            self.state['t'].current_date += timedelta(
                minutes=int(itinerary[-1]['travel_home_mins']))

    def plan_visit(self, site, next_site=None, est_mins_remaining=None):
        """ Check survey and travel times and see if there is enough time
            to go to site. If a site survey was started on a previous day
            the amount of minutes rolled over will be used for survey time.

        Args:
            site (dict): single site
            next_site (dict): single site used for estimating next

        Returns:
            {
                'site': same as input
                'go_to_site': whether there is enough time to go to site
                'travel_to_mins': travel time in minutes
                'travel_home_mins': travel time in minutes
                'LDAR_mins_onsite': minutes onsite
                'LDAR_mins': travel to and survey time (excludes travel home time)
                'remaining_mins': minutes left in survey
        }
        """
        name = self.config['label']
        site['{}_attempted_today?'.format(name)] = True

        # Check weather conditions
        if self.parameters['consider_weather'] \
            and not self.deployment_days[site['lon_index'], site['lat_index'],
                                         self.state['t'].current_timestep]:
            return None
        if self.rollover:
            if site['facility_ID'] == self.rollover['site']['facility_ID']:
                # Remove facility from rollover list, and retrieve remaining survey minutes
                LDAR_mins = self.rollover['remaining_mins']
            else:
                LDAR_mins = int(site['{}_time'.format(name)])
        else:
            # Get survey minutes
            LDAR_mins = int(site['{}_time'.format(name)])
        # Get travel time minutes, and check if there is enough time.
        travel_to_plan = self.upd_travel_time_loc(next_loc=site)
        travel_home_plan = self.upd_travel_time_loc(next_loc=next_site, is_homebase=True)
        survey_times = self.check_visit_time(
            LDAR_mins,
            travel_to_plan['travel_time'],
            travel_home_plan['travel_time'],
            est_mins_remaining)
        return {
            'site': site,
            'go_to_site': survey_times['go_to_site'],
            'travel_to_mins': travel_to_plan['travel_time'],
            'travel_home_mins': travel_home_plan['travel_time'],
            'LDAR_mins_onsite': survey_times['LDAR_mins_onsite'],
            # mins is LDAR + Travel to time. Home time is called at end of day
            'LDAR_mins': survey_times['LDAR_mins'],
            'remaining_mins': survey_times['remaining_mins'],
        }

    def upd_travel_time_loc(self, next_loc=None, is_homebase=False):
        """ Get travel time to next location and next homebase

        Args:
            next_loc (dict, optional): next site. Defaults to None.
            is_homebase (bool, optional): If next site is a homebase. Defaults to False.

        Returns:
            dict: {
                'travel_time': time in minutes to trave between current site and crews
                               current location
                'next_site': next location the crew will travel to.
            }
        """
        if self.config['scheduling']['route_planning']:
            # start day by reading the location of the LDAR team
            # find nearest home base
            if is_homebase and next_loc:
                next_loc, distance = find_homebase_opt(
                    self.crew_lon, self.crew_lat,
                    next_loc['lon'], next_loc['lat'], self.home_bases)
            elif is_homebase and not next_loc:
                next_loc, distance = find_homebase(
                    self.crew_lon, self.crew_lat, self.home_bases)
            else:
                distance = get_distance(
                    self.crew_lon, self.crew_lat,
                    next_loc['lon'], next_loc['lat'], "Haversine")

            speed = np.random.choice(self.config['scheduling']['travel_speeds'])
            travel_time = (distance/speed)*60
        # ----------------------------------------------------------
        else:
            travel_time = np.random.choice(self.config['t_bw_sites']['vals'])
        # returned dictionary
        out_dict = {
            'travel_time': travel_time,
            'next_loc': next_loc,
        }
        return out_dict

    def check_visit_time(self, survey_mins, travel_to_mins,
                         travel_home_mins, mins_left_in_day=None):
        """Check the survey and travel times, determine if there is enough
           time to go to site.

        Args:
            survey_mins (float): minutes required to perform or finish survey
            travel_to_mins (float): minutes required to travel to site
            travel_home_mins (float): minutes required to travel home from site

        Returns:
            dict:   'go_to_site' (boolean): go_to_site,
                    'LDAR_mins_onsite' (minutes): survey time today,
                    'travel_to_mins' (minutes): travel time to site,
                    'travel_home_mins' (minutes): travel time from site,
                    'remaining_mins' (minutes): minutes left in survey that can be rolled over
                     to another day,
        """
        if travel_to_mins >= mins_left_in_day:
            # Not enough time to travel to site
            go_to_site = False
            LDAR_mins_onsite = 0
        else:
            go_to_site = True
            if (travel_to_mins + survey_mins) > mins_left_in_day:
                LDAR_mins_onsite = mins_left_in_day - travel_to_mins
            else:
                LDAR_mins_onsite = survey_mins

        remaining_mins = survey_mins - LDAR_mins_onsite
        LDAR_mins = travel_to_mins + LDAR_mins_onsite
        if go_to_site:
            self.last_site_travel_home_min = travel_home_mins
        out_dict = {
            'LDAR_mins': LDAR_mins,
            'go_to_site': go_to_site,
            'LDAR_mins_onsite': LDAR_mins_onsite,
            'travel_to_mins': travel_to_mins,
            'travel_home_mins': travel_home_mins,
            'remaining_mins': remaining_mins,
        }
        return out_dict
    # ---------------------------------------------

    def choose_site(self, site_plans):
        """Choose the next visit site based on travel time

        Args:
            site_plans: a list of travel plan dictionary output from plan_visit()

        Returns:
            A dictionary (travel plan) of the selected site
        """
        if self.rollover:
            site_plan = self.rollover

        # route planning -> find the nearest site
        if self.config['scheduling']['route_planning']:
            # sort the list based on travel time
            sorted_site_plans = sorted(
                site_plans, key=lambda k: k['travel_to_mins'])
            # first site plan in the sorted list has minimum travel time
            site_plan = sorted_site_plans[0]

        else:
            # else just need 1st site to visit
            site_plan = site_plans[0]
        return site_plan

    # ------------------------------------------------
    def choose_accommodation(self, site=None):
        """choose the home base for crew

        Args:
            site: if site is defined, then choose the home base that close to both current
            location and next site
        Returns:

        """
        if self.config['scheduling']['route_planning']:
            if site:
                # today needs to travel all day
                hb = self.upd_travel_time_loc(next_loc=site, is_homebase=True)

            else:
                # if not means crew need to travel all the way to reach the next site
                hb = self.upd_travel_time_loc(is_homebase=True)

            self.crew_lon = hb['next_loc'][0]
            self.crew_lat = hb['next_loc'][1]
            self.last_site_travel_home_min = hb['travel_time']
        else:
            # travel time is sampled if not active route_planning
            self.last_site_travel_home_min = np.random.choice(
                self.config['t_bw_sites']['vals'])
