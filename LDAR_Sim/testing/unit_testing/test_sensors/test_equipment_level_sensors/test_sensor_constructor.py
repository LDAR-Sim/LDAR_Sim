from sensors.default_component_level_sensor import DefaultComponentLevelSensor
from testing.unit_testing.test_sensors.test_equipment_level_sensors.equipment_level_sensors_testing_fixtures import (  # noqa
    sensor_info_for_default_equipment_level_sensor_construction_testing_fix,
)


def test_000_simple_default_equipment_level_constructor_properly_initializes_as_default_equipment_level_sensor(  # noqa
    sensor_info_for_default_equipment_level_sensor_construction_testing: dict[str, int],
) -> None:
    sl_sensor = DefaultComponentLevelSensor(
        sensor_info_for_default_equipment_level_sensor_construction_testing["mdl"],
        sensor_info_for_default_equipment_level_sensor_construction_testing["QE"],
    )
    assert isinstance(sl_sensor, DefaultComponentLevelSensor)
