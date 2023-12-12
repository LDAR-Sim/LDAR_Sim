from virtual_world.emissions import Emission
from virtual_world.sites import Site


class DefaultSensor:
    def __init__(self, mdl: float) -> None:
        self._mdl: float = mdl

    def _emission_detected(self, emis: Emission) -> bool:
        if emis.get_rate() >= self._mdl:
            return True
        else:
            return False

    def detect_emissions(self, site: Site, meth_name: str):
        return
