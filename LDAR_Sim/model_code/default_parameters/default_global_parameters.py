# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        default_global_parameters
# Purpose:     Default global parameters
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

default_global_parameters = {
    'version': '2.0',
    'parameter_level': 'global',
    'wd': '..//inputs_template//',
    'output_directory': '..//outputs//',
    'n_processes':  None,
    'print_from_simulations': True,
    'n_simulations': 2,
    'spin_up': 0,
    'write_data':  True,
    'programs': [],
    'weather_file': "ERA5_AB_1x1_hourly_2015_2019.nc",
    'timesteps': 1000,
    'start_year': 2017,
    'reference_program': 'P_ref',
}


