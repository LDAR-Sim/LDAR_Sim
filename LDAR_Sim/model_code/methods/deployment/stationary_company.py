import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import math


class Schedule:
    def __init__(self, config, parameters, state):
        self.parameters = parameters
        self.config = config
        self.state = state

    def get_deployment_dates(self):
        """ Using input parameters get the range of years and months available
            for company/ crew deployment. If non are specified, set to the
            number of years within simulation and all months.
        """
        # if user does not specify deployment interval, set to all months/years
        if len(self.config['scheduling']['deployment_years']) > 0:
            self.deployment_years = self.config['scheduling']['deployment_years']
        else:
            self.deployment_years = list(
                range(self.state['t'].start_date.year, self.state['t'].end_date.year+1))

        if len(self.config['scheduling']['deployment_months']) > 0:
            self.deployment_months = self.config['scheduling']['deployment_months']
        else:
            self.deployment_months = list(range(1, 13))

    def can_deploy_today(self, date):
        """ If the current day is within the deployment month and years window
        Args:
            date (datetime): Current Date

        Returns:
            Boolean: If date passed is in deployment month and year
        """
        return date.month in self.deployment_months and date.year in self.deployment_years

    def assign_agents(self):
        return

    def get_due_sites(self, site_pool):
        return site_pool

    def get_working_crews(self, site_pool, n_crews, sites_per_crew=3):
        return n_crews

    def get_crew_site_list(self, site_pool, crew_num, n_crews):
        # This offsets by the crew number and increments by the
        # number of crews, n_crews= 3 ,  site_pool = [site[0], site[3], site[6]...]
        if len(site_pool) > 0:
            crew_site_list = site_pool[crew_num::n_crews]
        return crew_site_list
