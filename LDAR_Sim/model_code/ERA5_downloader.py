# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        ERA5 downloader
# Purpose:     Downloads ERA5 data
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

import cdsapi
# more detail about how to use cdsapi can be found in
# https://confluence.ecmwf.int/display/COPSRV/CDS+web+API+%28cdsapi%29+training
# downloads ERA5 total precipitation, 10 meter wind u component, 10 meter wind v
# component, and 2 meter air temperature
c = cdsapi.Client()
# download hourly data for Alberta from 2017-01-01 to 2019-12-31
yrs = ['2017', '2018', '2019']  # specify the years you want to download
mns = ['01', '02', '03',
       '04', '05', '06',
       '07', '08', '09',
       '10', '11', '12', ]  # specify the months you want to download
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            'total_precipitation', '10m_u_component_of_wind',
            '10m_v_component_of_wind', '2m_temperature',
        ],  # define the weather variables you want to download
        'year': ['2017', '2018', '2019'],  # define the years you want to download
        'month': ['01', '02', '03',
                  '04', '05', '06',
                  '07', '08', '09',
                  '10', '11', '12', ],  # define the months you want to download in each year
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],  # define the days you want to download in each month
        'time': ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
                 '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                 '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',
                 ],  # define hours you want to download in each day (temporal resolusion)

        # define the study area bounding box [north west south east]
        'area': [60, -120, 49, -110, ],
        'grid': [1, 1],  # define the size of weather grid in degrees (spatial resolution)
        'format': 'netcdf',
    },
    r'ERA5_2017_2019_AB.nc')  # define the name of file
