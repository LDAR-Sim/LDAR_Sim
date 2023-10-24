# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.reporting.estimate
# Purpose:     Basic method of estimating leak start date (half the time since last component
#              Survey)
#
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


def get_site_t_since_last_ldar(site, init_detect_company):
    """ Get the time since a site has last had LDAR"""

    if site['historic_t_since_LDAR'] is None:
        if '{}_RS'.format(init_detect_company) in site:
            RS = site['{}_RS'.format(init_detect_company)]
        else:
            RS = 1
        t_since_last_LDAR = ceil(365/RS)
    else:
        t_since_last_LDAR = site['historic_t_since_LDAR']

    return t_since_last_LDAR
