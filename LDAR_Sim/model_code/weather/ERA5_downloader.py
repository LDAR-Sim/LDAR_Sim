# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        ERA5 downloader
# Purpose:     Downloads ERA5 data
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

import cdsapi
import os
from math import floor, ceil
import pandas as pd
from pathlib import Path

'''
NOTE - This can take a very long time to download data from the copernicus server,
expect to be in the cueue for 1-3 hours regardless of file size be patient.

This script will download ERA reyanalysis weather data. In order to run you have to:

1) Setup a Copernicus account. Account setup instructions can be found at:
https://cds.climate.copernicus.eu/#!/home

2) Get UID and API key from account and put them in a .cdapirc file. See:
https://cds.climate.copernicus.eu/api-how-to

3) Enter facility template csv location, which must hava a lat and lon column.
    File must be relative to the root folder.

4) Fill in start year, end year, a region name (for output file tag), output resolution
   in degrees, and variable names to retrieve. Variable names  can be found at:
https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

This code is based on:
https://confluence.ecmwf.int/display/COPSRV/CDS+web+API+%28cdsapi%29+training
'''

# Input
facil_file = "./inputs_template/facility_list_template.csv"
root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent
facilities = pd.read_csv(root_dir/facil_file)

# Inputs
start_year = 2019
end_year = 2020
region_name = 'AB'
res = [1, 1]  # Resolution in degrees
vars = [
    'total_precipitation', '10m_u_component_of_wind',
    '10m_v_component_of_wind', '2m_temperature', 'total_cloud_cover',
]  # define the weather variables you want to download

# Bounding box (N,W,S,E)
bb = [str(ceil(facilities['lat'].max())), str(floor(facilities['lon'].min())),
      str(floor(facilities['lat'].min())), str(ceil(facilities['lon'].max()))]
yrs = [str(x) for x in range(start_year, end_year+1)]

c = cdsapi.Client()
# download hourly data for Alberta from 2017-01-01 to 2019-12-31
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': vars,
        'year': yrs,
        'month': ['{:02d}'.format(x) for x in range(1, 13)],
        'day': ['{:02d}'.format(x) for x in range(1, 32)],
        'time': ['{:02d}:00'.format(x) for x in range(0, 24)],
        'area': bb,
        'grid': res,  # define the size of weather grid in degrees (spatial resolution)
        'format': 'netcdf',
    },
    r'ERA5_{}_{}_{}.nc'.format(start_year, end_year, region_name))  # define the name of file
