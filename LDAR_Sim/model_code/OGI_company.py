#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        OGI company
# Purpose:     Company managing OGI agents.
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

from OGI_crew import *
from weather_lookup import *
from generic_functions import gap_calculator
import numpy as np
import os
from osgeo import gdal
from osgeo import osr

class OGI_company:
    def __init__ (self, state, parameters, config, timeseries):
        '''
        Initialize a company to manage the OGI crews (e.g. a contracting company).

        '''
        print('Initializing OGI company...')
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days('OGI')
        self.timeseries['OGI_prop_sites_avail'] = []
        self.timeseries['OGI_cost'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['OGI_redund_tags'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['OGI_sites_visited'] = np.zeros(self.parameters['timesteps'])
 
        # Additional variable(s) for each site       
        for site in self.state['sites']:
            site.update( {'OGI_t_since_last_LDAR': 0})
            site.update( {'OGI_surveys_conducted': 0})
            site.update( {'attempted_today_OGI?': False})
            site.update( {'surveys_done_this_year_OGI': 0})
            site.update( {'OGI_missed_leaks': 0})
            
        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_OGI_map = np.zeros((len(self.state['weather'].longitude), len(self.state['weather'].latitude)))
        self.MCB_OGI_map = np.zeros((len(self.state['weather'].longitude), len(self.state['weather'].latitude)))
        
        # Initialize the individual OGI crews (the agents)
        for i in range (config['n_crews']):
            self.crews.append (OGI_crew (state, parameters, config, timeseries, self.deployment_days, id = i + 1))

        return

    def find_leaks (self):
        '''
        The OGI company tells all the crews to get to work.
        '''

        for i in self.crews:
            i.work_a_day ()

        # Update method-specific site variables each day
        for site in self.state['sites']:
            site['OGI_t_since_last_LDAR'] += 1
            site['attempted_today_OGI?'] = False
            
        if self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
            for site in self.state['sites']:
                site['surveys_done_this_year_OGI'] = 0
                
        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                available_sites += 1
        prop_avail = available_sites/len(self.state['sites'])
        self.timeseries['OGI_prop_sites_avail'].append(prop_avail) 
            
        return
    
    def make_maps (self):
        '''
        If requested, makes maps of proportion of timesteps that are deployment days.
        Also outputs a map of MCB (maximum condition blackout) over period of analysis.
        '''
        
        print('Generating OGI maps...')

        # For each cell, sum the total number of deployment days and divide by total number of days        
        for lon in range(len(self.state['weather'].longitude)):
            for lat in range(len(self.state['weather'].latitude)):
                self.DD_OGI_map[lon, lat] = (self.deployment_days[lon, lat, :].sum())/self.parameters['timesteps']
        
        # Calculate MCB for each cell
        for lon in range(len(self.state['weather'].longitude)):
            for lat in range(len(self.state['weather'].latitude)):
                self.MCB_OGI_map[lon, lat] = gap_calculator(self.deployment_days[lon, lat, :])
                
        # Set variables necessary for writing map files
        DD_OGI_output = np.swapaxes (self.DD_OGI_map, axis1 = 0, axis2 = 1)
        MCB_OGI_output = np.swapaxes (self.MCB_OGI_map, axis1 = 0, axis2 = 1)
        lon, lat = self.state['weather'].longitude, self.state['weather'].latitude
        xmin,ymin,xmax,ymax = [lon.min(),lat.min(),lon.max(),lat.max()]
        nrows, ncols = np.shape(DD_OGI_output)
        xres = (xmax-xmin)/float(ncols)
        yres = (ymax-ymin)/float(nrows)
        geotransform = (xmin,xres,0,ymax,0, -yres)

        # Set output directory
        output_directory = os.path.join(self.parameters['working_directory'], self.parameters['output_folder'])
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        os.chdir(output_directory)

        # Export 2D proportions matrix as map
        output_raster = gdal.GetDriverByName('GTiff').Create('DD_OGI_map_' + self.parameters['simulation'] + '.tif', ncols, nrows, 1, gdal.GDT_Float32)
        output_raster.SetGeoTransform(geotransform)              # Specify file coordinates
        srs = osr.SpatialReference()                             # Establish coordinate encoding
        srs.ImportFromEPSG(4326)                                 # Specify WGS84 lat/long
        output_raster.SetProjection(srs.ExportToWkt())           # Exports the coordinate system to the file
        output_raster.GetRasterBand(1).WriteArray(DD_OGI_output)    # Writes my array to the raster
        output_raster = None
        
        # Exprot 2D MCB matrix as map
        output_raster = gdal.GetDriverByName('GTiff').Create('MCB_OGI_map_' + self.parameters['simulation'] + '.tif', ncols, nrows, 1, gdal.GDT_Float32)
        output_raster.SetGeoTransform(geotransform)              # Specify file coordinates
        srs = osr.SpatialReference()                             # Establish coordinate encoding
        srs.ImportFromEPSG(4326)                                 # Specify WGS84 lat/long
        output_raster.SetProjection(srs.ExportToWkt())           # Exports the coordinate system to the file
        output_raster.GetRasterBand(1).WriteArray(MCB_OGI_output)   # Writes my array to the raster
        output_raster = None
              
        return

    def site_reports (self):
        '''
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs) for each site.
        '''
        
        print ('Generating site-level reports for OGI company...')
        
        for site in self.state['sites']:
            site['OGI_prop_DDs'] = self.DD_OGI_map[site['lon_index'], site['lat_index']]
            site['OGI_MCB'] = self.MCB_OGI_map[site['lon_index'], site['lat_index']]
        
        return
            
            