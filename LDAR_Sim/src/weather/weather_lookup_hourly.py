# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Weather lookup hourly
# Purpose:     Calculate deployment days for a method
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

from netCDF4 import Dataset
import numpy as np
from datetime import date,  timedelta as tdelt, datetime as dt


class WeatherLookup:
    def __init__(self, state, parameters):
        """
        Read in NetCDF files and returns the environment at a given place in time.

        """
        self.state = state
        self.parameters = parameters

        # Read in weather data as NetCDF file(s)

        self.weather_data = Dataset(
            self.parameters['input_directory'] / self.parameters['weather_file'],
            'r')  # Load wind and temp data
        self.weather_data.set_auto_mask(False)
        self.time_total = self.weather_data.variables['time'][:]  # Extract time values
        self.weather_time_meta = {}
        # Get start and end date of weather data. (Time is hours since Jan1, 1900)
        start_date = dt(1900, 1, 1) + \
            tdelt(hours=int(self.time_total[0]))
        end_date = dt(1900, 1, 1) + \
            tdelt(hours=int(self.time_total[-1]))
        add_year = (end_date.month == 12) and (end_date.day == 31)
        num_years = end_date.year - start_date.year + add_year
        #  Go Through All years and Extract Metadata
        for year_delta in range(num_years):
            year = start_date.year + year_delta
            try:
                date(year, 2, 29)
                leap_year = True
            except ValueError:
                leap_year = False
            hrs_srt = (dt(year, 1, 1) - dt(1900, 1, 1)).days*24
            hrs_stp = (dt(year, 12, 31) - dt(1900, 1, 1)).days*24
            hrs_stp += 23
            self.weather_time_meta[year_delta] = {
                "year": year,
                "start_hr": hrs_srt,
                "stop_hr": hrs_stp,
                "leap_year": leap_year,
                "note": "hours since Jan 1, 1900"}
        self.temps = np.array(self.weather_data.variables['t2m'])  # Extract temperatures
        self.temps = self.temps - 273.15  # Convert to degrees Celcius (time, lat, long)
        self.u_wind = np.array(self.weather_data.variables['u10'])  # Extract u wind component
        self.v_wind = np.array(self.weather_data.variables['v10'])  # Extract v wind component
        self.winds = np.add(np.square(self.u_wind), np.square(
            self.v_wind))  # Calculate the net wind speed
        # Calculate the net wind speed (time, lat, long)
        self.winds = np.sqrt(self.winds.astype(float))
        # Extract precipitation values (time, lat, long)
        self.precip = np.array(self.weather_data.variables['tp'])
        self.precip = self.precip * 1000  # Convert m to mm (time, lat, long)
        self.latitude = self.weather_data.variables['latitude'][:]  # Extract latitude values
        self.longitude = self.weather_data.variables['longitude'][:]  # Extract longitude values
        self.weather_data.close()  # close the netCDF4 file
        return

    def deployment_days(self, method_name, config, start_date, start_work_hour=0,
                        consider_weather=True):
        """Generate a matrix with dimensions [num_lngs, num_lats, num_days]
        With each element being a boolean representing if the weather is
        suitable for surveying  (1 being ok).

        Args:
            method (string): LDAR Method ie. "OGI"
            start_date (date): Start day of Program
            consider_weather (Boolean): Ignore weather if false
                    returns all ones

        Returns:
            boolean Matrix: See Summary for description
        """

        # Initialize empty boolean arrays for threshold pass(1)/fail(0)
        bool_temp = np.zeros((len(self.longitude), len(
            self.latitude), self.parameters['timesteps']))
        bool_wind = np.zeros((len(self.longitude), len(
            self.latitude), self.parameters['timesteps']))
        bool_precip = np.zeros((len(self.longitude), len(
            self.latitude), self.parameters['timesteps']))

        # For each day...
        for day in range(self.parameters['timesteps']):
            start_dt = dt(start_date.year,
                          start_date.month,
                          start_date.day,
                          start_work_hour, 0)
            nday_dt = start_dt + tdelt(days=day)
            if 'max_workday' in config:
                max_day = config['max_workday']
            else:
                max_day = 23
                # Count DDs for each criteria
            for lat in range(len(self.latitude)):
                for lon in range(len(self.longitude)):
                    # If you exceed minimum temperature...
                    if consider_weather:
                        hr_weather = self.get_hourly_weather(
                            ['winds', 'precip', 'temps'],
                            nday_dt, number_of_hours=max_day,
                            lat_idx=lat, lon_idx=lon)
                        if config['weather_envs']['temp'][0] <= np.average(hr_weather['temps']) \
                                <= config['weather_envs']['temp'][1]:
                            # Count one instrument day (instrument can be used)
                            bool_temp[lon, lat, day] = 1
                        # If you are below the maximum wind...
                        if config['weather_envs']['wind'][0] <= np.average(hr_weather['winds']) \
                                <= config['weather_envs']['wind'][1]:
                            # Count one instrument day (instrument can be used)
                            bool_wind[lon, lat, day] = 1
                        # If you are below the precipitation threshold...
                        if config['weather_envs']['precip'][0] <= np.average(hr_weather['precip']) \
                                <= config['weather_envs']['precip'][1]:
                            # Count one instrument day (instrument can be used)
                            bool_precip[lon, lat, day] = 1
                    else:
                        bool_temp[lon, lat, day] = 1
                        bool_wind[lon, lat, day] = 1
                        bool_precip[lon, lat, day] = 1

                        # Check to see if all criteria (temp, wind, and precip) were met...
        bool_sum = np.add(bool_temp, np.add(bool_wind, bool_precip))
        DD_all = bool_sum == 3
        return DD_all

    def get_hourly_weather(self, weather_vars, start_datetime, number_of_hours=24,
                           site=None, lat_idx=None, lon_idx=None, lat=None, lon=None):
        """Retrieve Hourly Data within a day specified either at a site with
        lat_index and lng_index or with provided lat_idx lon_idx.

        Args:
            weather_vars (list of strings): LIsts of vars ['winds, 'temp', 'precip']
            start_datetime (datetime): Start of Program Datetime
            number_of_hours (int, optional): Number of consecutive hours to return. Defaults to 24.
            site (dict, optional): location with lat_index and lng_index. Defaults to None.
            lat_idx (integer, optional): index in matrix. Defaults to None.
            lon_idx (integer, optional): index in matrix. Defaults to None.
            lat (float, optional): specify latitude. Defaults to None.
            lon (float, optional): specify longitude. Defaults to None.

        Returns:
            dict: of weather data lists : {winds:[5,2,3,4],temps[-10,10,3,4]}
        """
        def find_nearest(value, array):
            array = np.asarray(array)
            return (np.abs(array - value)).argmin()

        if site:
            # Get Site latitude and longitude index
            lat_idx = site['lat_index']
            lon_idx = site['lon_index']
        elif lat and lon:
            # if a lat and logitude are provide find closes
            lat_idx = find_nearest(lat, self.latitude)
            lon_idx = find_nearest(lon, self.longitude)

        # Weather data is in timesteps since Jan 1 , 1900 UTC, the following
        # gets the current date in timesteps since Jan 1, 1900 UTC.
        date_UTC = start_datetime - tdelt(hours=self.state['t'].UTC_offset)
        dtime_s1900_UTC = date_UTC - dt(1900, 1, 1, 0, 0)
        hrs_s1900_UTC = int(dtime_s1900_UTC.days*24 +
                            np.floor(dtime_s1900_UTC.seconds/3600))
        start_hr_s1900_UTC = self.weather_time_meta[0]['start_hr']
        # Get the index (of the weather data array) for the start hour and endhour
        # (start hour + workhours) for the day
        cur_day_srt_idx = int(hrs_s1900_UTC - start_hr_s1900_UTC)
        cur_day_stp_idx = int(cur_day_srt_idx + number_of_hours)

        # could be used The following will "rollover" the weather data so the start and stop
        # Hours happen at the same time on the same julian date (potentially on a different year).
        # For example if the weather data goes from 2017-2020, and the current day is January 1st
        # 2021, the weather for Jan 1st 2017 will be used.

        # HBD , does not account for Leap year self.weather_time_meta has leap year info and
        while cur_day_srt_idx < 0:
            cur_day_srt_idx += len(self.winds)
        while cur_day_stp_idx < 0:
            cur_day_stp_idx += len(self.winds)
        while cur_day_srt_idx > len(self.winds):
            cur_day_srt_idx -= len(self.winds)
        while cur_day_stp_idx > len(self.winds):
            cur_day_stp_idx -= len(self.winds)
        out_weather = {}

        # For
        for weather_var in weather_vars:
            data_set = self.__getattribute__(weather_var)
            if cur_day_stp_idx > cur_day_srt_idx:
                hrly_weather_day = data_set[cur_day_srt_idx:cur_day_stp_idx,
                                            lat_idx, lon_idx]
            else:
                # Due to rollover the start index can occur later than
                # than the end index. For example if the weather data goes from
                # 2017-2020, the start time is December 31st 2020 20:00 UTC, and the
                # end of day time is Jan 1st 2021 1:00 UTC, then the Start index will
                # be larger than the end index, because the the end index will be pointing
                # at Jan 1st 2017 1:00 UTC.
                hrly_weather_day_1 = data_set[cur_day_srt_idx:,
                                              lat_idx, lon_idx]
                hrly_weather_day_2 = data_set[: cur_day_stp_idx,
                                              lat_idx, lon_idx]
                hrly_weather_day = np.concatenate((hrly_weather_day_1, hrly_weather_day_2))
            out_weather[weather_var] = hrly_weather_day
        return out_weather
