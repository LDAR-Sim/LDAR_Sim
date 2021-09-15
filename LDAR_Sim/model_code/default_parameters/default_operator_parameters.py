# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        default_OGI_parameters
# Purpose:     Default OGI parameters
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

default_operator_parameters = {
    'version': '2.0',
    'parameter_level': 'method',
    'label': 'operator',
    'module': 'dummy',
    'deployment_type': 'stationary',
    'measurement_scale': "component",
    'sensor': 'AVO',
    'is_follow_up': False,
    'n_crews': 1,
    'min_temp': -20,
    'max_wind': 10,
    'max_precip': 0.1,
    'max_workday': 8,
    'cost': {
        'upfront': 0,
        'per_day': 2500,
        'per_hour': 0,
        'per_site': 0,
    },
    'reporting_delay': 2,
    't_bw_sites': 0,
    'MDL': 0.7,
    'percent_detectable': 0.1,
    'consider_daylight': False,
    'scheduling': {
        'route_planning': False,
        'home_bases': 'homebases.csv',
        'speed_list': [80, 90, 100],
        'LDAR_crew_init_location': [-114.062019, 51.044270],
        'deployment_years': [],
        'deployment_months': [],
    },
}
