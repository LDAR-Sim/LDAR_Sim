# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Generic functions
# Purpose:     Generic functions for running LDAR-Sim.
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
# ------------------------------------------------------------------------------

import numpy as np
import os
from osgeo import gdal
from osgeo import osr

def gap_calculator(condition_vector):
    """
    This function calculates max gaps between daily activites in a time series.
    Requires only a single binary vector describing whether a condition was met.
    """

    # Find the index of all days in which the condition is true
    max_gap = None
    indices = np.where(condition_vector == True)

    # If there are no condition days, max_gap equals the vector length
    if len(indices[0]) == 0:
        max_gap = len(condition_vector)

    # If there is only one condition day, get max_gap
    elif len(indices[0]) == 1:
        start_gap = indices[0][0]
        end_gap = len(condition_vector) - indices[0][0]
        max_gap = max(start_gap, end_gap)

    # If there are multiple condition days, calculate longest gap   
    elif len(indices[0] > 1):
        start_gap = indices[0][0]
        mid_gap = max(abs(x - y) for (x, y) in zip(indices[0][1:], indices[0][:-1]))
        end_gap = len(condition_vector) - indices[0][-1]
        max_gap = max(start_gap, mid_gap, end_gap)

    return max_gap

def make_maps(company):
    """
    If requested, makes maps of proportion of timesteps that are deployment days.
    Also outputs a map of MCB (maximum condition blackout) over period of analysis.
    """

    # For each cell, sum the total number of deployment days and divide by total number of days
    for lon in range(len(company.state['weather'].longitude)):
        for lat in range(len(company.state['weather'].latitude)):
            company.DD_map[lon, lat] = (company.deployment_days[lon, lat, :].sum()) / company.parameters['timesteps']

    # Calculate MCB for each cell
    for lon in range(len(company.state['weather'].longitude)):
        for lat in range(len(company.state['weather'].latitude)):
            company.MCB_map[lon, lat] = gap_calculator(company.deployment_days[lon, lat, :])

    # Set variables necessary for writing map files
    DD_output = np.swapaxes(company.DD_map, axis1=0, axis2=1)
    MCB_output = np.swapaxes(company.MCB_map, axis1=0, axis2=1)
    lon, lat = company.state['weather'].longitude, company.state['weather'].latitude
    xmin, ymin, xmax, ymax = [lon.min(), lat.min(), lon.max(), lat.max()]
    nrows, ncols = np.shape(DD_output)
    xres = (xmax - xmin) / float(ncols)
    yres = (ymax - ymin) / float(nrows)
    geotransform = (xmin, xres, 0, ymax, 0, -yres)

    # Set output directory
    os.chdir(company.parameters['output_directory'])

    # Export 2D proportions matrix as map
    output_raster = gdal.GetDriverByName('GTiff').Create('DD_' + company.name + '_map_' + company.parameters['simulation'] + '.tif',
                                                         ncols, nrows, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify file coordinates
    srs = osr.SpatialReference()  # Establish coordinate encoding
    srs.ImportFromEPSG(4326)  # Specify WGS84 lat/long
    output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(DD_output)  # Writes my array to the raster
    output_raster = None

    # Export 2D MCB matrix as map
    output_raster = gdal.GetDriverByName('GTiff').Create('MCB_' + company.name + '_map_' + company.parameters['simulation'] + '.tif',
                                                         ncols, nrows, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify file coordinates
    srs = osr.SpatialReference()  # Establish coordinate encoding
    srs.ImportFromEPSG(4326)  # Specify WGS84 lat/long
    output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(MCB_output)  # Writes my array to the raster
    output_raster = None

    return