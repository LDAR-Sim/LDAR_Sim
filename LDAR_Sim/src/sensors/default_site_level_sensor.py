from sensors.default_sensor import DefaultSensor
from virtual_world.emissions import Emission
from virtual_world.sites import Site


class DefaultSiteLevelSensor(DefaultSensor):
    SURVEY_LEVEL = "site_level"

    def __init__(self, mdl: float) -> None:
        super().__init__(mdl)

    def detect_emissions(self, site: Site, meth_name: str):
        # TODO update and test this functionality
        detectable_emissions: dict[str, dict[str, list[Emission]]] = site.get_detectable_emissions(
            method_name=meth_name
        )
        site_level_emission_rate: float = sum(
            [
                emission.get_rate()
                for eq_emis_list in detectable_emissions.values()
                for emis_list in eq_emis_list.values()
                for emission in emis_list
            ]
        )

        if self._emission_detected(site_level_emission_rate):
            emissions_detected: bool = True
        else:
            emissions_detected: bool = False

        return self._gen_detection_report(site_level_emission_rate, emissions_detected)
