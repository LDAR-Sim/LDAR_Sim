import numpy as np


def get_distance(location1, location2, calc_method):
    '''
    A function that calculate different types of distance between two points

    Parameters
    ----------
    x1 : longitude 1
    y1 : latitude 1
    x2 : longitude 2
    y2 : latitude 2
    calc_method : Types of distance metrics

    Returns a distance in km

    '''
    y1, x1 = location1
    y2, x2 = location2
    if calc_method == "Euclidean":
        d = ((x1 - x2)**2 + (y1-y2)**2)**0.5
    elif calc_method == "Haversine":
        radius = 6371.0
        dlat = np.radians(y2 - y1)
        dlon = np.radians(x2 - x1)
        a = (np.sin(dlat / 2.0) * np.sin(dlat / 2.0) +
             np.cos(np.radians(y1)) * np.cos(np.radians(y2)) *
             np.sin(dlon / 2.0) * np.sin(dlon / 2.0))
        c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
        d = radius * c
    elif calc_method == "route":
        # HBD - To be added a later date
        d = 100
    return d
