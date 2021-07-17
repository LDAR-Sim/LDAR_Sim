import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import math
from methods.deployment.base import sched_company as base_sched_company
from methods.crew import BaseCrew


def make_crews(crews, config, state, parameters, timeseries, deployment_days):
    for site in state['sites']:
        if config['measurement_scale'] == "equipment":  # This may change in the future
            n_fixed = int(site['fixed_sensors'])
        else:
            n_fixed = int(site['fixed_sensors'])
        for i in range(n_fixed):
            crews.append(
                BaseCrew(
                    state,
                    parameters,
                    config,
                    timeseries,
                    site,
                    deployment_days,
                    id=site['facility_ID'] + '-' + str(i + 1)))
            timeseries['fixed_cost'][state['t'].current_timestep] += \
                parameters['methods']['fixed']['up_front_cost']


class Schedule(base_sched_company):
    def __init__(self, config, parameters, state):
        self.parameters = parameters
        self.config = config
        self.state = state

    # --- inherited ---
    # base.company ->  get_deployment_dates()
    # base.company ->  can_deploy_today()

    def assign_agents(self):
        pass

    def get_due_sites(self, site_pool):
        """[summary]

        Args:
            site_pool ([type]): [description]

        Returns:
            [type]: [description]
        """
        site = [site for site in site_pool if site['facility_ID'] == self.site['facility_ID']]
        return site

    def get_working_crews(self, site_pool, n_crews, sites_per_crew=3):
        """ Get number of working crews that day. Based on estimate
            that a crew can do 3 sites per day.
        Args:
            site_pool (dict): List of sites
            n_crews (int): Number of crews
            sites_per_crew (int, optional): Number of sites a crew can survey in a day.
            Defaults to 3.

        Returns:
            int: Number of crews to deploy that day.
        """
        n_sites = len(site_pool)
        n_crews = math.ceil(n_sites/(n_crews*sites_per_crew))
        # cap workuing crews at max number of crews
        if n_crews > self.config['n_crews']:
            n_crews = self.config['n_crews']
        return n_crews

    def get_crew_site_list(self, site_pool, crew_idx, n_crews):
        """[summary]

        Args:
            site_pool ([type]): [description]
            crew_id ([type]): [description]
            n_crews ([type]): [description]

        Returns:
            [type]: [description]
        """
        if crew_idx == 0:
            return site_pool  # Right now only going to consider the first crew
            # will fix this as an issue later. #giter'done
        else:
            return []
