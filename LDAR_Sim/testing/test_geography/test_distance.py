"""Module for testing distance"""
from src.geography.distance import get_distance


def test_002_dist_euclidean():
    """ Test Euclidean """
    expected = 2**0.5
    lat1 = 3
    lon1 = 2

    lat2 = 4
    lon2 = 1
    d = get_distance(lat1, lon1, lat2, lon2, "Euclidean")
    assert d == expected


def test_002_dist_haversine():
    """ Test Haversine """
    expected = 5897.658
    lat1 = -0.116773
    lon1 = 51.510357

    lat2 = -77.009003
    lon2 = 38.889931
    d = get_distance(lat1, lon1, lat2, lon2, "Haversine")
    assert round(d, 3) == expected
