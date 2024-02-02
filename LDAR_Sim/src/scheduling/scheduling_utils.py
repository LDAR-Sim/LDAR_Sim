"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        scheduling_utils
Purpose: Contains utility functions and variables used with the scheduling module

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
from scheduling.follow_up_mobile_schedule import FollowUpMobileSchedule
from scheduling.generic_schedule import GenericSchedule
from scheduling.mobile_schedule import MobileSchedule
from scheduling.stationary_schedule import StationarySchedule
from virtual_world.sites import Site

DEPLOY_TYPE_ACCESSOR = "deployment_type"
FOLLOWUP_ACCSSOR = "is_follow_up"
INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE = (
    "Error: LDAR-Sim has detected an invalid method deployment type of:"
    "{deploy_type} for method: {method}"
)


def create_schedule(
    method_name: str,
    method_details: dict,
    sites: list[Site],
    sim_start_date: date,
    sim_end_date: date,
    est_meth_daily_surveys: int,
    method_avail_crews: int,
) -> GenericSchedule:
    """Will create and return  schedule with the schedule type based on
    the provided method and it's parameters. All schedules inherit from generic schedule
    class and will overwrite it's method with method type specific behavior where required.

    Args:
        method_name (str): The method name that the schedule is being created for.
        method_details (dict): The method parameters, will be used to determine the
        correct schedule type to create.

    Returns:
        GenericSchedule: A schedule object with the correct schedule type for
        the given method deployment type. Should be treated as a generic schedule and will
        enforce the correct behavior through polymorphism.
    """
    method_follow_up: bool = method_details[FOLLOWUP_ACCSSOR]
    method_deployment_type: str = method_details[DEPLOY_TYPE_ACCESSOR]
    if not method_follow_up:
        if method_deployment_type == MobileSchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = MobileSchedule(
                method_name,
                sites,
                sim_start_date,
                sim_end_date,
                est_meth_daily_surveys,
                method_avail_crews,
            )
        elif method_deployment_type == StationarySchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = StationarySchedule(
                method_name,
                sites,
                sim_start_date,
                sim_end_date,
                est_meth_daily_surveys,
                method_avail_crews,
            )
        else:
            print(
                INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE.format(
                    deploy_type=method_deployment_type, method=method_name
                )
            )
            exit()
    else:
        if method_deployment_type == FollowUpMobileSchedule.DEPLOY_TYPE_CODE:
            schedule: GenericSchedule = FollowUpMobileSchedule(
                method_name,
                sites,
                sim_start_date,
                sim_end_date,
                est_meth_daily_surveys,
                method_avail_crews,
            )
        else:
            print(
                INVALID_DEPLOYMENT_TYPE_ERROR_MESSAGE.format(
                    deploy_type=method_deployment_type, method=method_name
                )
            )
            exit()
    return schedule
