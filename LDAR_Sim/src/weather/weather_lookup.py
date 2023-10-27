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
    def __init__(self, state, virtual_world, input_directory):
        """
        Read in NetCDF files and returns the environment at a given place in time.
        """
        self.state = state
        self.virtual_world = virtual_world

        # Read in weather data as NetCDF file(s)

        self.weather_data = Dataset(
            input_directory / self.virtual_world["weather_file"], "r"
        )  # Load wind and temp data
        self.weather_data.set_auto_mask(False)  # Load wind and temp data
        # Extract temperatures
        self.temps = np.array(self.weather_data.variables["t2m"])
        # Convert to degrees Celcius (time, lat, long)
        self.temps = self.temps - 273.15
        # Extract u wind component
        self.u_wind = np.array(self.weather_data.variables["u10"])
        # Extract v wind component
        self.v_wind = np.array(self.weather_data.variables["v10"])
        self.winds = np.add(
            np.square(self.u_wind), np.square(self.v_wind)
        )  # Calculate the net wind speed
        # Calculate the net wind speed (time, lat, long)
        self.winds = np.sqrt(self.winds.astype(float))
        # Extract precipitation values (time, lat, long)
        self.precip = np.array(self.weather_data.variables["tp"])
        self.precip = self.precip * 1000  # Convert m to mm (time, lat, long)

        # Extract time values
        self.time_total = self.weather_data.variables["time"][:]
        # Extract latitude values
        self.latitude = self.weather_data.variables["latitude"][:]
        # Extract longitude values
        self.longitude = self.weather_data.variables["longitude"][:]
        # Length of time dimension - number of timesteps
        self.time_length = len(self.time_total)
        # Length of latitude dimension - n cells
        self.lat_length = len(self.latitude)
        # Length of longitude dimension - n cells
        self.lon_length = len(self.longitude)

        self.weather_data.close()  # close the netCDF4 file

        return

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
