"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        default_site_level_sensor
Purpose: The provides default behaviors for site level sensors

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

from typing import Union
from constants.sensor_constants import QuantificationTypes
from scheduling.schedule_dataclasses import SiteSurveyReport
from sensors.default_sensor import DefaultSensor
from virtual_world.emission_types.emission import Emission
from virtual_world.sites import Site
from constants.param_default_const import Levels


class DefaultSiteLevelSensor(DefaultSensor):
    SURVEY_LEVEL = Levels.SITE_LEVEL

    def __init__(
        self,
        mdl: Union[list[float], float],
        quantification_parameters: list[float],
        quantification_type: str = QuantificationTypes.DEFAULT.value,
    ) -> None:
        super().__init__(
            mdl,
            quantification_parameters,
            quantification_type,
        )

    def detect_emissions(self, site: Site, meth_name: str, survey_report: SiteSurveyReport) -> bool:
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

        emissions_detected: bool = self._rate_detected(site_level_emission_rate)

        if emissions_detected:
            site_level_measured_rate: float = self._measure_rate(site_level_emission_rate)
            for eq_emis_list in detectable_emissions.values():
                for emis_list in eq_emis_list.values():
                    for emission in emis_list:
                        emission.update_detection_records(
                            company=meth_name, detect_date=survey_report.survey_completion_date
                        )
        else:
            site_level_measured_rate: float = 0.0

        self._fill_detection_report(
            survey_report, site_level_emission_rate, site_level_measured_rate
        )
        return emissions_detected

    def _fill_detection_report(
        self,
        survey_report: SiteSurveyReport,
        true_site_rate: float,
        measured_site_rate: float,
    ) -> None:
        survey_report.site_true_rate = true_site_rate
        survey_report.site_measured_rate = measured_site_rate
        survey_report.survey_level = self.SURVEY_LEVEL
