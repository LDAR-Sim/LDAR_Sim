from programs.method import Method
from sensors.default_site_level_sensor import DefaultSiteLevelSensor
from virtual_world.sites import Site
from scheduling.schedules import GenericSchedule
from sensors.sensor_constant_mapping import SENS_TYPE, SENS_MDL, ERR_MSG_UNKNOWN_SENS_TYPE
import sys


class SiteLevelMethod(Method):
    SURVEY_LEVEL = "site_level"

    def __init__(self, name, properties):
        super().__init__(name, properties)

    def survey_site(self, site: Site):
        # TODO complete this method
        self._sensor.detect_emissions(site, self._name)
        # if detection and will_followup:
        #     self.flag_site(site)

        return

    def flag_site(self, site: Site, follow_up_schedule: GenericSchedule):
        # TODO complete this method
        return

    def _initialize_sensor(self, sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): The dictionary of information the user has
            provided to the method about the sensor
        """
        if sensor_info[SENS_TYPE] == "default":
            self._sensor = DefaultSiteLevelSensor(sensor_info[SENS_MDL])
        else:
            print(ERR_MSG_UNKNOWN_SENS_TYPE.format(method=self._name))
            sys.exit()
