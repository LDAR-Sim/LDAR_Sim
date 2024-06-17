# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Weather lookup
# Purpose:     Calculate deployment days for a method
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

import numpy as np
from netCDF4 import Dataset


class WeatherLookup:
    def __init__(self, virtual_world, input_directory):
        """
        Read in NetCDF files and returns the environment at a given place in time.
        """
        # Initialize attributes to store weather data
        self.temps = None
        self.u_wind = None
        self.v_wind = None
        self.winds = None
        self.precip = None
        self.time_total = None
        self.latitude = None
        self.longitude = None
        self.time_length = None
        self.lat_length = None
        self.lon_length = None

        # Load weather data
        self.load_weather_data(virtual_world, input_directory)

    def load_weather_data(self, virtual_world, in_dir):
        # Read in weather data as NetCDF file(s)
        with Dataset(in_dir / virtual_world["weather_file"], "r") as weather_data:
            # Extract temperatures
            self.temps = np.array(weather_data.variables["t2m"]) - 273.15
            # Extract u wind component
            self.u_wind = np.array(weather_data.variables["u10"])
            # Extract v wind component
            self.v_wind = np.array(weather_data.variables["v10"])
            # Calculate the net wind speed
            self.winds = np.sqrt(np.square(self.u_wind) + np.square(self.v_wind))
            # Extract precipitation values and convert to mm
            self.precip = np.array(weather_data.variables["tp"]) * 1000
            # Extract time values
            self.time_total = weather_data.variables["time"][:]
            # Extract latitude values
            self.latitude = weather_data.variables["latitude"][:]
            # Extract longitude values
            self.longitude = weather_data.variables["longitude"][:]

            self.lat_sort = np.argsort(self.latitude, kind="mergesort")
            self.lon_sort = np.argsort(self.longitude, kind="mergesort")

            self.latitude = self.latitude[self.lat_sort]
            self.longitude = self.longitude[self.lon_sort]

            # Length of time dimension - number of timesteps
            self.time_length = len(self.time_total)
            # Length of latitude dimension - n cells
            self.lat_length = len(self.latitude)
            # Length of longitude dimension - n cells
            self.lon_length = len(self.longitude)

    def __reduce__(self):
        args = (
            self.temps,
            self.u_wind,
            self.v_wind,
            self.winds,
            self.precip,
            self.time_total,
            self.latitude,
            self.longitude,
            self.time_length,
            self.lat_length,
            self.lon_length,
        )
        return (self.__class__._reconstruct, args)

    @classmethod
    def _reconstruct(
        cls,
        temps,
        u_wind,
        v_wind,
        winds,
        precip,
        time_total,
        latitude,
        longitude,
        time_length,
        lat_length,
        lon_length,
    ):
        # Create a new instance without invoking __init__
        instance = cls.__new__(cls)
        instance.temps = temps
        instance.u_wind = u_wind
        instance.v_wind = v_wind
        instance.winds = winds
        instance.precip = precip
        instance.time_total = time_total
        instance.latitude = latitude
        instance.longitude = longitude
        instance.time_length = time_length
        instance.lat_length = lat_length
        instance.lon_length = lon_length
        return instance

    def deployment_days(
        self, method_name, config, start_date, start_work_hour=0, consider_weather=False
    ):
        """
        Generate a 3D space-time matrix of all days on which weather
        conditions are suitable for a given method to conduct LDAR.
        Should only be called once/method during initialization.
        DD = deployment day
        """

        # Initialize empty boolean arrays for threshold pass(1)/fail(0)
        bool_temp = np.zeros((self.lon_length, self.lat_length, self.virtual_world["timesteps"]))
        bool_wind = np.zeros((self.lon_length, self.lat_length, self.virtual_world["timesteps"]))
        bool_precip = np.zeros((self.lon_length, self.lat_length, self.virtual_world["timesteps"]))

        # For each day...
        for day in range(self.virtual_world["timesteps"]):
            # Count DDs for each criteria
            for lat in range(self.lat_length):
                for lon in range(self.lon_length):
                    # Check daily weather variables are within method range
                    if (
                        config["weather_envs"]["temp"][0]
                        <= self.temps[day, lat, lon]
                        <= config["weather_envs"]["temp"][1]
                    ):
                        bool_temp[lon, lat, day] = 1
                    if (
                        config["weather_envs"]["wind"][0]
                        <= self.winds[day, lat, lon]
                        <= config["weather_envs"]["wind"][1]
                    ):
                        bool_wind[lon, lat, day] = 1
                    if (
                        config["weather_envs"]["precip"][0]
                        <= self.precip[day, lat, lon]
                        <= config["weather_envs"]["precip"][1]
                    ):
                        bool_precip[lon, lat, day] = 1

        # Check to see if all criteria (temp, wind, and precip) were met...
        bool_sum = np.add(bool_temp, np.add(bool_wind, bool_precip))
        DD_all = bool_sum == 3

        return DD_all
