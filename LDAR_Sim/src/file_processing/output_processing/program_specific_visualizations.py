"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        program_specific_visualizations.py
Purpose: Contains functions to generate program-specific visualizations.

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

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from constants.output_file_constants import ProgTsConstants as pts, TIMESERIES_COL_ACCESSORS as tca


def gen_prog_timeseries_plot(timeseries: pd.DataFrame, ts_filepath: Path, name_str: str):
    x_data = timeseries[tca.DATE]
    y_data = timeseries[tca.EMIS]
    plt.plot(x_data, y_data)

    # Add title and labels
    plt.title(pts.TITLE.format(name_str=name_str))
    plt.xlabel(pts.X_AXIS_TITLE)
    plt.ylabel(pts.Y_AXIS_TITLE)

    complete_filename: str = "_".join([name_str, pts.FILENAME])
    complete_filepath = ts_filepath / complete_filename

    plt.savefig(complete_filepath)
    plt.close()
    return
