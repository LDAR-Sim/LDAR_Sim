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
        """[summary]
                ---HBD MO!!!  Describe what happens hear ---
        """
        # Use clustering analysis to assign facilities to each agent,
        # if 2+ agents are available
        if self.config['n_crews'] > 1:
            lats = []
            lons = []
            ID = []
            for site in self.state['sites']:
                ID.append(site['facility_ID'])
                lats.append(site['lat'])
                lons.append(site['lon'])
            # HBD - What is sdf?
            sdf = pd.DataFrame({"ID": ID,
                                'lon': lons,
                                'lat': lats})
            locs = sdf[['lat', 'lon']].values
            num = self.config['n_crews']
            kmeans = KMeans(n_clusters=num, random_state=0).fit(locs)
            label = kmeans.labels_
        else:
            label = np.zeros(len(self.state['sites']))

        for i in range(len(self.state['sites'])):
            self.state['sites'][i]['label'] = label[i]

    def get_due_sites(self, site_pool):
        """ Retrieve a site list of sites due for screen / survey

            If the method is a followup, return sites that have passed
            that have passed the reporting delay window.

            If the method is not followup return sites that have passed
            the minimum survey interval, and that still require surveys
            in the current year.

            # --Note-- this function persists the site list throughout,
            so the input site_pool will always be modified regardless of
            the variable assigned on return.

        Args:
            site_pool (dict): List of sites
        Returns:
            site_pool (dict): List of sites ready for survey.
        """
        name = self.config['label']
        days_since_LDAR = '{}_t_since_last_LDAR'.format(name)
        survey_done_this_year = '{}_surveys_done_this_year'.format(name)
        survey_min_interval = '{}_min_int'.format(name)
        survey_frequency = '{}_RS'.format(name)
        meth = self.parameters['methods']

        if self.config['is_follow_up']:
            site_pool = filter(
                lambda s, : (
                    self.state['t'].current_date - s['date_flagged']).days
                >= meth[s['flagged_by']]['reporting_delay'],
                site_pool)
        else:
            days_since_LDAR = '{}_t_since_last_LDAR'.format(name)
            site_pool = filter(
                lambda s: s[survey_done_this_year] < int(s[survey_frequency]) and
                s[days_since_LDAR] >= int(s[survey_min_interval]), site_pool)

        site_pool = sorted(
            list(site_pool), key=lambda x: x[days_since_LDAR], reverse=True)
        return site_pool

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

    def get_crew_site_list(self, site_pool, crew_num, n_crews):
        """ This function divies the site pool among all crews. Ordering
            of sites is not changed by function.
        Args:
            site_pool (dict): List of sites
            crew_num (int): Integer index of crew
            n_crews (int): Number of crews

        Returns:
            dict: Crew site list (subset of site_pool)
        """
        if self.config['scheduling']['geography']:
            pass
        else:
            # This offsets by the crew number and increments by the
            # number of crews, n_crews= 3 ,  site_pool = [site[0], site[3], site[6]...]
            if len(site_pool) > 0:
                crew_site_list = site_pool[crew_num::n_crews]
        return crew_site_list
