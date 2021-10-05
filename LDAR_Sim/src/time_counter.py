# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Time counter
# Purpose:     Initialize time object and keeps track of simulation time
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

from datetime import datetime, timedelta
from statistics import mean
from timezonefinder import TimezoneFinder
import pytz


class TimeCounter:
    def __init__(self, parameters):
        """
        Initialize a calendar and clock to count through the simulation.

        """
        self.parameters = parameters
        self.start_date = datetime(*parameters['start_date'])
        self.end_date = datetime(*parameters['end_date'])
        self.timesteps = (self.end_date - self.start_date).days
        self.current_date = self.start_date
        self.current_timestep = 0
        return

    def next_day(self):
        """
        Go to the next day in the simulation

        """
        self.current_date += timedelta(days=1)
        self.current_timestep += 1
        return

    def set_UTC_offset(self, sites):
        '''
        set UTC offset based on average site lat longs

        Uses current (now()) offset
        '''
        avg_lat = mean([float(site['lat']) for site in sites])
        avg_lon = mean([float(site['lon']) for site in sites])
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=avg_lon, lat=avg_lat)
        # This uses the current time to estimate offset, so if running
        # software during DST, the the offset will include DST. Fix this
        # someday, by keeping timezone as a site variable and localizing
        # very year.
        tz_now = datetime.now(pytz.timezone(timezone_str))
        self.UTC_offset = tz_now.utcoffset().total_seconds()/60/60
