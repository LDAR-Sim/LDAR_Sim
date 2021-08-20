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
    'UTC_offset': -6,
    'time_offsite': 'time_offsite_ground.csv',
    'weather_file': "ERA5_AB_1x1_hourly_2015_2019.nc",
    'weather_is_hourly': False,
    'infrastructure_file': 'facility_list_template.csv',
    'leak_file': 'leak_rates.csv',
    'count_file': 'leak_counts.csv',
    'vent_file': 'site_rates.csv',
    'site_samples': [True, 500],
    'subtype_distributions': [False, 'subtype_distributions.csv'],
    'subtype_times': [False, 'subtype_times.csv'],
    'consider_operator': False,
    'consider_venting': False,
    'consider_weather': True,
    'repair_delay': 14,
    'repair_cost': 200,
    'use_empirical_rates': False,
    'leak_rate_dist': ['lognorm', -2.776, 1.462, "kilogram", "hour"],
    'max_leak_rate': 100,
    'LPR': 0.0065,
    'NRd': 150,
    'max_det_op': 0.00,
    'spin_up': 0,
    'write_data': True,
    'make_plots': True,
    'make_maps': True,
    'print_from_simulations': True,
    'operator_strength': 0,
    'verification_cost': 25,
}
