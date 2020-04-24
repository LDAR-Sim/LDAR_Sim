#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Weather lookup
# Purpose:     Calculate deployment days for a method
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#------------------------------------------------------------------------------

from netCDF4 import Dataset
import numpy as np

class weather_lookup:
    def __init__ (self, state, parameters):
        '''
        Read in NetCDF files and returns the environment at a given place in time.

        '''
        print('Initializing weather...')
        self.state = state
        self.parameters = parameters

        # Read in weather data as NetCDF file(s)

        self.wind_temp_data = Dataset(self.parameters['an_data'])                 # Load wind and temp data
        self.wind_temp_data.set_auto_mask(False)                                  # Load wind and temp data
        self.precip_data = Dataset(self.parameters['fc_data'])                    # Load precip data
        self.precip_data.set_auto_mask(False)                                     # Load precip data
        self.temps = np.array(self.wind_temp_data.variables['t2m'])               # Extract temperatures
        self.temps = self.temps - 273.15                                          # Convert to degrees Celcius (time, lat, long)
        self.u_wind = np.array(self.wind_temp_data.variables['u10'])              # Extract u wind component
        self.v_wind = np.array(self.wind_temp_data.variables['v10'])              # Extract v wind component
        self.winds = np.add(np.square(self.u_wind), np.square(self.v_wind))       # Calculate the net wind speed
        self.winds = np.sqrt(self.winds.astype(float))                            # Calculate the net wind speed (time, lat, long)
        self.precip = np.array(self.precip_data.variables['tp'])                  # Extract precipitation values (time, lat, long)

        self.time_total = self.wind_temp_data.variables['time'][:]                # Extract time values
        self.latitude = self.wind_temp_data.variables['latitude'][:]              # Extract latitude values
        self.longitude = self.wind_temp_data.variables['longitude'][:]            # Extract longitude values
        self.time_length = len(self.wind_temp_data.variables['time'])             # Length of time dimension - number of timesteps
        self.lat_length = len(self.wind_temp_data.variables['latitude'])          # Length of latitude dimension - number of cells
        self.lon_length = len(self.wind_temp_data.variables['longitude'])         # Length of longitude dimension - number of cells

        return

    def deployment_days (self, method):
        '''
        Generate a 3D space-time matrix of all days on which weather
        conditions are suitable for a given method to conduct LDAR.
        
        Should only be called once/method during initialization.
        
        DD = deployment day
        '''

        # Initialize empty boolean arrays for threshold pass(1)/fail(0)
        bool_temp = np.zeros((self.lon_length, self.lat_length, self.parameters['timesteps']))
        bool_wind = np.zeros((self.lon_length, self.lat_length, self.parameters['timesteps']))
        bool_precip = np.zeros((self.lon_length, self.lat_length, self.parameters['timesteps']))
    
        # For each day...
        for day in range(self.parameters['timesteps']):
            
            # Count DDs for each criteria
            for lat in range(self.lat_length):
                for lon in range(self.lon_length):
                    # If you exceed minimum temperature...
                    if self.temps[day, lat, lon] >= self.parameters['methods'][method]['min_temp']:       
                        bool_temp[lon, lat, day] = 1       # Count one instrument day (instrument can be used)
                    # If you are below the maximum wind...
                    if self.winds[day, lat, lon] <= self.parameters['methods'][method]['max_wind']:       
                        bool_wind[lon, lat, day] = 1        # Count one instrument day (instrument can be used)
                    # If you are below the precipitation threshold...
                    if self.precip[day, lat, lon] <= self.parameters['methods'][method]['max_precip']:         
                        bool_precip[lon, lat, day] = 1      # Count one instrument day (instrument can be used)
    
        # Check to see if all criteria (temp, wind, and precip) were met...
        bool_sum = np.add(bool_temp, np.add(bool_wind, bool_precip))
        DD_all = bool_sum == 3

        return (DD_all)
