from typing import Any, Tuple
from hypothesis import given, strategies as st
from scheduling.workplan import SiteSurveyReport
from sensors.default_site_level_sensor import DefaultSiteLevelSensor
from testing.unit_testing.test_sensors.sensors_testing_fixtures import (  # noqa
    sensor_for_default_site_level_sensor_testing_fix,
)


@st.composite
def gen_measured_and_true_rates(draw) -> Tuple[Any | float, Any | int]:
    site_true_rate: float = draw(st.floats(min_value=0))
    site_measured_rate: float = draw(st.floats(min_value=0))
    return site_true_rate, site_measured_rate


@given(gen_data=gen_measured_and_true_rates())
def test_000_default_sl_sensor_fill_detection_report_with_successful_detection_correctly_fills_values(  # noqa
    sensor_for_default_site_level_sensor_testing: DefaultSiteLevelSensor, gen_data
) -> None:
    report: SiteSurveyReport = SiteSurveyReport()
    site_true_rate: float = gen_data[0]
    site_measured_rate: float = gen_data[1]
    sensor_for_default_site_level_sensor_testing._fill_detection_report(
        report, site_true_rate, site_measured_rate
    )
    assert report.site_measured_rate == site_measured_rate
    assert report.site_true_rate == site_true_rate
