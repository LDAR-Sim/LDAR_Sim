# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Daylight calculator
# Purpose:     Calculates daylight hours (daily) for a set of locations.
#
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

import datetime

import ephem
import numpy as np


# Calculate the study area average daylight for each day of the simulation
class DaylightCalculatorAve:
    def __init__(self, state, parameters):
        self.state = state
        self.parameters = parameters

        # Get average lat and lon values for the sites in your study area
        lat_list = []
        lon_list = []
        for site in self.state["sites"]:
            lat_list.append(float(site["lat"]))
            lon_list.append(float(site["lon"]))
        self.lat_ave = np.mean(lat_list)
        self.lon_ave = np.mean(lon_list)

        # Build vector of dates spanning timeseries with format "yyyy/mm/dd"
        self.date_list = [
            self.state["t"].start_date + datetime.timedelta(days=x)
            for x in range(0, self.parameters["timesteps"])
        ]

        # Create an empty list to store the daylight hours - rounding down.
        self.daylight_hours = []

        for day in range(len(self.date_list)):
            # Create ephem object
            obs = ephem.Observer()
            # Turn off PyEphem’s native mechanism for computing atmospheric refraction
            # near the horizon
            obs.pressure = 0
            obs.horizon = "-6"  # -6 = civil twilight, -12 = nautical, -18 = astronomical
            # Set the time
            obs.date = self.date_list[day]
            # set the latitude and longitude for object
            obs.lat = str(self.lat_ave)
            obs.lon = str(self.lon_ave)

            # get the sunset and sunrise UTC time
            sunrise = obs.previous_rising(ephem.Sun(), use_center=True).datetime()
            sunset = obs.next_setting(ephem.Sun(), use_center=True).datetime()
            dif_hours = (sunset - sunrise).total_seconds() / 3600
            self.daylight_hours.append(dif_hours)
        return

    def get_daylight(self, timestep):
        daylight = self.daylight_hours[timestep]
        return daylight


# -----------------------------------------------------------------------------#
class DaylightCalculatorAll:
    def __init__(self, latitude, longitude, date):
        self.time = date
        self.lat = latitude
        self.lon = longitude

        # create an empty array to store the daylight hours
        self.sunrise = np.empty((len(self.time), len(self.lat), len(self.lon)), dtype=np.float)
        self.sunset = np.empty((len(self.time), len(self.lat), len(self.lon)), dtype=np.float)

        for i in range(len(self.time)):
            # Create ephem object
            obs = ephem.Observer()
            # turn off PyEphem’s native mechanism for computing atmospheric refraction
            # near the horizon
            obs.pressure = 0
            obs.horizon = "-6"  # -6=civil twilight, -12=nautical, -18=astronomical
            # set the time
            obs.date = self.time[i]
            # set the latitude and longitude for object
            for j in range(len(self.lat)):
                obs.lat = str(self.lat[j])
                for k in range(len(self.lon)):
                    obs.lon = str(self.lon[k])

                    # get the sunset and sunrise UTC time
                    sunrise = obs.previous_rising(ephem.Sun(), use_center=True).datetime()
                    sunset = obs.next_setting(ephem.Sun(), use_center=True).datetime()

                    # convert to local time
                    sr = (sunrise.hour - 7) + (sunrise.minute / 100)
                    ss = (sunset.hour + 17) + (sunset.minute / 100)

                    self.sunrise[i, j, k] = sr
                    self.sunset[i, j, k] = ss

    def get_sunrise(self, day, lat, lon):
        # find latitude index
        tar_la = lat
        lat_index = 0
        i = 1
        while i < len(self.lat):
            if self.lat[i - 1] > tar_la >= self.lat[i]:
                lat_index = i
            i = i + 1
        self.tar_lo = lon
        # find longitude index
        lon_index = 0
        j = 1
        while j < len(self.lon):
            if self.lon[j - 1] > tar_la >= self.lon[j]:
                lon_index = j
            j = j + 1

            # find time index
        k = 0
        for d in np.arange(len(self.time)):
            if d == day:
                d_index = k
            k = k + 1

        self.sr = self.sunrise[d_index, lat_index, lon_index]
        return self.sr

    def get_sunset(self, day, lat, lon):
        # find latitude index
        tar_la = lat
        lat_index = 0
        i = 1
        while i < len(self.lat):
            if self.lat[i - 1] > tar_la >= self.lat[i]:
                lat_index = i
            i = i + 1
        self.tar_lo = lon
        # find longitude index
        lon_index = 0
        j = 1
        while j < len(self.lon):
            if self.lon[j - 1] > tar_la >= self.lon[j]:
                lon_index = j
            j = j + 1

            # find time index
        k = 0
        for d in np.arange(len(self.time)):
            if day == d + 1:
                d_index = k
            k = k + 1

        self.ss = self.sunset[d_index, lat_index, lon_index]
        return self.ss
