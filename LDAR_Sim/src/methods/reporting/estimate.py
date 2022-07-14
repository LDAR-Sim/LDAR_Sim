# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.reporting.estimate
# Purpose:     Basic method of estimating leak start date (half the time since last component
#              Survey)
#
# Copyright (C) 2018-2022  Intelligent Methane Monitoring and Management System (IM3S) Group
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
from math import ceil


def estimate_start_date(leak, cur_ts, site, company, init_detect_company):
    """ Estimate The start day based on calculation type.

    Args:
        crews (list): List of crews

    """

    if site['historic_t_since_LDAR'] is None:
        if '{}_RS'.format(init_detect_company['label']) in site:
            RS = site['{}_RS'.format(init_detect_company['label'])]
        else:
            RS = 1
        t_since_last_LDAR = ceil(365/RS)
    else:
        t_since_last_LDAR = site['historic_t_since_LDAR']
    estimated_start_date = cur_ts - t_since_last_LDAR / 2
    if estimated_start_date < 0:
        estimated_start_date = 0
    return estimated_start_date
