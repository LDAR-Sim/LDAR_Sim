import numpy as np
#from generic_functions import get_prop_rate
from methods.base_company import company
from methods.base_crew import crew 
import pandas as pd 
from sklearn.cluster import KMeans


class aircraftS_company(company):
    def __init__(self,state, parameters, config, timeseries):
        # Run The base class Init
        super(aircraftS_company, self).__init__(state, parameters, config, timeseries)
        ###################---------company-level scheduling------############
        # Use clustering analysis to assign facilities to each agent, if two or more agents are aviable
        m_name = self.config['name']
        if self.parameters['methods'][m_name]['n_crews']>1:
            Lats = [] 
            Lons = [] 
            ID = [] 
            for site in self.state['sites']:
                ID.append(site['facility_ID'])
                Lats.append(site['lat'])
                Lons.append(site['lon'])
            sdf = pd.DataFrame({"ID":ID,
                        'lon':Lons,
                        'lat':Lats}) 
            X = sdf[['lat', 'lon']].values
            num = config['n_crews']
            kmeans = KMeans(n_clusters=num, random_state=0).fit(X)
            l = kmeans.labels_
        else: 
            l = np.zeros(len(self.state['sites']))
        
        for i in range(len(self.state['sites'])): 
            self.state['sites'][i]['label'] = l[i]
            
        # Initiate Crews
        for i in range(config['n_crews']):
            self.crews.append(crew(state, parameters, config,
                                     timeseries, self.deployment_days, id=i + 1))


        
		

