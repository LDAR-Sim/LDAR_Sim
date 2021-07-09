from geography.distance import get_distance


def find_homebase(cur_lat, cur_lon, homebase_locs):
    '''
    Find the nearest home base from home bases list
    Parameters
    ----------
    cur_lat, and cur_lon contains longitude and latitude of the current crew location
    homebase_locs : A list that includes latitudes and longitudes of all home bases

    Returns
    -------
    The latitude and longitude of nearest home base and the distance to that home base in km.
    '''
    distances = []
    for lonlat in homebase_locs:
        hb_lon = lonlat[0]
        hb_lat = lonlat[1]
        d = get_distance(cur_lat, cur_lon, hb_lat, hb_lon, "Haversine")
        distances.append(d)
    dist = min(distances)
    ind = distances.index(dist)
    return (homebase_locs[ind], dist)


def find_homebase_opt(x1, y1, x2, y2, HX, HY):
    '''
    Find the home base that nearest to both LDAR team and next visit facility.
    Parameters
    ----------
    x1 and y1 are longitude and latitude of the current location of LDAR crew
    x2 and y2 are longitude and latitude of the next visit facility
    HX : A list that includes longitudes of all home bases
    HY : A list that includes latitudes of all home bases

    Returns
    -------
    The latitude and longitude of nearest home base and the distance to that home base in km.
    '''
    XY = list(zip(HX, HY))
    xy2 = (x2, y2)
    if xy2 in XY:
        ind = XY.index(xy2)
        XY.pop(ind)
    D = []
    for xy in XY:
        x3 = xy[0]
        y3 = xy[1]
        d1 = get_distance(x1, y1, x3, y3, "Haversine")
        d2 = get_distance(x1, y1, x2, y2, "Haversine")
        d = d1 + d2
        D.append(d)
    dist = min(D)
    ind = D.index(dist)
    return (XY[ind], dist)
