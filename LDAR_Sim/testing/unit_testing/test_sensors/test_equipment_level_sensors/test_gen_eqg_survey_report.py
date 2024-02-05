from hypothesis import given, strategies as st
from src.scheduling.schedule_dataclasses import EquipmentGroupSurveyReport
from src.sensors.default_equipment_level_sensor import DefaultEquipmentLevelSensor


def get_sensor_for_default_equipment_level_sensor_testing() -> (
    DefaultEquipmentLevelSensor
):
    mdl: float = 1.0
    QE: float = 0.0
    return DefaultEquipmentLevelSensor(mdl=mdl, quantification_error=QE)


@st.composite
def gen_test_data(draw):
    measured_rate: float = draw(st.floats(min_value=0))
    true_rate: float = draw(st.floats(min_value=0))
    site_id: str = draw(st.text(min_size=1))
    eqg_id: str = draw(st.text(min_size=1))
    return site_id, eqg_id, true_rate, measured_rate


@given(test_data=gen_test_data())
def test_000_gen_equipment_survey_report_return_expected_report(test_data):
    sensor: DefaultEquipmentLevelSensor = (
        get_sensor_for_default_equipment_level_sensor_testing()
    )
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
