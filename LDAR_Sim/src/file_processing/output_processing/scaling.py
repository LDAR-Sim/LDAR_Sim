import matplotlib.scale as mscale
import matplotlib.ticker
import numpy as np
from scipy import stats


class QuantileFormatter(matplotlib.ticker.Formatter):
    def __call__(self, x, pos=None):
        formatted_number = "{:.2f}".format((1 - x) * 100)
        return formatted_number


class QuantileScale(mscale.ScaleBase):
    name = "quantile"

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self, axis)
        self.dist = stats.distributions.norm
        self._transform = self.ProbabilityTransform()

    def _get_quantiles(self):
        return np.array([1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 99]) / 100.0

    def get_transform(self):
        return self._transform

    def set_default_locators_and_formatters(self, axis) -> None:
        axis.set_major_locator(matplotlib.ticker.FixedLocator(self._get_quantiles()))
        axis.set_major_formatter(matplotlib.ticker.FuncFormatter(QuantileFormatter()))
        axis.set_minor_locator(matplotlib.ticker.NullLocator())
        axis.set_minor_formatter(matplotlib.ticker.NullFormatter())

    class ProbabilityTransform(mscale.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True
        has_inverse = True

        def transform_non_affine(self, a):
            a = np.ma.masked_where(~np.isfinite(a), a)
            return np.ma.filled(stats.norm.ppf(a), -np.inf)

        def inverted(self):
            return QuantileScale.QuantileTransform()

    class QuantileTransform(mscale.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True
        has_inverse = True

        def transform_non_affine(self, a):
            a = np.ma.masked_invalid(a)
            return np.ma.filled(stats.norm.cdf(a), 0.0)

        def inverted(self):
            return QuantileScale.ProbabilityTransform()
