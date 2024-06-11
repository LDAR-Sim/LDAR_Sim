from hypothesis import given, strategies as st
from src.scheduling.schedule_dataclasses import EmissionDetectionReport, EquipmentGroupSurveyReport
from sensors.default_component_level_sensor import DefaultComponentLevelSensor


def get_sensor_for_default_equipment_level_sensor_testing() -> DefaultComponentLevelSensor:
    mdl: float = [1.0]
    quantification_parameters: list[float] = [0.0, 0.0]
    quantification_type: str = "default"
    return DefaultComponentLevelSensor(
        mdl=mdl,
        quantification_parameters=quantification_parameters,
        quantification_type=quantification_type,
    )


generate_emission_detection_reports_strategy: st.SearchStrategy = st.builds(
    EmissionDetectionReport,
    site=st.text(min_size=1),
    equipment_group=st.text(min_size=1),
    component=st.text(min_size=1),
    true_rate=st.floats(min_value=0),
    measured_rate=st.floats(min_value=0),
)


measured_rate_strategy: st.SearchStrategy = st.floats(min_value=0)
true_rate_strategy: st.SearchStrategy = st.floats(min_value=0)
site_id_strategy: st.SearchStrategy = st.text(min_size=1)
eqg_id_strategy: st.SearchStrategy = st.text(min_size=1)


gen_test_data = st.tuples(
    site_id_strategy,
    eqg_id_strategy,
    measured_rate_strategy,
    true_rate_strategy,
    generate_emission_detection_reports_strategy,
)


@given(test_data=gen_test_data)
def test_000_gen_equipment_survey_report_return_expected_report(test_data):
    sensor: DefaultComponentLevelSensor = get_sensor_for_default_equipment_level_sensor_testing()
    site_id: str = test_data[0]
    eqg_id: str = test_data[1]
    meas_rate: float = test_data[3]
    true_rate: float = test_data[2]
    emissions_detection_reports: list[EmissionDetectionReport] = test_data[4]
    report: EquipmentGroupSurveyReport = sensor._gen_eqg_survey_report(
        site_id,
        eqg_id,
        true_rate=true_rate,
        measured_rate=meas_rate,
        emissions_detection_reports=emissions_detection_reports,
    )
    assert emissions_detection_reports == report.emissions_detected
    assert meas_rate == report.measured_rate
    assert true_rate == report.true_rate
    assert site_id == report.site
    assert eqg_id == report.equipment_group
