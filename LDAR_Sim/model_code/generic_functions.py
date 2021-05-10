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
import os
import sys
from osgeo import gdal
from osgeo import osr
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import boto3  # for downloading data from AWS
from botocore.exceptions import ClientError
import ephem

def gap_calculator(condition_vector):
    """
    This function calculates max gaps between daily activites in a time series.
    Requires only a single binary vector describing whether a condition was met.
    """

    # Find the index of all days in which the condition is true
    max_gap = None
    indices = np.where(condition_vector)

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


def get_prop_rate(proportion, rates):
    """
     The purpose of this function is to calculate the emission rate(s) that
     correspond(s) with a desired proportion total emissions for a given emission
     size distribution. It estimates the MDL needed to find the top X percent
     of sources for a given leak size distribution.

     Inputs are: (1) a proportion value (or list a list of values) that represents
     top emitting sources, and (2) a distribution of emission rates (either leaks or sites).

     For example, given a proportion of 0.01 and a leak-size distribution,
     this function will return an estimate of the detection limit that will
     ensure that all leaks in the top 1% of leak sizes are found.

    """

    # Sort emission rates, get cumulative rates, and convert to proportions
    rates_sorted = sorted(rates)
    cum_rates = np.cumsum(rates_sorted)
    cum_rates_prop = cum_rates / max(cum_rates)

    # Get relative position of each element in emissions distribution
    p = 1. * np.arange(len(rates)) / (len(rates) - 1)

    # Estimate proportion of emissions that correspond with a given proportion of top emitters.
    # 100% of sites account for 100% of emissions. 0% of sites account for 0% of emissions.
    def f(x): return np.interp(x, xp=p, fp=cum_rates_prop)
    prop_rate = f(1 - proportion)
    # prop_above = 1 - prop_rate

    # Convert result (prop emissions) back to cumulative rate
    cum_rate = prop_rate * max(cum_rates)

    # Estimate emission rate that corresponds with cumulative rate
    def f2(x): return np.interp(x, cum_rates, rates_sorted)
    rate = f2(cum_rate)

    # A dataframe of all the useful info, if ever needed for a list of thresholds
    # (not returned by function)
    # df = pd.DataFrame(
    #     {'Proportion': proportion, 'Prop Emissions': prop_above, 'follow_up_thresh': rate})

    return (rate)


