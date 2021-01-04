# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:48:15 2021

@author: MZG
"""

import netCDF4 as nc 
import pandas as pd 
import numpy as np

yrs = [2015,2016,2017,2018,2019]

Wbase = np.empty((1,45,41),dtype=np.float)
Tbase = np.empty((1,45,41),dtype=np.float)
Pbase = np.empty((1,45,41),dtype=np.float)
for y in yrs: 
    data = nc.Dataset(r"D:\ERA5AB\weather_04_19/weather_{}.nc".format(y),'r') # where you save data 
    t = len(data['time'][:])
    days =int(t/24)
    
    lat = data.variables["latitude"][:]
    lon = data.variables['longitude'][:]
    
    WS = np.empty((days,45,41),dtype=np.float)
    TMP = np.empty((days,45,41),dtype=np.float)
    TP = np.empty((days,45,41),dtype=np.float)
    li = 0
    ui = 23
    index=0 
    while ui < t:

        #wind
        v = data.variables['v10'][li:ui,:,:]
        u = data.variables['u10'][li:ui,:,:]
        ws = (u ** 2 + v ** 2) ** 0.5
        d_ave_ws = np.average(ws,axis=0)
        WS[index,:,:] = d_ave_ws

        # temperature
        tmp = data.variables['t2m'][li:ui,:,:]
        tmp = tmp - 273.15 
        d_ave_tmp = np.average(tmp,axis=0)
        TMP[index,:,:] = d_ave_tmp

        #Total precipitation
        tp = data.variables['tp'][li:ui,:,:]
        tp = tp * 1000
        d_ave_tp = np.average(tp,axis=0)
        TP[index,:,:] = d_ave_tp

        li += 24 
        ui += 24
        index += 1
    
    Wbase = np.concatenate((Wbase,WS),axis=0)
    Tbase = np.concatenate((Tbase,TMP),axis=0)
    Pbase = np.concatenate((Pbase,TP),axis=0)
    data.close()
    print (y)
    
W5 = Wbase[1:,:,:]
T5 = Tbase[1:,:,:]
P5 = Pbase[1:,:,:]

ti = W5.shape[0]
la = W5.shape[1]
lo = W5.shape[2]

#write everything into one netcdf file 
ncfile = nc.Dataset('D:\ERA5AB\ERA5_new.nc',mode='w',format='NETCDF4_CLASSIC') 

# create dimensions
lat_dim = ncfile.createDimension('lat', la)     # latitude axis
lon_dim = ncfile.createDimension('lon', lo)    # longitude axis
time_dim = ncfile.createDimension('time',ti)  # time axis 


# create dimension variables 
new_lat = ncfile.createVariable('lat', np.float32, ('lat',))
new_lat.units = 'degrees_north'
new_lat.long_name = 'latitude'
new_lon = ncfile.createVariable('lon', np.float32, ('lon',))
new_lon.units = 'degrees_east'
new_lon.long_name = 'longitude' 
new_time = ncfile.createVariable('time', np.float64, ('time',))
new_time.units = 'days since 2015-01-01'
new_time.long_name = 'time'


# create weather variables
# tempertaure
temp = ncfile.createVariable('t2m',np.float64,('time','lat','lon')) # note: unlimited dimension is leftmost
temp.units = 'C' # degrees Celsius
temp.standard_name = 'daily average 2 meter air temperature' # this is a CF standard name 

# wind speed 
wind = ncfile.createVariable('ws10',np.float64,('time','lat','lon')) 
wind.units = "m/s" 
wind.standard_name = 'daily average wind speed 10 meter above ground' 

# total precipitation 
precip = ncfile.createVariable('tp',np.float64,('time','lat','lon')) 
precip.units = "mm"
precip.standard_name = 'daily average 2 meter air temperature' 


# writing data 
new_lat[:] = lat
new_lon[:] = lon 
temp[:] = T5
wind[:] = W5
precip[:] = P5

ncfile.close()