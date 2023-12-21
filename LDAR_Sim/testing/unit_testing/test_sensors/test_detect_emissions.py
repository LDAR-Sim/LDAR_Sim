from scheduling.workplan import SiteSurveyReport
from sensors.default_site_level_sensor import DefaultSiteLevelSensor
from virtual_world.sites import Site
from testing.unit_testing.test_sensors.sensors_testing_fixtures import (  # noqa
    mock_site_emis_for_detect_emissions_testing_fix,
    mock_site_for_detect_emissions_testing_fix,
    sensor_info_for_default_site_level_sensor_construction_testing_fix,
)


def test_000_default_site_level_sensor_detect_emissions_detects_emissions_at_site_if_combined_rate_above_mdl(  # noqa
    sensor_info_for_default_site_level_sensor_construction_testing,
    mock_site_for_detect_emissions_testing,
) -> None:
    mock_site: Site = Site()
    mdl: float = sensor_info_for_default_site_level_sensor_construction_testing["mdl"]
    qe: float = sensor_info_for_default_site_level_sensor_construction_testing["QE"]
    sensor = DefaultSiteLevelSensor(mdl, qe)
    report: SiteSurveyReport = SiteSurveyReport(1)
    emis_detected: bool = sensor.detect_emissions(mock_site, "test", report)
    expected_emis = mock_site_for_detect_emissions_testing[1]
    assert emis_detected
    assert report.site_true_rate == expected_emis
    assert report.site_measured_rate == expected_emis
