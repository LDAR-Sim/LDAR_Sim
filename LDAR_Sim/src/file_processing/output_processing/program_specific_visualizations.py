from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from file_processing.output_processing.output_visualization_constants import ProgTsConstants as pts
from file_processing.output_processing.output_utils import TIMESERIES_COL_ACCESSORS as tca


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
    return
