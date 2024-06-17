from hypothesis import given, strategies as st
from src.scheduling.schedule_dataclasses import EquipmentGroupSurveyReport
from src.sensors.default_equipment_group_level_sensor import (
    DefaultEquipmentGroupLevelSensor,
)


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
def gen_test_data(draw):
    measured_rate: float = draw(st.floats(min_value=0))
    true_rate: float = draw(st.floats(min_value=0))
    site_id: str = draw(st.text(min_size=1))
    eqg_id: str = draw(st.text(min_size=1))
    return site_id, eqg_id, true_rate, measured_rate


@given(test_data=gen_test_data())
def test_000_gen_eqg_survey_report_return_expected_report(test_data):
    sensor: DefaultEquipmentGroupLevelSensor = get_sensor_for_default_eqg_level_sensor_testing()
    site_id: str = test_data[0]
    eqg_id: str = test_data[1]
    meas_rate: float = test_data[3]
    true_rate: float = test_data[2]
    report: EquipmentGroupSurveyReport = sensor._gen_eqg_survey_report(
        site_id, eqg_id, true_rate=true_rate, measured_rate=meas_rate
    )
    assert [] == report.emissions_detected
    assert meas_rate == report.measured_rate
    assert true_rate == report.true_rate
    assert site_id == report.site
    assert eqg_id == report.equipment_group
