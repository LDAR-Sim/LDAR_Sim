from typing import Any, Tuple
from hypothesis import given, strategies as st
from src.scheduling.schedule_dataclasses import SiteSurveyReport
from src.sensors.default_site_level_sensor import DefaultSiteLevelSensor


def get_sensor_for_default_site_level_sensor_testing() -> DefaultSiteLevelSensor:
    mdl: float = 1.0
    QE: float = 0.0
    return DefaultSiteLevelSensor(mdl=mdl, quantification_error=QE)


@st.composite
def gen_measured_and_true_rates(draw) -> Tuple[Any | float, Any | int]:
    site_true_rate: float = draw(st.floats(min_value=0))
    site_measured_rate: float = draw(st.floats(min_value=0))
    return site_true_rate, site_measured_rate


@given(gen_data=gen_measured_and_true_rates())
def test_000_default_sl_sensor_fill_detection_report_with_successful_detection_correctly_fills_values(  # noqa
    gen_data,
) -> None:
    sensor: DefaultSiteLevelSensor = get_sensor_for_default_site_level_sensor_testing()
    report: SiteSurveyReport = SiteSurveyReport(1)
    site_true_rate: float = gen_data[0]
    site_measured_rate: float = gen_data[1]
    sensor._fill_detection_report(report, site_true_rate, site_measured_rate)
    assert report.site_measured_rate == site_measured_rate
    assert report.site_true_rate == site_true_rate
