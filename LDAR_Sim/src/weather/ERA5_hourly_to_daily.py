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

import netCDF4 as nc
import numpy as np

yrs = [2017, 2018, 2019]  # Here, we have weather data for 2017, 2018, and 2019.
# Here, each data file includes four weather variables:
# u and v wind components, temperature and wind.
# We also know there are 45 rows and 41 columns of grids
# for Alberta when each grid is 0.25-degree square.

ubase = np.empty((1, 45, 41), dtype=np.float)  # create empty array for storing converted data
vbase = np.empty((1, 45, 41), dtype=np.float)
Tbase = np.empty((1, 45, 41), dtype=np.float)
Pbase = np.empty((1, 45, 41), dtype=np.float)
for y in yrs:
    data = nc.Dataset(
        r"D:\ERA5AB\weather_04_19\weather_{}.nc".format(y),
        'r')  # where you save data
    t = len(data['time'][:])  # read time
    days = int(t/24)
    # create empty arrays for each variable of ech file
    U10 = np.empty((days, 45, 41), dtype=np.float)
    V10 = np.empty((days, 45, 41), dtype=np.float)
    T2M = np.empty((days, 45, 41), dtype=np.float)
    TP = np.empty((days, 45, 41), dtype=np.float)
    li = 0
    ui = 23
    index = 0
    # for every 24 hours we calculate averages for each weather variable and
    # assign averages tothe predefined empty arrays
    while ui < t:

        # wind
        u = data.variables['u10'][li:ui, :, :]
        v = data.variables['v10'][li:ui, :, :]
        u_ave = np.average(u, axis=0)
        v_ave = np.average(v, axis=0)
        U10[index, :, :] = u_ave
        V10[index, :, :] = v_ave

        # temperature
        t2m = data.variables['t2m'][li:ui, :, :]
        t2m_ave = np.average(t2m, axis=0)
        T2M[index, :, :] = t2m_ave

        # Total precipitation
        tp = data.variables['tp'][li:ui, :, :]
        tp_ave = np.average(tp, axis=0)
        TP[index, :, :] = tp_ave

        li += 24
        ui += 24
        index += 1

    ubase = np.concatenate((ubase, U10), axis=0)
    vbase = np.concatenate((vbase, V10), axis=0)
    Tbase = np.concatenate((Tbase, T2M), axis=0)
    Pbase = np.concatenate((Pbase, TP), axis=0)
    data.close()
    print(y)

# extract only effective values for each weather variable array
u3 = ubase[1:, :, :]
v3 = vbase[1:, :, :]
T3 = Tbase[1:, :, :]
P3 = Pbase[1:, :, :]

ti = u3.shape[0]
la = u3.shape[1]
lo = u3.shape[2]

# write everything into one netcdf file
ncfile = nc.Dataset('D:\ERA5AB\ERA5_new.nc', mode='w', format='NETCDF4_CLASSIC')  # noqa

# create dimensions
lat_dim = ncfile.createDimension('lat', la)     # latitude axis
lon_dim = ncfile.createDimension('lon', lo)    # longitude axis
time_dim = ncfile.createDimension('time', ti)  # time axis


# create dimension variables
new_lat = ncfile.createVariable('lat', np.float32, ('lat',))
new_lat.units = 'degrees_north'
new_lat.long_name = 'latitude'
new_lon = ncfile.createVariable('lon', np.float32, ('lon',))
new_lon.units = 'degrees_east'
new_lon.long_name = 'longitude'
new_time = ncfile.createVariable('time', np.int, ('time',))
new_time.units = 'days since 2015-01-01'
new_time.long_name = 'time'


# create weather variables
# tempertaure
temp = ncfile.createVariable('t2m', np.float64, ('time', 'lat', 'lon')
                             )  # note: unlimited dimension is leftmost
temp.units = 'K'
temp.standard_name = 'daily average 2 meter air temperature'  # this is a CF standard name

# wind components
u_comp = ncfile.createVariable('u10', np.float64, ('time', 'lat', 'lon'))
u_comp.units = "m/s"
u_comp.standard_name = 'daily average 10 meter u wind component above ground'

v_comp = ncfile.createVariable('v10', np.float64, ('time', 'lat', 'lon'))
v_comp.units = "m/s"
v_comp.standard_name = 'daily average 10 meter v wind component above ground'

# total precipitation
precip = ncfile.createVariable('tp', np.float64, ('time', 'lat', 'lon'))
precip.units = "m"
precip.standard_name = 'daily average 2 meter air temperature'


# writing data
# new_lat[:] = lat
# new_lon[:] = lon
# new_time[:] = arange(ti)
temp[:] = T3
u_comp[:] = u3
v_comp[:] = v3
precip[:] = P3

ncfile.close()
