# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.template_company
# Purpose:     Template company specific deployment classes and methods (ie. Scheduling)
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
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


from methods.deployment._base import SchedCompany as BaseSchedCompany
from methods.crew import BaseCrew


def make_crews(crews, config, state, parameters, timeseries, deployment_days):
    """ Generate crews using BaseCrew class.

    Args:
        crews (list): List of crews
        config (dict): Method parameters
        state (dict): Current state of LDAR-Sim
        parameters (dict): Program parameters
        timeseries (dict): Timeseries
        deployment_days (list): days method can be deployed based on weather

    --- Required in module.company.BaseCompany ---
    """
    for i in range(config['n_crews']):
        crews.append(BaseCrew(state, parameters, config,
                              timeseries, deployment_days, id=i + 1))


class Schedule(BaseSchedCompany):
    def __init__(self, config, parameters, state):
        self.parameters = parameters
        self.config = config
        self.state = state

    # --- inherited methods ---
    # base.company ->  get_deployment_dates()
    # base.company ->  can_deploy_today()

    def assign_agents(self):
        """ assign agents to sites.
            --- Required in module.company.BaseCompany ---
        """

    def get_due_sites(self, site_pool):
        """ Retrieve a site list of sites due for screen / survey
        Args:
            site_pool (dict): List of sites
        Returns:
            site_pool (dict): List of sites ready for survey.
        """
        return site_pool

    def get_working_crews(self, site_pool, n_crews):
        """ Get number of working crews that day. Based on estimate
            that a crew ccan do 3 sites per day.
        Args:
            site_pool (dict): List of sites
            n_crews (int): Number of crews
            sites_per_crew (int, optional): Number of sites a crew can survey in a day.
            Defaults to 3.

        Returns:
            int: Number of crews to deploy that day.
        """
        return n_crews

    def get_crew_site_list(self, site_pool, crew_ID, n_crews):
        """ Allocates site pool among all crews. Ordering
            of sites is not changed by function.
        Args:
            site_pool (dict): List of sites
            crew_num (int): Integer index of crew
            n_crews (int): Number of crews

        Returns:
            dict: Crew site list (subset of site_pool)
        """
        return  # crew_site_list
