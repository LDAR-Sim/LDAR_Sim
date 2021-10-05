# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Satellite crew
# Purpose:     Initialize each satellite under the satellite company
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
import random
from generic_functions import quick_cal_daylight, init_orbit_poly, geo_idx
from orbit_predictor.sources import get_predictor_from_tle_lines
import netCDF4 as nc
from shapely.geometry import Point
from shapely import speedups


speedups.disable()


class satellite:
    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        """
        Constructs an individual satellite based on defined configuration.
        """
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.deployment_days = deployment_days
        self.satstate = {'id': id}  # satstate is unique to this agent
        self.worked_today = False

        # read cloud cover data
        input_directory = self.parameters['input_directory']
        cloud = self.parameters['weather_file']
        Dataset = nc.Dataset(input_directory / cloud, 'r')
        self.cloudcover = Dataset.variables['tcc'][:]
        Dataset.close()

        # build a satellite orbit object
        sat = self.config['satellite_name']
        tlefile = self.config['TLE_files']
        TLEs = []
        with open(input_directory / tlefile) as f:
            for line in f:
                TLEs.append(line.rstrip())
        i = 0
        for x in TLEs:
            if x == sat:
                break
            i += 1
        TLE_LINES = (TLEs[i+1], TLEs[i+2])

        self.predictor = get_predictor_from_tle_lines(TLE_LINES)

        # initiate the orbit path by using bulding satellite predictor
        T1 = self.state['t'].start_date
        T2 = self.state['t'].end_date

        # calculate the orbit path polygon for satellite
        self.sat_datetime, self.orbit_path = init_orbit_poly(
            self.predictor, T1, T2, 15)

        self.sat_date = [d.date() for d in self.sat_datetime]

        self.sat_date = np.array(self.sat_date)
        self.orbit_path = np.array(self.orbit_path)

        return

    def work_a_day(self, candidate_flags):
        """
        Go to work and find the leaks for a given day.
        """
        self.worked_today = True
        self.candidate_flags = candidate_flags
        # satellites work 24 days an hour, but need to check daylight
        # at the site every timestep if daylight matters to the satellite.

        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=1)  # Set the start of work day
        while self.state['t'].current_date.hour < 24:
            # find a site
            facility_ID, found_site, site = self.choose_site()
            if not found_site:
                break  # Break out if no site can be found
            self.visit_site(facility_ID, site)

        if self.worked_today:
            self.timeseries['satellite_cost'][self.state['t'].current_timestep] += \
                self.config['cost']['per_day']

        return

    def calc_viewable_sites(self):
        """Generic utility function to check whether a satellite can see
           a given patch of ground. Returns True to denote the satellite
           can see the location and False otherwise.
           Args:
               site: a site

           Returns:
               valid_site: boolean
        """
        valid_site_indices = []
        # ind = 0

        site = self.state['sites']
        sat_date = self.sat_date
        path = self.orbit_path
        date = self.state['t'].current_date.date()
        # find daily pathes
        DP = path[sat_date == date]
        for s in site:
            fac_lat = np.float16(s['lat'])
            fac_lon = np.float16(s['lon'])
            PT = Point(fac_lon, fac_lat)
            check = False
            for dp in DP:
                if dp.contains(PT):
                    check = True
                    break
            valid_site_indices.append(check)

        return (valid_site_indices)

    def assess_weather(self, site):
        """Check whether the site is covered by clound or have enough daylight
            Args:
             site: a site

            Returns:
                valid_site: boolean
        """
        # obtain the geo index of site
        site_lat = np.float16(site['lat'])
        site_lon = np.float16(site['lon'])
        lat_idx = geo_idx(site_lat, self.state['weather'].latitude)
        lon_idx = geo_idx(site_lon, self.state['weather'].longitude)
        ti = self.state['t'].current_timestep

        # check daylight
        date = self.state['t'].current_date
        sr, ss = quick_cal_daylight(date, site_lat, site_lon)

        if sr <= self.state['t'].current_date.hour <= ss:
            sat_daylight = True
        else:
            sat_daylight = False

        # check cloud cover
        CC = self.cloudcover[ti, lat_idx, lon_idx] * 100
        CC = round(CC)
        # cloud cover is a value that represent the proportion of
        # a grid cell covered by cloud
        arr = np.zeros(100)
        arr[:CC] = 1
        # based on the cloud cover, we do a binoary random sample (0 or 1)
        # to determine whether the site is covered by clound in the cell
        np.random.shuffle(arr)
        if np.random.choice(arr, 1)[0] == 0:
            sat_cc = True
        else:
            sat_cc = False

        return (sat_daylight, sat_cc)

    def check_detection(self, site, site_cum_rate):
        """
        Function to check detection on the site scale
        site_cum_rate: the real cumulative emissions rate from the site
        """
        # obtain the geo index of site
        site_lat = np.float16(site['lat'])
        site_lon = np.float16(site['lon'])
        lat_idx = geo_idx(site_lat, self.state['weather'].latitude)
        lon_idx = geo_idx(site_lon, self.state['weather'].longitude)
        windspeed = self.state['weather'].winds

        ti = self.state['t'].current_timestep
        U = windspeed[ti, lat_idx, lon_idx]
        Q_min = 5.79 * (1.39/U)
        # set MDL to 0 for testing
        # Q_min = 0

        return (site_cum_rate > Q_min)

    def quantify(self, site_cum_rate):
        """
        Function to perform synthetic quantification of the site
        """
        sigma = random.choice([0.01, 0.02, 0.03, 0.04, 0.05])
        quantification = site_cum_rate * (1 - sigma)
        return (quantification)

    def choose_site(self):
        """
        Choose a site to survey.
        """
        # Sort all sites based on a neglect ranking
        self.state['sites'] = sorted(
            self.state['sites'],
            key=lambda k: k['satellite_t_since_last_LDAR'],
            reverse=True)

        # determine the viewable sites
        in_view_indices = self.calc_viewable_sites()

        facility_ID = None  # The facility ID gets assigned if a site is found
        found_site = False  # The found site flag is updated if a site is found

        # Then, starting with the most neglected site,
        # check if conditions are suitable for LDAR
        for i, site in enumerate(self.state['sites']):

            # Check if the site is viewable
            if in_view_indices[i]:

                # If the site hasn't been attempted yet today
                if not site['attempted_today_satellite?']:

                    # If the site hasn't met the minimum interval
                    # break out - no LDAR today
                    if site['satellite_t_since_last_LDAR'] < self.config['min_interval']:
                        self.state['t'].current_date = self.state['t'].current_date.replace(
                            hour=23)
                        break

                    # Else if site-specific required visits haven't
                    # been met for the year
                    elif site['surveys_done_this_year_satellite'] < int(site['satellite_RS']):
                        # Check the weather for that site
                        if not self.parameters['consider_weather'] or self.assess_weather(site):
                            # The site passes all the tests! Choose it!
                            facility_ID = site['facility_ID']
                            found_site = True
                            # Update site
                            site['satellite_surveys_conducted'] += 1
                            site['surveys_done_this_year_satellite'] += 1
                            site['satellite_t_since_last_LDAR'] = 0
                            break

                        else:
                            site['attempted_today_satellite?'] = True

        return (facility_ID, found_site, site)

    def visit_site(self, facility_ID, site):
        """
        Look for emissions at the chosen site.
        """
        # Sum all the emissions at the site
        leaks_present = []
        site_cum_rate = 0
        for leak in self.state['leaks']:
            if leak['facility_ID'] == facility_ID:
                if leak['status'] == 'active':
                    leaks_present.append(leak)
                    site_cum_rate += leak['rate']

        # Add vented emissions
        venting = 0
        if self.parameters['emissions']['consider_venting']:
            venting = self.state['empirical_vents'][np.random.randint(
                0, len(self.state['empirical_vents']))]
            site_cum_rate += venting

        # Check detection
        if self.check_detection(site, site_cum_rate):

            # quantify emissions
            QE = self.quantify(site_cum_rate)
            if QE > self.config['follow_up']['thresh']:
                flag_site = True
            else:
                flag_site = False

            # Flag the site if conditions for flagging are met
            if flag_site:

                # Put all necessary information in a dictionary
                site_dict = {
                    'site': site,
                    'leaks_present': leaks_present,
                    'site_measured_rate': QE,
                    'site_true_rate': site_cum_rate,
                    'venting': venting
                }

                self.candidate_flags.append(site_dict)
        else:
            site['satellite_missed_leaks'] += len(leaks_present)

        # Currently, we assume satellite surveys a facility instantaneously
        # self.state['t'].current_date += timedelta(minutes=int(site['satellite_time']))
        self.timeseries['satellite_sites_visited'][self.state['t'].current_timestep] += 1

        return
