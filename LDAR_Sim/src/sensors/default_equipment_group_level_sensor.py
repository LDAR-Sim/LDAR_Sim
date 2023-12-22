from scheduling.workplan import EquipmentGroupSurveyReport, SiteSurveyReport
from sensors.default_sensor import DefaultSensor
from virtual_world.emissions import Emission
from virtual_world.sites import Site


class DefaultEquipmentGroupLevelSensor(DefaultSensor):
    SURVEY_LEVEL = "equipment_group_level"

    def __init__(self, mdl: float, quantification_error: float) -> None:
        super().__init__(mdl, quantification_error)

    def detect_emissions(self, site: Site, meth_name: str, survey_report: SiteSurveyReport) -> bool:
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

        emissions_detected: bool = self._rate_detected(site_level_emission_rate)

        if emissions_detected:
            site_level_measured_rate: float = self._measure_rate(site_level_emission_rate)
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
        eqg_survey_reports: list[EquipmentGroupSurveyReport],
    ) -> None:
        survey_report.site_true_rate = true_site_rate
        survey_report.site_measured_rate = measured_site_rate
        survey_report.survey_level = self.SURVEY_LEVEL
        survey_report.equipment_groups_surveyed = eqg_survey_reports

    def _gen_eqg_survey_report(
        self, site_id: str, eqg_id: str, true_rate: float, measured_rate: float
    ) -> EquipmentGroupSurveyReport:
        eqg_survey_report: EquipmentGroupSurveyReport = EquipmentGroupSurveyReport(
            site_id, eqg_id, measured_rate=measured_rate, true_rate=true_rate
        )
        return eqg_survey_report
