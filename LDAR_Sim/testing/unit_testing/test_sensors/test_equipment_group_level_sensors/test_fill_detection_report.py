from typing import Any, Tuple
from hypothesis import given, strategies as st
from src.scheduling.schedule_dataclasses import SiteSurveyReport, EquipmentGroupSurveyReport
from src.sensors.default_equipment_group_level_sensor import DefaultEquipmentGroupLevelSensor


def get_sensor_for_default_eqg_level_sensor_testing() -> DefaultEquipmentGroupLevelSensor:
    mdl: float = 1.0
    quantification_parameters: list[float] = [0.0, 0.0]
    quantification_type: str = "default"
    return DefaultEquipmentGroupLevelSensor(
        mdl=mdl,
        quantification_parameters=quantification_parameters,
        quantification_type=quantification_type,
    )


@st.composite
def gen_measured_and_true_rates(draw) -> Tuple[Any | float, Any | int]:
    eqg_count: int = draw(st.integers(min_value=1, max_value=100))
    eqg_rates: dict[str, Tuple[float, float]] = {}
    for eqg in range(eqg_count):
        eqg_true_rate: float = draw(st.floats(min_value=0))
        eqg_measured_rate: float = draw(st.floats(min_value=0))
        eqg_rates[str(eqg)] = (eqg_true_rate, eqg_measured_rate)

    site_true_rate: float = sum(eqg_rate_vals[0] for eqg_rate_vals in eqg_rates.values())
    site_measured_rate: float = sum(eqg_rate_vals[1] for eqg_rate_vals in eqg_rates.values())

    return site_true_rate, site_measured_rate, eqg_rates


@given(gen_data=gen_measured_and_true_rates())
def test_000_default_sl_sensor_fill_detection_report_with_successful_detection_correctly_fills_values(  # noqa
    gen_data,
) -> None:
    sensor: DefaultEquipmentGroupLevelSensor = get_sensor_for_default_eqg_level_sensor_testing()
    report: SiteSurveyReport = SiteSurveyReport(1)
    site_true_rate: float = gen_data[0]
    site_measured_rate: float = gen_data[1]
    eqg_rates: dict[str, Tuple[float, float]] = gen_data[2]
    eqg_detection_results: list[EquipmentGroupSurveyReport] = []
    for eqg, rates in eqg_rates.items():
        eqg_detection_results.append(EquipmentGroupSurveyReport(1, eqg, rates[0], rates[1]))
    sensor._fill_detection_report(report, site_true_rate, site_measured_rate, eqg_detection_results)
    assert report.site_measured_rate == site_measured_rate
    assert report.site_true_rate == site_true_rate
    assert len(eqg_rates) == len(report.equipment_groups_surveyed)
