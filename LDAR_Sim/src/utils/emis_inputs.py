# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        utils.emis_inputs
# Purpose:     Store subtype level emissions input data
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
import pandas as pd


def assign_vents(program, wd) -> None:
    """Assign empirical venting rates to each subtype based on the subtype vent_rates_files

    Args:
        program (dict): The program dictionary storing all the program specific information
        wd (Path): The path to the current working directory
    """
    for st_idx, subtype in program["subtypes"].items():
        if "vent_rates_file" in subtype:
            subtype["empirical_vent_rates"] = np.array(
                pd.read_csv(wd / subtype["vent_rates_file"]).iloc[:, 0]
            )
