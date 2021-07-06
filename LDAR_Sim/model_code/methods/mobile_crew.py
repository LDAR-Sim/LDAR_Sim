# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Mobile crew
# Purpose:     Initialize each crew under company
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
import pandas as pd

from methods.base_crew import BaseCrew
from datetime import timedelta
import numpy as np
from geography.homebase import find_homebase, find_homebase_opt


class MobileCrew(BaseCrew):
    """
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(MobileCrew, self).__init__(state, parameters,
                                         config, timeseries, deployment_days, id)
        # --- Mobile specific Initalization ---
        self.worked_today = False
        self.rollover = []
        self.scheduling = self.config['scheduling']

        # IF there is scheduling or routeplanning load home bases and init LDAR Crew locations
        if self.config['scheduling']['route_planning'] or self.config['scheduling']['geography']:
            hb_file = parameters['working_directory'] + self.scheduling['home_bases']
            self.state['homebases'] = pd.read_csv(hb_file, sep=',')
            self.HX = self.state['homebases']['lon']
            self.HY = self.state['homebases']['lat']
            # initiate the location of LDAR crew
            self.state['current_x'] = self.scheduling['LDAR_crew_init_location'][0]
            self.state['current_y'] = self.scheduling['LDAR_crew_init_location'][1]
        # -------------------------------------------
    # --- Mobile specific methods ---

    def work_a_day(self, candidate_flags=None):
        """
        Go to work and find the leaks for a given day
        """
        m_name = self.config['label']
        self.worked_today = False
        self.candidate_flags = candidate_flags
        work_hours = None
        max_work = self.config['max_workday']

        if self.config['consider_daylight']:
            daylight_hours = self.state['daylight'].get_daylight(self.state['t'].current_timestep)
            if daylight_hours <= max_work:
                work_hours = daylight_hours
            elif daylight_hours > max_work:
                work_hours = max_work
        elif not self.config['consider_daylight']:
            work_hours = max_work

        if work_hours < 24 and work_hours != 0:
            start_hour = (24 - work_hours) / 2
            end_hour = start_hour + work_hours
        else:
            print(
                'Unreasonable number of work hours specified for crew ' +
                str(self.crewstate['id']))

        self.allowed_end_time = self.state['t'].current_date.replace(
            hour=int(end_hour), minute=0, second=0)
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(start_hour))  # Set start of work

        # agent-level scheduling for geography (real home bases locations)
        if self.scheduling['geography']:
            # start day with the current location of the LDAR team
            # HBD -- Is there supposed to be more code here?
            crew_x = self.state['current_x']
            crew_y = self.state['current_y']
        else:
            # Start day with random "t_bw_sites" required for driving to first site
            self.state['t'].current_date += timedelta(
                minutes=int(np.random.choice(self.config['t_bw_sites'])))

        # Check if there is a partially finished site from yesterday
        if len(self.rollover) > 0:
            # Check to see if the remainder of this site can be finished today
            # (if not, this one is huge!) projection includes the time it would
            #  time to travel back to the home base
            projected_end_time = self.state['t'].current_date + \
                timedelta(minutes=int(self.rollover[1]))

            # agent-level scheduling for geography (real home bases locations)
            if self.scheduling['geography']:
                # start day by reading the location of the LDAR team
                # find nearest home base
                home_loc, distance = find_homebase(crew_x, crew_y, self.HX, self.HY)
                crew_x = home_loc[0]
                crew_y = home_loc[1]
                self.state['current_x'] = crew_x
                self.state['current_y'] = crew_y
                speed = np.random.choice(self.config['scheduling']['speed_list'])
                travel_home = timedelta(minutes=(distance/speed)*60)
            # ----------------------------------------------------------
            else:
                travel_home = timedelta(minutes=int(np.random.choice(self.config['t_bw_sites'])))

            if (projected_end_time + travel_home) > self.allowed_end_time:
                # There's not enough time left for that site today -
                #  get started and figure out how much time remains
                minutes_remaining = (projected_end_time - self.allowed_end_time).total_seconds()/60
                # self.rollover = []
                self.rollover[0] = self.rollover[0]
                self.rollover[1] = minutes_remaining
                # self.rollover.append(self.rollover[0])
                # self.rollover.append(minutes_remaining)
                self.state['t'].current_date = self.allowed_end_time
                self.worked_today = True
            elif (projected_end_time + travel_home) <= self.allowed_end_time:
                # Looks like we can finish off that site today
                self.visit_site(self.rollover[0], travel_home.seconds/60)
                self.rollover = []
                self.worked_today = True

        # -agent-level scheduling for geography (real home bases locations)
        if self.scheduling['geography']:
            # start day by reading the location of the LDAR team
            crew_x = self.state['current_x']
            crew_y = self.state['current_y']
            while self.state['t'].current_date.hour < int(end_hour):
                facility_ID, found_site, site, travel_time = self.choose_site(crew_x, crew_y)
                if not found_site:
                    home_loc, distance = find_homebase(crew_x, crew_y, self.HX, self.HY)
                    crew_x = home_loc[0]
                    crew_y = home_loc[1]
                    self.state['current_x'] = crew_x
                    self.state['current_y'] = crew_y
                    break  # Break out

                if found_site:
                    projected_end_time = self.state['t'].current_date + \
                        timedelta(minutes=int(site['{}_time'.format(m_name)]))

                self.state['t'].current_date += timedelta(minutes=travel_time)

                if self.state['t'].current_date.hour > int(end_hour):
                    x_temp = np.float(site['lon'])
                    y_temp = np.float(site['lat'])
                    x_cut = self.state['current_x']
                    y_cut = self.state['current_y']
                    home_loc, distance = find_homebase_opt(
                        x_temp, y_temp, x_cut, y_cut, self.HX, self.HY)

                    self.state['current_x'] = home_loc[0]
                    self.state['current_y'] = home_loc[1]
                    minutes_remaining = (
                        projected_end_time - self.allowed_end_time).total_seconds()/60
                    self.rollover = []
                    self.rollover.append(site)
                    self.rollover.append(minutes_remaining)
                    self.state['t'].current_date = self.allowed_end_time
                    break
                else:
                    crew_x = np.float(site['lon'])
                    crew_y = np.float(site['lat'])
                    self.visit_site(site, travel_time)
                self.worked_today = True
        # ----------------------------------------------------------
        else:
            # self.state['t'].current_date += timedelta(
            #     minutes=int((np.random.choice(self.config['t_bw_sites']))))
            while self.state['t'].current_date < self.allowed_end_time:
                facility_ID, found_site, site, travel_time = self.choose_site(0, 0)
                if not found_site:
                    break  # Break out if no site can be found

                # Check to make sure there's enough time left in the day to do this site
                # This projection includes the time it would time to travel back to the home base
                if found_site:
                    projected_end_time = self.state['t'].current_date + \
                        timedelta(minutes=int(site['{}_time'.format(m_name)]))
                    travel_home = timedelta(minutes=int(
                        np.random.choice(self.config['t_bw_sites'])))
                    if (projected_end_time + travel_home) > self.allowed_end_time:
                        # There's not enough time left for that site today
                        # - get started and figure out how much time remains
                        minutes_remaining = (
                            projected_end_time - self.allowed_end_time).total_seconds()/60
                        self.rollover = []
                        self.rollover.append(site)
                        self.rollover.append(minutes_remaining)
                        self.state['t'].current_date = self.allowed_end_time

                    # There's enough time left in the day for this site
                    elif (projected_end_time + travel_home) <= self.allowed_end_time:
                        self.visit_site(site, travel_time)
                    self.worked_today = True

        if self.worked_today:
            self.timeseries['{}_cost'.format(m_name)][self.state['t'].current_timestep] += \
                self.config['cost_per_day']
            self.timeseries['total_daily_cost'][self.state['t'].current_timestep] += \
                self.config['cost_per_day']

        return
    # -------------------------------
