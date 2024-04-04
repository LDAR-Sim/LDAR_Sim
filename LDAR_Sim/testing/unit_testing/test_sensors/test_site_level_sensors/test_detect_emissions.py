from pytest import approx
from src.scheduling.schedule_dataclasses import SiteSurveyReport
from src.sensors.default_site_level_sensor import DefaultSiteLevelSensor
from src.virtual_world.sites import Site
from testing.unit_testing.test_sensors.test_site_level_sensors.site_level_sensors_testing_fixtures import (  # noqa
    mock_site_emis_for_detect_emissions_testing_fix,
    mock_site_for_detect_emissions_testing_fix,
    sensor_info_for_default_equipment_group_level_sensor_construction_testing_fix,
    sensor_info_high_mdl_for_default_site_level_sensor_testing_fix,
    mock_site_emis_for_detect_emissions_testing_lower_emis_fix,
    mock_site_for_detect_emissions_testing_lower_emissions_fix,
)


def test_000_default_site_level_sensor_detect_emissions_detects_emissions_at_site_if_combined_rate_above_mdl(  # noqa
    sensor_info_for_default_equipment_group_level_sensor_construction_testing: dict[str, int],
    mock_site_for_detect_emissions_testing,
) -> None:
    mock_site: Site = Site()
    mdl: float = sensor_info_for_default_equipment_group_level_sensor_construction_testing["mdl"]
    qe: float = sensor_info_for_default_equipment_group_level_sensor_construction_testing["QE"]
    sensor = DefaultSiteLevelSensor([mdl], qe)
    report: SiteSurveyReport = SiteSurveyReport(1)
    emis_detected: bool = sensor.detect_emissions(mock_site, "test", report)
    expected_emis = mock_site_for_detect_emissions_testing[1]
    assert emis_detected
    assert expected_emis == report.site_true_rate
    assert expected_emis == report.site_measured_rate


def test_000_default_site_level_sensor_detect_emissions_does_not_detect_emissions_at_site_if_combined_rate_below_mdl(  # noqa
    sensor_info_high_mdl_for_default_site_level_sensor_testing,
    mock_site_for_detect_emissions_testing_lower_emissions,
) -> None:
    mock_site: Site = Site()
    mdl: float = sensor_info_high_mdl_for_default_site_level_sensor_testing["mdl"]
    qe: float = sensor_info_high_mdl_for_default_site_level_sensor_testing["QE"]
    sensor = DefaultSiteLevelSensor(mdl, qe)
    report: SiteSurveyReport = SiteSurveyReport(1)
    emis_detected: bool = sensor.detect_emissions(mock_site, "test", report)
    expected_true_emis = mock_site_for_detect_emissions_testing_lower_emissions[1]
    expected_measured_emis = mock_site_for_detect_emissions_testing_lower_emissions[2]
    assert not emis_detected
    assert expected_true_emis == approx(report.site_true_rate)
    assert expected_measured_emis == approx(report.site_measured_rate)
