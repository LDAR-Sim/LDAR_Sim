# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Generic functions
# Purpose:     Generic functions for running LDAR-Sim.
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
from osgeo import gdal
from osgeo import osr
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


#convert df to gdf fun 
def df_to_gdf (df,lat,lon,epsg):
    # lat and lon are column name of coordinates field in df 
    geometry = [Point(xy) for xy in zip(df[lon], df[lat])]
    df = df.drop([lon, lat], axis=1)
    crs = {'init':"epsg:"+str(epsg)}
    df = gpd.GeoDataFrame(df,crs=crs,geometry = geometry)
    return df


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

def make_maps(company, sites,epsg = 4326):
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
	output_name  = 'DD_' + company.name + '_map' + '.tif'
    output_raster = gdal.GetDriverByName('GTiff').Create(output_name,
                                                         ncols, nrows, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify file coordinates
    srs = osr.SpatialReference()  # Establish coordinate encoding
    srs.ImportFromEPSG(4326)  # Specify WGS84 lat/long
    output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(DD_output)  # Writes my array to the raster
    output_raster = None
	# project the raster 
	iras = gdal.Open(output_name)
	prj_output_name = 'DD_' + company.name + '_map' +'_prj' + '.tif'
	gdal.Warp(prj_output_name,iras,dstSRS = "EPSG:"+str(epsg))
	

    # Export 2D MCB matrix as map
	output_name  = 'MCB_' + company.name + '_map' + '.tif'
    output_raster = gdal.GetDriverByName('GTiff').Create('output_name,
                                                         ncols, nrows, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify file coordinates
    srs = osr.SpatialReference()  # Establish coordinate encoding
    srs.ImportFromEPSG(4326)  # Specify WGS84 lat/long
    output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(MCB_output)  # Writes my array to the raster
    output_raster = None
	# project the raster 
	iras = gdal.Open(output_name)
	prj_output_name = 'MCB_' + company.name + '_map' +'_prj' + '.tif'
	gdal.Warp(prj_output_name,iras,dstSRS = "EPSG:"+str(epsg))
	
	
	# convert sites dataframe to sites geodataframe
	sites_gdf = df_to_gdf (sites,"lat","lon",4326)
	# project the geodataframe
	sites_gdf.crs={'init' :'epsg:4326'} 
	sites_gdf = sites_gdf.to_crs({'init': 'epsg:'+str(epsg)})
	
	sitesx = np.array(sites_gdf.geometry.x)
	sitesy = np.array(sites_gdf.geometry.y)


    # Make nice map images
    plt.rcParams["figure.figsize"] = (10, 10)
    map1 = Basemap(epsg=epsg, llcrnrlon=xmin - 360 - 1, llcrnrlat= ymin - 1, urcrnrlon=xmax - 360 + 3,
                  urcrnrlat=ymax + 1, resolution='i', area_thresh=10000.)
    map1.fillcontinents(color='#e8e8e8', alpha=1, zorder=1)
    map1.drawcountries(color='black', linewidth=2, zorder=3)
    map1.drawstates(color='black', linewidth=1, zorder=4)
    map1.drawparallels(np.arange(ymin, ymax, round(abs(ymin-ymax)/3)), color="black", labels=[1, 0, 0, 0], fontsize=10, linewidth=0.2, zorder=5)
    map1.drawmeridians(np.arange(xmin, xmax, round(abs(xmin-xmax)/3)), color="black", labels=[0, 0, 0, 1], fontsize=10, linewidth=0.2, zorder=6)
	
	x,y = map1(sitesx,sitesy)
	map1.scatter(x, y, marker='o',s=5, zorder=7, color = 'black')
	
	m_lon, m_lat = np.meshgrid(lon, lat)
	xi, yi = map(m_lon, m_lat)
    cs = map1.pcolor(xi, yi, np.squeeze(DD_output), alpha=1, vmin=0, vmax=1, cmap='jet_r', zorder=2)
    cbar = map1.colorbar(cs, location='bottom', pad="5%")
    cbar.set_alpha(1)
    cbar.draw_all()
    cbar.set_label('Proportion of days suitable for deployment', fontsize=12)
    plt.savefig('DD_' + company.name + '_map' + '.png', dpi=300)
    plt.clf()
			#### Map2###
    map2 = Basemap(epsg=epsg, llcrnrlon=xmin - 360 - 1, llcrnrlat= ymin - 1, urcrnrlon=xmax - 360 + 3,
                  urcrnrlat=ymax + 1, resolution='i', area_thresh=10000.)
    map2.fillcontinents(color='#e8e8e8', alpha=1, zorder=1)
    map2.drawcountries(color='black', linewidth=2, zorder=3)
    map2.drawstates(color='black', linewidth=1, zorder=4)
    map2.drawparallels(np.arange(ymin, ymax, round(abs(ymin-ymax)/3)), color="black", labels=[1, 0, 0, 0], fontsize=10, linewidth=0.2, zorder=5)
    map2.drawmeridians(np.arange(xmin, xmax, round(abs(xmin-xmax)/3)), color="black", labels=[0, 0, 0, 1], fontsize=10, linewidth=0.2, zorder=6)
	
	x,y = map2(sitesx,sitesy)
    map2.scatter(x, y, marker='o', color = 'black', s = 1, zorder=7)

    m_lon, m_lat = np.meshgrid(lon, lat)
    xi, yi = map(m_lon, m_lat)

    cs = map2.pcolor(xi, yi, np.squeeze(MCB_output), alpha=1, vmin=0, vmax=365, cmap='jet', zorder=2)
    cbar = map2.colorbar(cs, location='bottom', pad="5%")
    cbar.set_alpha(1)
    cbar.draw_all()
    cbar.set_label('Maximum blackout period (days)', fontsize=12)
    plt.savefig('MCB_' + company.name + '_map' + '.png', dpi = 300)
    plt.clf()

    return
