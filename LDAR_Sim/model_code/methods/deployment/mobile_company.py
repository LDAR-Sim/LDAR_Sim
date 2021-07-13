import pandas as pd
from sklearn.cluster import KMeans
import numpy as np


class Schedule:
    def __init__(self, config, parameters, state):
        self.parameters = parameters
        self.config = config
        self.state = state

    def get_deployment_dates(self):
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

    def can_deploy(self, date):
        #  If date passed is in deployment month and year return true
        return date.month in self.deployment_months and date.year in self.deployment_years

    def assign_agents(self):
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

    def select_crew_sites(self, site_pool, crew_num):
        # This function divies the site pool among all crews. Sites
        # are passed ordered on neglected, and order is kept in the
        # output
        if self.config['scheduling']['geography']:
            pass
        else:
            # This offsets by the crew number and increments by the
            # number of crews, n_crews= 3 ,  site_pool = [site[0], site[3], site[6]...]
            if len(site_pool) > 0:
                site_pool = site_pool[crew_num::self.config['n_crews']]
        return site_pool
