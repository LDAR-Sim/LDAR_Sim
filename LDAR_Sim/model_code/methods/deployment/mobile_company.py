import pandas as pd
from sklearn.cluster import KMeans
import numpy as np


class Schedule:
    def __init__(self, config, state):
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
