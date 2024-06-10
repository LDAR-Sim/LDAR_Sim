"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        uniform_quantification_predictor.py
Purpose: The provides an emissions quantification predictor that uses a uniform distribution

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


class UniformQuantificationPredictor:
    """
    A class representing a uniform quantification predictor.

    Attributes:
        _upper_range (float): The upper range of the quantification 95% confidence interval.
        _lower_range (float): The lower range of the quantification 95% confidence interval.


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

        self._upper_range = quantification_95_percent_ci_upper_range
        self._lower_range = quantification_95_percent_ci_lower_range

    def predict(self, true_rate: float) -> float:
        """
        Predicts the quantified rate based on a given true rate.

        Args:
            true_rate (float): The true rate.

        Returns:
            float: The predicted quantified rate.
        """
        quantification_shift: float = np.random.uniform(self._lower_range, self._upper_range)
        return true_rate + true_rate * quantification_shift
