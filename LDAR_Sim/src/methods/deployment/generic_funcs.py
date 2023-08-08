# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.generic_funcs
# Purpose:     Commonly used schedule class methods for crew and companies
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

def get_work_hours(config, state):
    """ Get hours in day the crew is able to work
    """
    if config['consider_daylight']:
        daylight_hours = state['daylight'].get_daylight(
            state['t'].current_timestep)
        if daylight_hours <= config['max_workday']:
            work_hours = daylight_hours
        elif daylight_hours > config['max_workday']:
            work_hours = config['max_workday']
    else:
        work_hours = config['max_workday']

    if work_hours < 24 and work_hours != 0:
        start_hour = (24 - work_hours) / 2
        end_hour = start_hour + work_hours

    return work_hours, start_hour, end_hour


def get_deployment_dates(config, state):
    """ Using input parameters get the range of years and months available
        for company/ crew deployment. If none are specified, set to the
        number of years within simulation and all months.
    """
    # if user does not specify deployment interval, set to all months/years
    if len(config['scheduling']['deployment_years']) > 0:
        deployment_years = config['scheduling']['deployment_years']
    else:
        deployment_years = list(
            range(state['t'].start_date.year, state['t'].end_date.year+1))

    if len(config['scheduling']['deployment_months']) > 0:
        deployment_months = config['scheduling']['deployment_months']
    else:
        deployment_months = list(range(1, 13))
    return deployment_years, deployment_months
