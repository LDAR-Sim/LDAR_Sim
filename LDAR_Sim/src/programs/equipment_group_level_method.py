import sys
from programs.site_level_method import SiteLevelMethod
from scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule
from sensors.default_equipment_group_level_sensor import (
    DefaultEquipmentGroupLevelSensor,
)
from sensors.sensor_constant_mapping import (
    ERR_MSG_UNKNOWN_SENS_TYPE,
    SENS_MDL,
    SENS_QE,
    SENS_TYPE,
)


class EquipmentGroupLevelMethod(SiteLevelMethod):
    MEASUREMENT_SCALE = "equipment"

    def __init__(
        self,
        name,
        properties,
        consider_weather,
        sites,
        follow_up_schedule: FollowUpMobileSchedule,
    ):
        super().__init__(name, properties, consider_weather, sites, follow_up_schedule)

    def _initialize_sensor(self, sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): _description_
        """
        if sensor_info[SENS_TYPE] == "default":
            self._sensor = DefaultEquipmentGroupLevelSensor(
                sensor_info[SENS_MDL], sensor_info[SENS_QE]
            )
        else:
            print(ERR_MSG_UNKNOWN_SENS_TYPE.format(method=self._name))
            sys.exit()
