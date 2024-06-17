from src.sensors.default_equipment_group_level_sensor import (
    DefaultEquipmentGroupLevelSensor,
)
from testing.unit_testing.test_sensors.test_site_level_sensors.site_level_sensors_testing_fixtures import (  # noqa
    sensor_info_for_default_equipment_group_level_sensor_construction_testing_fix,
)

from constants import param_default_const as pdc


def test_000_simple_default_equipment_group_level_constructor_properly_initializes_as_default_equipment_group_level_sensor(  # noqa
    sensor_info_for_default_equipment_group_level_sensor_construction_testing: dict[str, int],
) -> None:
    sl_sensor = DefaultEquipmentGroupLevelSensor(
        sensor_info_for_default_equipment_group_level_sensor_construction_testing[
            pdc.Method_Params.MDL
        ],
        sensor_info_for_default_equipment_group_level_sensor_construction_testing[
            pdc.Method_Params.QE
        ][pdc.Method_Params.QUANTIFICATION_PARAMETERS],
        sensor_info_for_default_equipment_group_level_sensor_construction_testing[
            pdc.Method_Params.QE
        ][pdc.Method_Params.Q_TYPE],
    )
    assert isinstance(sl_sensor, DefaultEquipmentGroupLevelSensor)
