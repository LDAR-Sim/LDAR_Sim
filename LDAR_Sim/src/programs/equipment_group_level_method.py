"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        equipment_group_level_method
Purpose: The module provides default behaviors for equipment group level methods

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""
import sys
from programs.site_level_method import SiteLevelMethod
from scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule
from sensors.METEC_NoWind_sensor import METECNWEquipmentGroup
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
        elif sensor_info[SENS_TYPE] == "METEC_no_wind":
            self._sensor = METECNWEquipmentGroup(
                sensor_info[SENS_MDL], sensor_info[SENS_QE]
            )
        else:
            print(ERR_MSG_UNKNOWN_SENS_TYPE.format(method=self._name))
            sys.exit()
