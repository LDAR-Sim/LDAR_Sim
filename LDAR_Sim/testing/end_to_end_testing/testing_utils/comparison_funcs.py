import math


def check_relative_similarity(similarity, val, val_expected):
    if math.isclose(val, val_expected, rel_tol=similarity):
        return "Success"
    return "Failure"
