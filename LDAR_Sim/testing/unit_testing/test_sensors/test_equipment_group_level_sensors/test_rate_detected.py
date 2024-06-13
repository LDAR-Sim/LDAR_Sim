from src.sensors.default_equipment_group_level_sensor import (
    DefaultEquipmentGroupLevelSensor,
)
from hypothesis import given, strategies as st


@st.composite
def gen_rate_above_mdl(draw, mdl):
    rate: float = draw(st.floats(min_value=mdl))
    return rate


@st.composite
def gen_rate_below_mdl(draw, mdl):
    rate: float = draw(st.floats(min_value=0, max_value=mdl, exclude_max=True))
    return rate


@st.composite
def gen_sens_mdl_and_detectable_rates(draw):
    mdl = draw(st.floats(min_value=0, exclude_min=True))
    rate = draw(gen_rate_above_mdl(mdl))
    return mdl, rate


@st.composite
def gen_sens_mdl_and_undetectable_rates(draw):
    mdl = draw(st.floats(min_value=0, exclude_min=True))
    rate = draw(gen_rate_below_mdl(mdl))
    return mdl, rate


@given(gen_test_vals=gen_sens_mdl_and_detectable_rates())
def test_000_default_eqg_level_sensor_returns_true_above_mdl(gen_test_vals):
    sens: DefaultEquipmentGroupLevelSensor = DefaultEquipmentGroupLevelSensor(
        [gen_test_vals[0]],
        [0.0, 0.0],
        "default",
    )
    rate = gen_test_vals[1]
    assert sens._rate_detected(rate) is True


@given(gen_test_vals=gen_sens_mdl_and_undetectable_rates())
def test_000_default_eqg_level_sensor_returns_false_below_mdl(gen_test_vals):
    sens: DefaultEquipmentGroupLevelSensor = DefaultEquipmentGroupLevelSensor(
        [gen_test_vals[0]],
        [0.0, 0.0],
        "default",
    )
    rate = gen_test_vals[1]
    assert sens._rate_detected(rate) is False
