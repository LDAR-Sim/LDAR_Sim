# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        geography.distance
# Purpose:     Calculate distance between two coordinates
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

import numpy as np


def get_distance(lon1, lat1, lon2, lat2, calc_method):
    """
    A function that calculate different types of distance between two points

    Parameters
    ----------
    lat1 : latitude 1
    lon1 : longitude 1
    lat2 : latitude 2
    lon2 : longitude 2
    calc_method : Types of distance metrics

    Returns a distance in km

    """
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    if calc_method == "Euclidean":
        d = ((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2) ** 0.5
    elif calc_method == "Haversine":
        radius = 6371.0
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat / 2.0) * np.sin(dlat / 2.0) + np.cos(np.radians(lat1)) * np.cos(
            np.radians(lat2)
        ) * np.sin(dlon / 2.0) * np.sin(dlon / 2.0)
        c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
        d = radius * c
    elif calc_method == "route":
        # HBD - To be added a later date
        d = 100
    return d
