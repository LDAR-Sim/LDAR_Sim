# ------------------------------------------------------------------------------
# Program:     ERA_concat (standalone)
# File:        ERA_concat.py
# Purpose:     Concatenate timeseries from ERA5 netcdf files
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
from pathlib import Path

import xarray

'''
Concatenate two weather netcdf files on the time column. Keep Lat Long coordinates the same
'''

# Inputs
folder = 'inputs'
f1 = "ERA5_2017_2018_AB.nc"
f2 = "ERA5_2019_2020_AB.nc"
output = "ERA5_2017_2020_AB.nc"


root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent
os.chdir(root_dir/folder)
ds = xarray.open_mfdataset([f1, f2], combine='by_coords', concat_dim="time", decode_times=False)
ds.to_netcdf(output)
