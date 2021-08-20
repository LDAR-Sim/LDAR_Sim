# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        default_truck_parameters
# Purpose:     Default truck parameters
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

default_truck_parameters = {
    'version': '2.0',
    'parameter_level': 'method',
    'label': 'truck',
    'module': 'truck',
    'deployment_type': 'mobile',
    'n_crews': 1,
    'min_temp': -40,
    'max_wind': 20,
    'max_precip': 0.01,
    'max_workday': 8,
    'measurement_scale': "equipment",
    'cost_per_day': 2000,
    'follow_up_thresh': [0, "absolute"],
    'follow_up_ratio': 1,
    'reporting_delay': 2,
    'MDL': 0.05,
    'QE': 0,
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
