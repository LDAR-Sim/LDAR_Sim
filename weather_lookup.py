from netCDF4 import Dataset
import numpy as np

class weatherman:
    def __init__ (self, state, parameters):
        '''
        Read in a NetCDF file and returns the weather at a given place in time.

        '''
        self.state = state
        self.parameters = parameters

        # Read in weather data as NetCDF file(s)

        self.wind_temp_data = Dataset(self.parameters['WT_data'])                 # Load wind and temp data
        self.wind_temp_data.set_auto_mask(False)                                  # Load wind and temp data
        self.precip_data = Dataset(self.parameters['P_data'])                     # Load precip data
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

    def get_weather (self, time, lat, lon):
        '''
        Query the weather for a specific day and place.
        '''

        # Convert the input in decimal degrees to a cell in the grid to query the weather
        lat_index = min(range(len(self.latitude)), key=lambda i: abs(self.latitude[i]-lat))              # Finds the cell latitude index for the point provided
        lon_index = min(range(len(self.longitude)), key=lambda i: abs(self.longitude[i]-lon%360))        # Find lon index. %360 converts longitude from -180 to 180 to 0 to 360 coordinate

        weather = {
                   'temp': self.temps[time, lat_index, lon_index],
                   'precip': self.precip[time, lat_index, lon_index],
                   'wspeed': self.winds[time, lat_index, lon_index]
                   #'wdir': .....
                   #'clouds': .....
                   }
        return (weather)









