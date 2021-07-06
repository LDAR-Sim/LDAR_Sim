# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        crew
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

from datetime import timedelta
import numpy as np
from aggregator import aggregate
from method_functions import measured_rate
from geography.homebase import find_homebase, find_homebase_opt
from geography.distance import get_distance


class BaseCrew:
    """
    Base class crew function. Changes made here will affect any inheriting
    classes. To use base class, import and use as argument arguement. ie.

    from methods.base_crew import base_crew
    class crew (base_crew):
        def __init__(self, **kwargs):
            super(crew, self).__init__(**kwargs)
        ...s

    overwrite methods by creating methods in the inheriting class
    after the __init__ function.
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        """
        Constructs an individual crew based on defined configuration.
        """
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.crewstate = {'id': id}
        self.crewstate['lat'] = 0.0
        self.crewstate['lon'] = 0.0
        return

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

    def choose_site(self, crew_x, crew_y):
        """
        Choose a site to survey.

        """
        m_name = self.config['label']
        if self.config['is_follow_up']:
            site_pool = self.state['flags']
        else:
            site_pool = self.state['sites']
        # Sort all sites based on a neglect ranking
        site_pool = sorted(
            site_pool,
            key=lambda k: k['{}_t_since_last_LDAR'.format(m_name)],
            reverse=True)
        site = None
        facility_ID = None  # The facility ID gets assigned if a site is found
        found_site = False  # The found site flag is updated if a site is found
        travel_time = None
        Site_T = []
        s_list = []

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in site_pool:
            s_list.append(site)
            site_x = np.float(site['lon'])
            site_y = np.float(site['lat'])

            # Check to see if the site can be surveyed.
            # If route planning is used the site needs to be assigned to the crew
            if (self.config['scheduling']['route_planning']
                    and site['label'] + 1 == self.crewstate['id']
                    or not self.config['scheduling']['route_planning']):
                if not site['{}_attempted_today?'.format(m_name)]:
                    if self.config['is_follow_up']:
                        is_ready = (self.state['t'].current_date - site['date_flagged']).days \
                            >= self.parameters['methods'][site['flagged_by']]['reporting_delay']
                    else:
                        # If the site is 'unripened' (i.e. hasn't met the minimum interval set
                        # out in the LDAR regulations/policy), break out - no LDAR today
                        if site['{}_t_since_last_LDAR'.format(m_name)]  \
                                < int(site['{}_min_int'.format(m_name)]):
                            self.state['t'].current_date = self.state['t'].current_date.replace(
                                hour=23)
                            break
                        elif site['{}_surveys_done_this_year'.format(m_name)] \
                                < int(site['{}_RS'.format(m_name)]):
                            is_ready = True
                        else:
                            is_ready = False

                    # if the site is ready for survey (schedule, or picked through route planning)
                    if is_ready:
                        # If weather is suitable for crew to survey
                        if self.deployment_days[site['lon_index'],
                                                site['lat_index'],
                                                self.state['t'].current_timestep]:

                            if self.scheduling['geography']:
                                d = get_distance(crew_x, crew_y, site_x, site_y, "Haversine")
                                speed = np.random.choice(self.config['scheduling']['speed_list'])
                                wt = d/speed * 60
                                Site_T.append(wt)
                                # HBD - What happens if there is route planning and geography?
                                if not self.scheduling['route_planning']:
                                    # The site passes all the tests! Choose it!
                                    travel_time = wt
                                    facility_ID = site['facility_ID']
                                    found_site = True
                                    # Update site
                                    site['{}_surveys_conducted'.format(m_name)] += 1
                                    site['{}_surveys_done_this_year'.format(m_name)] += 1
                                    site['{}_t_since_last_LDAR'.format(m_name)] = 0
                                    break
                            else:
                                # The site passes all the tests! Choose it!
                                facility_ID = site['facility_ID']
                                found_site = True
                                travel_time = int(np.random.choice(self.config['t_bw_sites']))
                                # Update site
                                site['{}_surveys_conducted'.format(m_name)] += 1
                                site['{}_surveys_done_this_year'.format(m_name)] += 1
                                site['{}_t_since_last_LDAR'.format(m_name)] = 0
                                break

                        else:
                            site['{}_attempted_today?'.format(m_name)] = True

        if self.scheduling['route_planning']:
            if len(Site_T) > 0:
                j = Site_T.index(min(Site_T))
                site = s_list[j]
                facility_ID = site['facility_ID']
                travel_time = min(Site_T)*60
                found_site = True

                # Update site
                site['{}_surveys_conducted'.format(m_name)] += 1
                site['{}_surveys_done_this_year'.format(m_name)] += 1
                site['{}_t_since_last_LDAR'.format(m_name)] = 0

        return (facility_ID, found_site, site, travel_time)

    def visit_site(self, site, travel_time=None):
        """
        Look for emissions at the chosen site.
        """
        m_name = self.config['label']

        # Aggregate true emissions to equipment and site level; get list of leaks present
        leaks_present, equipment_rates, site_true_rate = aggregate(site, self.state['leaks'])

        # Add vented emissions
        venting = 0
        if self.parameters['consider_venting']:
            venting = self.state['empirical_vents'][
                np.random.randint(0, len(self.state['empirical_vents']))]
        site_true_rate += venting
        for rate in range(len(equipment_rates)):
            equipment_rates[rate] += venting/int(site['equipment_groups'])

        _ = self.detect_emissions(
            site, leaks_present, equipment_rates, site_true_rate, venting)

        # --- Update time ---
        self.state['t'].current_date += timedelta(minutes=int(site['{}_time'.format(m_name)]))
        # if travel time was not generated when choosing site
        if not travel_time:
            travel_time = np.random.choice(self.config['t_bw_sites'])
        self.state['t'].current_date += timedelta(
            minutes=int(travel_time))
        self.timeseries['{}_sites_visited'.format(m_name)][self.state['t'].current_timestep] += 1

        if self.config['is_follow_up']:
            # Remove site from flag pool
            site['currently_flagged'] = False
        return

    def detect_emissions(self, site, leaks_present, equipment_rates, site_true_rate, venting):
        # init vars
        m_name = self.config['label']
        site_measured_rate = 0
        is_leak_detected = False

        if self.config["measurement_scale"] == "site":
            if site_true_rate > (self.config['MDL']):
                # If source is above follow-up threshold, calculate measured rate using QE
                site_measured_rate = measured_rate(site_true_rate, self.config['QE'])
                is_leak_detected = True
        elif self.config["measurement_scale"] == "equipment":
            for rate in equipment_rates:
                if rate > (self.config['MDL']):
                    equip_measured_rate = measured_rate(rate, self.config['QE'])
                    site_measured_rate += equip_measured_rate
                    is_leak_detected = True
        elif self.config["measurement_scale"] == "leak":
            for leak in leaks_present:
                if leak['rate'] > (self.config['MDL']):
                    site_measured_rate += measured_rate(leak['rate'], self.config['QE'])
                    is_leak_detected = True

        # If source is above follow-up threshold
        if site_measured_rate > self.config['follow_up_thresh']:
            # Put all necessary information in a dictionary to be assessed at end of day
            site_dict = {
                'site': site,
                'leaks_present': leaks_present,
                'site_true_rate': site_true_rate,
                'site_measured_rate': site_measured_rate,
                'venting': venting
            }
            self.candidate_flags.append(site_dict)

        else:
            site['{}_missed_leaks'.format(m_name)] += len(leaks_present)

        return is_leak_detected
