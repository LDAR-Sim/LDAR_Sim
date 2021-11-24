# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Generic functions
# Purpose:     Generic functions for running LDAR-Sim.
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

import collections
import datetime
import os
import sys
from math import atan, atan2, cos, degrees, sin, sqrt
from pathlib import Path

import boto3
import ephem
import numpy as np
from botocore.exceptions import ClientError
from shapely.geometry import Polygon


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



def check_ERA5_file(dir, programs):
    for p in programs:
        my_file = Path(dir / p['weather_file'])
        if my_file.is_file():
            print("Weather data checked. Continuing simulation.")
        else:
            print("Weather data not found. Downloading from AWS now ...")
            try:
                access_key = os.getenv('AWS_KEY')
                secret_key = os.getenv('AWS_SEC')
            except Exception:
                print(
                    "AWS_KEY and AWS_SEC environment variables have not been set," +
                    "refer to model documentation for configuration instructions.")

            try:
                s3 = boto3.client('s3', aws_access_key_id=access_key,
                                  aws_secret_access_key=secret_key)
                s3.download_file('im3sweather', p['weather_file'],
                                 r'{}/{}'.format(dir, p['weather_file']))
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


def quick_cal_daylight(date, lat, lon):

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

    return (sunrise, sunset)


def ecef_to_llh(ecef_km):
    """
    Converts the Earth-Centered Earth-Fixed (ECEF) coordinates (x, y, z) to
    (WGS-84) Geodetic point (lat, lon, h)
    ecef_km contains three elements
    ecef_km[0] is the x coordiante of satellite in ecef in km
    ecef_km[1] is the y coordiante of satellite in ecef in km
    ecef_km[2] is the z coordiante of satellite in ecef in km
    """
    # WGS-84 Earth semimajor axis (km)
    a = 6378.1370
    # Derived Earth semimajor axis (km)
    b = 6356.752314
    # pythagoras to calculate two earth's minor axises
    p = sqrt(ecef_km[0] ** 2 + ecef_km[1] ** 2)
    # Calculate the angle between orbit object and earth center
    thet = atan(ecef_km[2] * a / (p * b))
    # Caluclate ellipsoid flatness and ellipsoid flatness factor
    esq = 1.0 - (b / a) ** 2
    epsq = (a / b) ** 2 - 1.0
    # calculate latitude
    lat = atan((ecef_km[2] + epsq * b * sin(thet) ** 3) /
               (p - esq * a * cos(thet) ** 3))
    # calculate longitude
    lon = atan2(ecef_km[1], ecef_km[0])
    # Calculate prime vertical radius of curvature at latitude
    n = a * a / sqrt(a * a * cos(lat) ** 2 + b ** 2 * sin(lat) ** 2)
    # Calculate altitude
    h = p / cos(lat) - n
    lat = degrees(lat)
    lon = degrees(lon)
    return lat, lon, h


def init_orbit_poly(predictor, T1, T2, interval):
    """
    Grab the esitamted positions of satellite
    predictor: orbit path predictor of satellit created by using orbit_predictor package
    T1: start datetime
    T2: end datetime
    interval: time interval of each time step in minutes

    return: day_list: date time of the satellite
            polygon_list: coverage area polygon of the satellite

    """
    polygon_list = []
    day_list = []
    while T1 != T2:
        # obtain the position info of the satellite
        info1 = predictor.get_position(T1)
        # get position in ecef coordinate system
        ecef1 = info1.position_ecef
        # covert ecef to lat, lon, and altitude
        lat1, lon1, h1 = ecef_to_llh(ecef1)

        # update time
        st = T1 + datetime.timedelta(minutes=interval)
        # obtain the position of the satellite
        info2 = predictor.get_position(st)
        ecef2 = info2.position_ecef
        lat2, lon2, h2 = ecef_to_llh(ecef2)

        # get the bounding box of the coverage of satellite between this two time step
        pt1 = (lon1, lat1+0.1)
        pt2 = (lon1+0.1, lat1)
        pt3 = (lon2, lat2-0.1)
        pt4 = (lon2-0.1, lat2)

        # create that coverage area polygon
        polygon3 = Polygon([pt1, pt2, pt3, pt4])
        polygon_list.append(polygon3)
        day_list.append(T1)

        T1 += datetime.timedelta(minutes=interval)

    return day_list, polygon_list


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + str(k) if parent_key else str(k)
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
