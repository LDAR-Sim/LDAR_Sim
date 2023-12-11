from virtual_world.sites import Site
from scheduling.workplan import Workplan


class Method:
    SURVEY_TIME_ACCESSOR = "time"
    TRAVEL_TIME_ACCESSOR = "t_bw_sites"
    DETEC_ACCESSOR = "sensor"

    # TODO ensure survey times aren't needed for methods
    def __init__(self, name: str, properties: dict):
        self._name: str = name
        self._initialize_sensor(properties[Method.DETEC_ACCESSOR])

    def deploy_crews(self, workplan: Workplan):
        """Deploy crews will send crews out to survey sites based on the provided workplan"""
        return

    def survey_site(self, site: Site):
        """The method will attempt to survey the site provided as an argument, detecting emissions
        at it's detection level, either tagging sites for follow-up or flagging leaks,
        and generating an emissions report

        Args:
            site (Site): The site to survey
        """
        return

    def gen_emissions_report(site: Site):
        """Will generate an emissions report of detections at the site.
        If no emissions are detected,will generate a report indicating that was the case.

        Args:
            site (Site): The site for which to generate the emissions report.
        """
        return

    def _initialize_sensor(sensor_info: dict) -> None:
        """Will initialize a sensor of the correct type based
        on the sensor info provided to the method

        Args:
            sensor_into (dict): _description_
        """
        return
