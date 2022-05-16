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

import os
from math import ceil, floor
from pathlib import Path

import cdsapi
import pandas as pd


# Input
facil_file = "./inputs/facilities_permian.csv"
root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent
facilities = pd.read_csv(root_dir/facil_file)

# Inputs
start_year = 2019
end_year = 2020
region_name = 'perm'
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
