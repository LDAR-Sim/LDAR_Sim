"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        emissions_source_processing
Purpose: Module for processing User defined emissions sources

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

from typing import Any
from pandas import DataFrame
import scipy.stats
import json


def read_in_emissions_sources_file(
    virtual_world: dict,
) -> DataFrame:  # TODO: this should also allow from subtype file...
    """Get the location for the emissions sources file and read the file into a pandas DataFrame

    Args

    Returns

    """
    virtual_world["emissions"]["emissions_file"]
    return None


def process_emission_source_file(emiss_source: DataFrame) -> dict[str, Any]:
    """Process the given emissions sources DataFrame in order to
    set up the correct emissions sources types.

    Emissions sources of the sample type will be set up as a list of sample values,

    Emissions sources of the fit type will be set up as a scipy distribution object,

    Emissions sources of the distribution type will be set up as a scipy distribution object.

    Args:
        emiss_source (DataFrame): _description_

    Returns:
        dict[str, (List or scipy dist obj)]: _description_
    """

    return None


def process_emiss_samples_as_dist(emiss_source: list[float]) -> scipy.stats.rv_continuous:
    """
    Process the given emission source sample List and fit into
    a scipy distribution object

    Args:
        emiss_source (list): the emissions DataFrame

    Returns:
        scipy object
    """
    if emiss_source is None or not emiss_source:
        raise ValueError("emiss_source must be a non-empty list of samples")

    # Initialize a lognormal distribution
    dist = scipy.stats.lognorm()

    try:
        # Attempt to fit the samples to the distribution
        param = dist.fit(emiss_source, floc=0)
    except Exception as e:
        # Handle exceptions during fitting
        print(f"Error fitting distribution: {e}")
        return None

    loc = param[-2]
    scale = param[-1]
    shape = param[:-2]

    if isinstance(shape, str):
        # If shape is a string, convert it to a Python object (int or list)
        shape = json.loads(shape)

    if not isinstance(shape, list):
        # If the shape is not a list, convert it to a list
        shape = [shape]

    # Return a distribution object with the fitted parameters
    return dist(*shape, loc=loc, scale=scale)
