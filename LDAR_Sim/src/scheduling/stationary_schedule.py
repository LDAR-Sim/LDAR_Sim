"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        stationary_schedule
Purpose: The extended schedule module for stationary types. 

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

    def _reconstruct():
        super()._reconstruct()
        return
