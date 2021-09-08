# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        default_program_parameters
# Purpose:     Default program parameters
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

default_program_parameters = {
    'version': '2.0',
    'parameter_level': 'program',
    'methods': {},
    'method_labels': [],
    'program_name': 'default',
    'weather_file': "ERA5_2017_2020_AB.nc",
    'weather_is_hourly': True,
    'infrastructure_file': 'facility_list_template.csv',
    'site_samples': [True, 500],
    'subtype_times': [False, 'subtype_times.csv'],
    'consider_operator': False,
    'consider_venting': False,
    'consider_weather': True,
    'repair_delay': 14,
    'repair_cost': 200,
    'emissions': {
        'leak_count_file': 'leak_counts.csv',
        'vent_file': 'site_rates.csv',
        'leak_file': "",  # 'leak_rates.csv',
        'leak_file_use': 'sample',  # 'sample', 'fit'
        'leak_dist_type': 'lognorm',
        'leak_dist_params': [-2.776, 1.462],
        'units': ['kilogram', 'hour'],
        'subtype_leak_dist_file': None,
        'max_leak_rate': 100,
    },

    'LPR': 0.0065,
    'NRd': 150,
    'max_det_op': 0.00,
    'operator_strength': 0,
    'verification_cost': 25,
}