def make_maps(company, sites):
    """
    If requested, makes maps of proportion of timesteps that are deployment days.
    Also outputs a map of MCB (maximum condition blackout) over period of analysis.
    """

    # For each cell, sum the total number of deployment days and divide by total number of days
    for lon in range(len(company.state['weather'].longitude)):
        for lat in range(len(company.state['weather'].latitude)):
            company.DD_map[lon, lat] = (
                company.deployment_days[lon, lat, :].sum()) / company.parameters['timesteps']

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
    output_raster = gdal.GetDriverByName('GTiff').Create('DD_' + company.name + '_map' + '.tif',
                                                         ncols, nrows, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify file coordinates
    srs = osr.SpatialReference()  # Establish coordinate encoding
    srs.ImportFromEPSG(4326)  # Specify WGS84 lat/long
    output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(DD_output)  # Writes my array to the raster
    output_raster = None

    # Export 2D MCB matrix as map
    output_raster = gdal.GetDriverByName('GTiff').Create('MCB_' + company.name + '_map' + '.tif',
                                                         ncols, nrows, 1, gdal.GDT_Float32)
    output_raster.SetGeoTransform(geotransform)  # Specify file coordinates
    srs = osr.SpatialReference()  # Establish coordinate encoding
    srs.ImportFromEPSG(4326)  # Specify WGS84 lat/long
    output_raster.SetProjection(srs.ExportToWkt())  # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(MCB_output)  # Writes my array to the raster
    output_raster = None

    # Make nice map images
    plt.rcParams["figure.figsize"] = (10, 10)
    map = Basemap(epsg=3401, llcrnrlon=xmin - 1, llcrnrlat=ymin - 1, urcrnrlon=xmax + 3,
                  urcrnrlat=ymax + 1, resolution='i', area_thresh=10000.)
    map.fillcontinents(color='#e8e8e8', alpha=1, zorder=1)
    map.drawcountries(color='black', linewidth=2, zorder=3)
    map.drawstates(color='black', linewidth=1, zorder=4)
    map.drawparallels(
        np.arange(ymin, ymax, round(abs(ymin - ymax) / 3)),
        color="black", labels=[1, 0, 0, 0],
        fontsize=10, linewidth=0.2, zorder=5)
    map.drawmeridians(
        np.arange(xmin, xmax, round(abs(xmin - xmax) / 3)),
        color="black", labels=[0, 0, 0, 1],
        fontsize=10, linewidth=0.2, zorder=6)

    sitesx, sitesy = map(
        (pd.to_numeric(sites['lon']) + 360).tolist(),
        pd.to_numeric(sites['lat']).tolist())
    map.scatter(sitesx, sitesy, marker='o', color='black', s=1, zorder=7)

    m_lon, m_lat = np.meshgrid(lon, lat)
    xi, yi = map(m_lon, m_lat)

    cs = map.pcolor(xi, yi, np.squeeze(DD_output), alpha=1, vmin=0, vmax=1, cmap='jet_r', zorder=2)
    cbar = map.colorbar(cs, location='bottom', pad="5%")
    cbar.set_alpha(1)
    cbar.draw_all()
    cbar.set_label('Proportion of days suitable for deployment', fontsize=12)
    plt.savefig('DD_' + company.name + '_map' + '.png', dpi=300)
    plt.clf()

    map2 = Basemap(epsg=3401, llcrnrlon=xmin - 1, llcrnrlat=ymin - 1, urcrnrlon=xmax + 3,
                   urcrnrlat=ymax + 1, resolution='i', area_thresh=10000.)
    map2.fillcontinents(color='#e8e8e8', alpha=1, zorder=1)
    map2.drawcountries(color='black', linewidth=2, zorder=3)
    map2.drawstates(color='black', linewidth=1, zorder=4)
    map2.drawparallels(
        np.arange(ymin, ymax, round(abs(ymin - ymax) / 3)),
        color="black", labels=[1, 0, 0, 0],
        fontsize=10, linewidth=0.2, zorder=5)
    map2.drawmeridians(
        np.arange(xmin, xmax, round(abs(xmin - xmax) / 3)),
        color="black", labels=[0, 0, 0, 1],
        fontsize=10, linewidth=0.2, zorder=6)
    map2.scatter(sitesx, sitesy, marker='o', color='black', s=1, zorder=7)

    m_lon, m_lat = np.meshgrid(lon, lat)
    xi, yi = map(m_lon, m_lat)

    cs = map2.pcolor(xi, yi, np.squeeze(MCB_output), alpha=1,
                     vmin=0, vmax=365, cmap='jet', zorder=2)
    cbar = map2.colorbar(cs, location='bottom', pad="5%")
    cbar.set_alpha(1)
    cbar.draw_all()
    cbar.set_label('Maximum blackout period (days)', fontsize=12)
    plt.savefig('MCB_' + company.name + '_map' + '.png', dpi=300)
    plt.clf()

    return


def check_ERA5_file(wd, target_file):
    ncfiles = []
    target_file_found = False
    # search netCDF file in the working directory
    for file in os.listdir(wd):
        if file.endswith(".nc"):
            ncfiles.append(file)

    for file in ncfiles:
        if file == target_file:
            target_file_found = True

    if target_file_found:
        print("Weather data checked. Continuing simulation.")

    if not target_file_found:
        print("Weather data not found. Downloading now from AWS you...")
        access_key = os.getenv('AWS_KEY')
        secret_key = os.getenv('AWS_SEC')

        try:
            s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            s3.download_file('im3sweather', target_file, r'{}/{}'.format(wd, target_file))
        except ClientError:
            print("Authentication Failed or Server Unavailable. Exiting")
            sys.exit()
        print("Weather data download complete")
        
def geo_idx(dd, dd_array):
    """
     - dd - the decimal degree (latitude or longitude)
     - dd_array - the list of decimal degrees to search.
     search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
   """
    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx
	
def quick_cal_daylight(date,lat,lon):

    # Create ephem object
    obs = ephem.Observer()
    # turn off PyEphem’s native mechanism for computing atmospheric refraction
    # near the horizon
    obs.pressure = 0
    obs.horizon = '-6'  # -6=civil twilight, -12=nautical, -18=astronomical
    # set the time
    obs.date = date
    # set the latitude and longitude for object
    obs.lat = str(lat)
    obs.lon = str(lon)

    # get the sunset and sunrise UTC time
    sunrise = obs.previous_rising(ephem.Sun(), use_center=True).datetime()
    sunset = obs.next_setting(ephem.Sun(), use_center=True).datetime()

    # convert to local time
    sr = (sunrise.hour - 7) + (sunrise.minute / 100)
    ss = (sunset.hour + 17) + (sunset.minute / 100)

    sunrise = sr
    sunset = ss

    return (sunrise,sunset)
