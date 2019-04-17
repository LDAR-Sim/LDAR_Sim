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
        self.crews = []                         # Empty list of OGI agents (crews)
        self.deployment_days = self.state['weather'].deployment_days('OGI')
        self.timeseries['prop_sites_avail_OGI'] = []
        
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
            
        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'], site['lat_index'], self.state['t'].current_timestep] == True:
                available_sites += 1
        prop_avail = available_sites/len(self.state['sites'])
        self.timeseries['prop_sites_avail_OGI'].append(prop_avail) 
            
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
        output_raster = gdal.GetDriverByName('GTiff').Create('DD_OGI_map.tif', ncols, nrows, 1, gdal.GDT_Float32)
        output_raster.SetGeoTransform(geotransform)              # Specify file coordinates
        srs = osr.SpatialReference()                             # Establish coordinate encoding
        srs.ImportFromEPSG(4326)                                 # Specify WGS84 lat/long
        output_raster.SetProjection(srs.ExportToWkt())           # Exports the coordinate system to the file
        output_raster.GetRasterBand(1).WriteArray(DD_OGI_output)    # Writes my array to the raster
        output_raster = None
        
        # Exprot 2D MCB matrix as map
        output_raster = gdal.GetDriverByName('GTiff').Create('MCB_OGI_map.tif', ncols, nrows, 1, gdal.GDT_Float32)
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
            site['prop_DDs_OGI'] = self.DD_OGI_map[site['lon_index'], site['lat_index']]
            site['MCB_OGI'] = self.MCB_OGI_map[site['lon_index'], site['lat_index']]
        
        return
            
            
            