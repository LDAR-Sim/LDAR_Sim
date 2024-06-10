from pytest import approx
from src.scheduling.schedule_dataclasses import SiteSurveyReport, EmissionDetectionReport
from sensors.default_component_level_sensor import DefaultComponentLevelSensor
from src.virtual_world.sites import Site
from testing.unit_testing.test_sensors.test_equipment_level_sensors.equipment_level_sensors_testing_fixtures import (  # noqa
    mock_site_emis_for_equip_level_detect_emissions_testing_fix,
    mock_site_emis_for_equip_level_detect_emissions_testing_lower_emis_fix,
    mock_site_for_equip_level_detect_emissions_testing_fix,
    mock_site_for_equip_level_detect_emissions_testing_lower_emissions_fix,
    sensor_info_for_default_equipment_level_sensor_construction_testing_fix,
    sensor_info_high_mdl_for_default_equipment_level_sensor_testing_fix,
    mock_site_emis_for_equip_level_detect_emissions_testing_mixed_detect_fix,
    mock_site_for_equip_level_detect_emissions_testing_mixed_detect_fix,
)
from constants import param_default_const as pdc


def compare_reports(expected, result) -> bool:
    match: bool = True
    for exp_prop, res_prop in zip(expected.__dict__, result.__dict__):
        if isinstance(exp_prop, float):
            if not exp_prop == approx(res_prop):
                match = False
        elif isinstance(expected, EmissionDetectionReport):
            if not compare_reports(EmissionDetectionReport):
                match = False
        else:
            if not exp_prop == res_prop:
                match = False
    return match


def test_000_default_equip_level_sensor_detect_emissions_detects_emissions_at_site_if_combined_rate_above_mdl(  # noqa
    sensor_info_for_default_equipment_level_sensor_construction_testing: dict[str, int],
    mock_site_for_equip_level_detect_emissions_testing,
) -> None:
    mock_site: Site = Site()
    mdl: float = sensor_info_for_default_equipment_level_sensor_construction_testing[
        pdc.Method_Params.MDL
    ]
    qe: float = sensor_info_for_default_equipment_level_sensor_construction_testing[
        pdc.Method_Params.QE
    ]
    sensor = DefaultComponentLevelSensor(
        mdl, qe[pdc.Method_Params.Q5], qe[pdc.Method_Params.Q95], qe[pdc.Method_Params.Q_TYPE]
    )
    report: SiteSurveyReport = SiteSurveyReport(1)
    emis_detected: bool = sensor.detect_emissions(mock_site, "test", report)
    expected_emis = mock_site_for_equip_level_detect_emissions_testing[1]
    expected_eqg_srv_results = mock_site_for_equip_level_detect_emissions_testing[2]
    assert emis_detected
    assert expected_emis == report.site_true_rate
    assert expected_emis == report.site_measured_rate
    assert len(expected_eqg_srv_results) == len(report.equipment_groups_surveyed)
    for expected, result in zip(expected_eqg_srv_results, report.equipment_groups_surveyed):
        assert compare_reports(expected, result)


def test_000_default_equip_level_sensor_detect_emissions_does_not_detect_emissions_at_site_if_combined_rate_below_mdl(  # noqa
    sensor_info_high_mdl_for_default_equipment_level_sensor_testing,
    mock_site_for_equip_level_detect_emissions_testing_lower_emissions,
) -> None:
    mock_site: Site = Site()
    mdl: float = sensor_info_high_mdl_for_default_equipment_level_sensor_testing[
        pdc.Method_Params.MDL
    ]
    qe: float = sensor_info_high_mdl_for_default_equipment_level_sensor_testing[
        pdc.Method_Params.QE
    ]
    sensor = DefaultComponentLevelSensor(
        mdl, qe[pdc.Method_Params.Q5], qe[pdc.Method_Params.Q95], qe[pdc.Method_Params.Q_TYPE]
    )
    report: SiteSurveyReport = SiteSurveyReport(1)
    emis_detected: bool = sensor.detect_emissions(mock_site, "test", report)
    expected_true_emis = mock_site_for_equip_level_detect_emissions_testing_lower_emissions[1]
    expected_measured_emis = mock_site_for_equip_level_detect_emissions_testing_lower_emissions[2]
    expected_eqg_srv_results = mock_site_for_equip_level_detect_emissions_testing_lower_emissions[3]
    assert not emis_detected
    assert expected_true_emis == approx(report.site_true_rate)
    assert expected_measured_emis == approx(report.site_measured_rate)
    assert len(expected_eqg_srv_results) == len(report.equipment_groups_surveyed)
    for expected, result in zip(expected_eqg_srv_results, report.equipment_groups_surveyed):
        assert compare_reports(expected, result)


def test_000_default_eqg_level_sensor_detect_emissions_correctly_detects_only_emissions_at_eqgs_above_MDL(  # noqa
    sensor_info_high_mdl_for_default_equipment_level_sensor_testing,
    mock_site_for_equip_level_detect_emissions_testing_mixed_detect,
) -> None:
    mock_site: Site = Site()
    mdl: float = sensor_info_high_mdl_for_default_equipment_level_sensor_testing[
        pdc.Method_Params.MDL
    ]
    qe: float = sensor_info_high_mdl_for_default_equipment_level_sensor_testing[
        pdc.Method_Params.QE
    ]
    sensor = DefaultComponentLevelSensor(
        mdl, qe[pdc.Method_Params.Q5], qe[pdc.Method_Params.Q95], qe[pdc.Method_Params.Q_TYPE]
    )
    report: SiteSurveyReport = SiteSurveyReport(1)
    emis_detected: bool = sensor.detect_emissions(mock_site, "test", report)
    expected_true_emis = mock_site_for_equip_level_detect_emissions_testing_mixed_detect[1]
    expected_measured_emis = mock_site_for_equip_level_detect_emissions_testing_mixed_detect[2]
    expected_eqg_srv_results = mock_site_for_equip_level_detect_emissions_testing_mixed_detect[3]
    assert emis_detected
    assert expected_true_emis == approx(report.site_true_rate)
    assert expected_measured_emis == approx(report.site_measured_rate)
    assert len(expected_eqg_srv_results) == len(report.equipment_groups_surveyed)
    for expected, result in zip(expected_eqg_srv_results, report.equipment_groups_surveyed):
        assert compare_reports(expected, result)
