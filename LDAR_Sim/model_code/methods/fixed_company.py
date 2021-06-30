# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        Travel Base Company
# Purpose:     Company managing crew agents agents
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


from methods.base_company import company as base_company


class fixed_company(base_company):

    def __init__(self, state, parameters, config, timeseries):
        super(fixed_company, self).__init__(state, parameters, config, timeseries)
        # --- Fixed Sensor specific Initalization ---
        # -------------------------------------------
    # --- Fixed Sensor specific methods ---
    # -------------------------------------
