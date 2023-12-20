import numpy as np
from virtual_world.sites import Site


class DefaultSensor:
    def __init__(self, mdl: float, quantification_error: float) -> None:
        self._mdl: float = mdl
        self._quantification_error: float = quantification_error

    def _rate_detected(self, emis_rate: float) -> bool:
        return emis_rate >= self._mdl

    def detect_emissions(self, site: Site, meth_name: str):
        return

    def _measure_site_rate(self, true_site_rate: float) -> float:
        quant_error: float = np.random.normal(0, self._quantification_error)

        measured_rate = None
        if quant_error >= 0:
            measured_rate: float = true_site_rate + true_site_rate * quant_error
        if quant_error < 0:
            denom: float = abs(quant_error - 1)
            measured_rate: float = true_site_rate / denom

        return measured_rate
