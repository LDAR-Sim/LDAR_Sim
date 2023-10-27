import math
from typing import Literal


def check_relative_similarity(similarity, val, val_expected) -> Literal["Success", "Failure"]:
    """_summary_

    Args:
        similarity (_type_): The percent similarity in decimal number format
        to test that the value and expected are within.
        The value and the expected value must be within this percent similarity.
        For example: 0.1 is 10%.
        val (_type_): The value
        val_expected (_type_): The expected value

    Returns:
        Literal['Success', 'Failure']: Returns either "Success" or "Failure" based on if the value
        and the expected value are within "similarity" of each other
    """
    if math.isclose(val, val_expected, rel_tol=similarity):
        return "Success"
    return "Failure"
