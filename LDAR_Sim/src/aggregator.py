# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
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
import operator


def aggregate(site):

    equipment_rates = []
    site_rate = 0

    # Make list of all leaks and add up all emissions at site
    site_rate = sum(map(operator.itemgetter('rate'), site['active_leaks']))

    # Sum emissions by equipment group
    for group in range(int(site['equipment_groups'])):
        group_emissions = 0
        for leak in site['active_leaks']:
            if leak['equipment_group'] == (group + 1):
                group_emissions += leak['rate']
        equipment_rates.append(group_emissions)

    return site['active_leaks'], equipment_rates, site_rate
