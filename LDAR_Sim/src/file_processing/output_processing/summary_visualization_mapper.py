from matplotlib import ticker
from file_processing.output_processing import output_utils
from file_processing.output_processing.output_utils import percent_difference, relative_difference
from constants import output_file_constants


class SummaryVisualizationMapper:
    def __init__(self, site_count: int):
        self._summary_stat_functions = {
            (
                output_file_constants.SummaryVisualizationStatistics.PERCENT_DIFFERENCE
            ): percent_difference,
            (
                output_file_constants.SummaryVisualizationStatistics.RELATIVE_DIFFERENCE
            ): relative_difference,
        }

        self._histogram_properties_lookup = {
            output_file_constants.FileNames.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT: {
                "hist0": {
                    "bin_width": (
                        (
                            output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                        ).HISTOGRAM_BIN_WIDTH
                    ),
                    "bin_range": (
                        output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                    ).HISTOGRAM_PERCENT_DIFF_BIN_RANGE,
                    "x_label": output_file_constants.HistogramConstants.X_AXIS_LABEL_PERCENT,
                    "y_label": output_file_constants.HistogramConstants.Y_AXIS_LABEL,
                }
            },
            output_file_constants.FileNames.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT: {
                "hist0": {
                    "bin_width": (
                        (
                            output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                        ).HISTOGRAM_BIN_WIDTH
                    ),
                    "bin_range": (-100, None),
                    "x_label": output_file_constants.HistogramConstants.X_AXIS_LABEL_RELATIVE,
                    "y_label": output_file_constants.HistogramConstants.Y_AXIS_LABEL,
                    "x_locator": ticker.MaxNLocator(nbins="auto", prune=None),
                }
            },
            output_file_constants.FileNames.TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT: {
                "hist0": {
                    "x_label": output_file_constants.HistogramConstants.X_AXIS_LABEL_PAIRED.format(
                        n_sites=site_count
                    ),
                    "y_label": output_file_constants.HistogramConstants.Y_AXIS_LABEL,
                    "bins": output_file_constants.HistogramConstants.BINS,
                    "bin_range": (None, None),
                    "legend_label": (
                        output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                    ).TRUE_EMISSIONS_SUFFIX,
                },
                "hist1": {
                    "x_label": output_file_constants.HistogramConstants.X_AXIS_LABEL_PAIRED.format(
                        n_sites=site_count
                    ),
                    "y_label": output_file_constants.HistogramConstants.Y_AXIS_LABEL,
                    "bins": output_file_constants.HistogramConstants.BINS,
                    "bin_range": (None, None),
                    "legend_label": (
                        output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                    ).ESTIMATED_EMISSIONS_SUFFIX,
                },
            },
        }
        self._axis_formatter_lookup = {
            output_file_constants.FileNames.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT: (
                ticker.FuncFormatter(output_utils.percentage_formatter)
            ),
            output_file_constants.FileNames.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT: (
                ticker.FuncFormatter(output_utils.percentage_formatter)
            ),
        }

        self._probit_properties_lookup = {
            output_file_constants.FileNames.TRUE_AND_ESTIMATED_PAIRED_PROBIT_PLOT: {
                "probit0": {
                    "x_label": output_file_constants.ProbitConstants.X_AXIS_LABEL.format(
                        n_sites=site_count
                    ),
                    "y_label": output_file_constants.ProbitConstants.Y_AXIS_LABEL.format(
                        n_sites=site_count
                    ),
                    "legend_label": (
                        output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                    ).TRUE_EMISSIONS_SUFFIX,
                },
                "probit1": {
                    "x_label": output_file_constants.ProbitConstants.X_AXIS_LABEL.format(
                        n_sites=site_count
                    ),
                    "y_label": output_file_constants.ProbitConstants.Y_AXIS_LABEL.format(
                        n_sites=site_count
                    ),
                    "legend_label": (
                        output_file_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
                    ).ESTIMATED_EMISSIONS_SUFFIX,
                },
            }
        }

    def get_summary_stat_function(self, stat_type: str):
        return self._summary_stat_functions.get(stat_type)

    def get_histogram_properties(self, visualization_name: str):
        return self._histogram_properties_lookup.get(visualization_name)

    def get_probit_properties(self, visualization_name: str):
        return self._probit_properties_lookup.get(visualization_name)

    def get_x_axis_formatter(self, visualization_name: str):
        return self._axis_formatter_lookup.get(visualization_name)
