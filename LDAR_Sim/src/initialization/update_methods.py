# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.update_methods
# Purpose:     Estimate number of crews, and number of sites a crew can survey in a day
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

from math import ceil, floor
from numpy.random import choice
from numpy import average


def est_n_crews(m, sites):
    """ Estimate the number of mobile crews required to survey all sites within a campaign. This
    function will find estimate number of crews based on an estimate of sites per day a single
    crew is able to accomplish. If the function fails (usually non mobile method) n_crews of 1
    will be returned.

    Args:
        m (dict): method parameters
        sites (dict): site dictionary
    Returns:
        int: number of working crews.
    """
    m_name = m['label']
    avg_sites_per_day = est_site_p_day(m, sites)
    try:
        avg_days_per_campaign = ceil(average([365 / s['{}_RS'.format(m_name)] for s in sites]))
        n_crews = ceil(len(sites)/(avg_sites_per_day*avg_days_per_campaign))
    except KeyError:
        n_crews = 1
    return n_crews


def est_site_p_day(m, sites):
    """
    Estimate the number of sites a crew can survey in a day based on the average survey time
    , time between sites and the max workday.
    Args:
        m (dict): method parameters
        sites (dict): site dictionary
    Returns:
        int:estimated sites per day per crew.
    """
    def _s_per_day(s):
        # Calc sites per day based on single site parameters
        workday_aj = work_mins - int(choice(m['t_bw_sites']['vals']))
        t_per_site = int(choice(m['t_bw_sites']['vals'])) + int(s['{}_time'.format(m_name)])
        return workday_aj / t_per_site
    m_name = m['label']
    work_mins = m['max_workday']*60
    try:
        est_val = floor(average([_s_per_day(s) for s in sites]))
    except KeyError:
        est_val = 1
    return est_val
