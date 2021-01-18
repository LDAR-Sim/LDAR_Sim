# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        ERA5 downloader
# Purpose:     Downloads ERA5 data
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

import cdsapi
# downloads ERA5 total precipitation, 10 meter wind u component, 10 meter wind v component, and 2 meter air temperature 
c = cdsapi.Client()
# download hourly data for Alberta from 2017-01-01 to 2019-12-31
yrs = ['2017','2018','2019'] 
mns = ['01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',]
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'variable':[
            'total_precipitation','10m_u_component_of_wind', 
            '10m_v_component_of_wind', '2m_temperature',
        ],
        'year':yrs,
        'month':mns,
        'day':[
            '01','02','03',
            '04','05','06',
            '07','08','09',
            '10','11','12',
            '13','14','15',
            '16','17','18',
            '19','20','21',
            '22','23','24',
            '25','26','27',
            '28','29','30',
            '31',
        ],
        'time':['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00',
                    '08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00',
                   '16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00',
                   ],

        'area': [60,-120,49,-110,],
        'grid':[1,1],
        'format':'netcdf',
    },
    r'ERA5_2017_2019_AB.nc')
