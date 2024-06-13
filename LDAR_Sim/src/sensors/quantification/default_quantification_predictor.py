"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        default_quantification_predictor.py
Purpose: The provides default behaviors for emissions quantification

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

import numpy as np


class DefaultQuantificationPredictor:
    """
    A class representing a default quantification predictor.

    Attributes:
        _quantification_standard_deviation (float): The standard deviation of
        the quantification 95% confidence interval.
        _quantification_centre (float): The centre/mean of the quantification shift.

    Methods:
        predict(true_rate):
            Predicts the quantified rate for a given true rate.
    """

    def __init__(
        self,
        quantification_95_percent_ci_lower_range: float,
        quantification_95_percent_ci_upper_range: float,
    ):
        """
        Initializes a new instance of the UniformQuantificationPredictor class.

        Args:
            quantification_95_percent_ci_lower_range (float): The lower range of the
            quantification 95% confidence interval.
            quantification_95_percent_ci_upper_range (float): The upper range of the
            quantification 95% confidence interval.

        """
        quantification_95_percent_ci_width: float = abs(
            quantification_95_percent_ci_upper_range - quantification_95_percent_ci_lower_range
        )
        # We assume the empirical rule that 95% of the data lies within 2
        # standard deviations of the mean. This means that u-2s = lower bound
        # and u+2s = upper bound, where u is the mean and s is the standard deviation.
        # Therefore, we can calculate the standard deviation s = (upper bound - lower bound) / 4
        self._quantification_standard_deviation: float = quantification_95_percent_ci_width / 4.0

        self._quantification_centre: float = (
            quantification_95_percent_ci_upper_range + quantification_95_percent_ci_lower_range
        ) / 2.0

    def predict(self, true_rate: float) -> float:
        """
        Predicts the quantified rate based on a given true rate.

        Args:
            true_rate (float): The true rate.

        Returns:
            float: The predicted quantified rate.
        """
        quantification_shift: float = np.random.normal(
            loc=self._quantification_centre, scale=self._quantification_standard_deviation
        )
        return true_rate * (1 + (quantification_shift / 100))
