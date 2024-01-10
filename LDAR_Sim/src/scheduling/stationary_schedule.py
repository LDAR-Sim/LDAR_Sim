from datetime import date
from scheduling.generic_schedule import GenericSchedule
from virtual_world.sites import Site


class StationarySchedule(GenericSchedule):
    """A schedule class to provide scheduling functionality for methods classified
    as the "stationary" type. Will overwrite GenericSchedule functionality as required.
    """

    DEPLOY_TYPE_CODE = "stationary"

    def __init__(
        self,
        method_name: str,
        sites: "list[Site]",
        sim_start_date: date,
        sim_end_date: date,
        est_meth_daily_surveys: int,
        method_avail_crews: int,
    ) -> None:
        super().__init__(
            method_name,
            sites,
            sim_start_date,
            sim_end_date,
            est_meth_daily_surveys,
            method_avail_crews,
        )
        return
