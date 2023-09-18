from geography.distance import get_distance

# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        geography.homebase
# Purpose:     Find nearest homebase
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


def find_homebase(lon, lat, homebase_locs):
    '''
    Find the nearest home base from home bases list
    Parameters
    ----------
    lon, and lat contains longitude and latitude of the current crew location
    homebase_locs : A list that includes latitudes and longitudes of all home bases

    Returns
    -------
    The latitude and longitude of nearest home base and the distance to that home base in km.
    '''
    distances = []
    for lonlat in homebase_locs:
        hb_lon = lonlat[0]
        hb_lat = lonlat[1]
        d = get_distance(lon, lat, hb_lon, hb_lat, "Haversine")
        distances.append(d)
    dist = min(distances)
    ind = distances.index(dist)
    return (homebase_locs[ind], dist)


def find_homebase_opt(lon1, lat1, lon2, lat2, homebase_locs):
    '''
    Find the home base that nearest to both LDAR team and next visit facility.
    Parameters
    ----------
    lon1 and lat1 are longitude and latitude of the current location of LDAR crew
    lon2 and lat2 are longitude and latitude of the next visit facility
    homebase_locs : A list that includes latitudes and longitudes of all home bases

    Returns
    -------
    The latitude and longitude of nearest home base and the distance to that home base in km.
    '''
    xy2 = (lon2, lat2)
    if xy2 in homebase_locs:
        ind = homebase_locs.index(xy2)
        homebase_locs.pop(ind)
    D = []
    for xy in homebase_locs:
        lon3 = xy[0]
        lat3 = xy[1]
        d1 = get_distance(lon1, lat1, lon3, lat3, "Haversine")
        d2 = get_distance(lon1, lat1, lon2, lat2, "Haversine")
        d = d1 + d2
        D.append(d)
    dist = min(D)
    ind = D.index(dist)
    return (homebase_locs[ind], dist)
