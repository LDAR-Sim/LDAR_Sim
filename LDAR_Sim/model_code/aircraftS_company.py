import math
import numpy as np
from generic_functions import get_prop_rate
from methods.base_company import company
from aircraftS_crew import AC_Screw
import pandas as pd 
from sklearn.cluster import KMeans


class aircraftS_company(company):
    def __init__(self,state, parameters, config, timeseries):
        # Run The base class Init
        super(aircraftS_company, self).__init__(state, parameters, config, timeseries)
        
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
            self.crews.append(AC_Screw(state, parameters, config,
                                     timeseries, self.deployment_days, id=i + 1))


        
		
    def find_leaks(self):
        """
        The aircraft company tells all the crews to get to work.
        
        """
        m_name = self.config['name']
        self.scheduling  = self.parameters['methods'][m_name]['scheduling']
        if self.scheduling['deployment_times'][0]: 
            required_year = self.scheduling['deployment_times'][1]
            required_month = self.scheduling['deployment_times'][2]
        else:
            required_year = list(range(self.state['t'].start_date.year,self.state['t'].end_date.year+1))
            required_month = list(range(1,13))
        
        if self.state['t'].current_date.month in required_month  and self.state['t'].current_date.year in required_year:
        
            self.candidate_flags = []
            for i in self.crews:
                i.work_a_day(self.candidate_flags)
            
            
            # Flag sites according to the flag ratio
            if len(self.candidate_flags) > 0:
                self.flag_sites()
    
            # Update method-specific site variables each day
            for site in self.state['sites']:
                site['{}_t_since_last_LDAR'.format(m_name)] += 1
                site['{}_attempted_today?'.format(m_name)] = False
    
            if self.state['t'].current_date.day == 1 and self.state['t'].current_date.month == 1:
                for site in self.state['sites']:
                    site['{}_surveys_done_this_year'.format(m_name)] = 0
    
            # Calculate proportion sites available
            available_sites = 0
            for site in self.state['sites']:
                if self.deployment_days[site['lon_index'],
                                        site['lat_index'],
                                        self.state['t'].current_timestep]:
                    available_sites += 1
            prop_avail = available_sites / len(self.state['sites'])
            self.timeseries['{}_prop_sites_avail'.format(m_name)].append(prop_avail)
        else: 
            self.timeseries['{}_prop_sites_avail'.format(m_name)].append(0)

        return

