from sensors.default_sensor import DefaultSensor
from virtual_world.sites import Site


class DefaultSiteLevelSensor(DefaultSensor):
    SURVEY_LEVEL = "site_level"

    def __init__(self, mdl: float) -> None:
        super().__init__(mdl)

    def detect_emissions(self, site: Site, meth_name: str):
        # TODO update and test this functionality
        emissions = site.get_detectable_emissions(
            method_name=meth_name, survey_level=self.SURVEY_LEVEL
        )
        for emission in emissions:
            self._emission_detected(emission)
