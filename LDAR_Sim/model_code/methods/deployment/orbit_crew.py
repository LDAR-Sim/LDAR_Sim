import numpy as np
from shapely.geometry import Point
from shapely import speedups
from methods.deployment._base import SchedCrew as BaseSchedCrew
from generic_functions import quick_cal_daylight, geo_idx
from datetime import timedelta
import netCDF4 as nc
from orbit_predictor.sources import get_predictor_from_tle_lines
from generic_functions import init_orbit_poly

speedups.disable()


class Schedule(BaseSchedCrew):
    def __init__(self, id, lat, lon, state, config, parameters, deployment_days, home_bases=None):
        self.parameters = parameters
        self.config = config
        self.state = state
        self.deployment_days = deployment_days
        self.crew_lat = lat
        self.crew_lon = lon
        self.allowed_end_time = None

        # extract cloud cover data
        wd = self.parameters['working_directory']
        cloud = self.parameters['weather_file']
        Dataset = nc.Dataset(wd + cloud, 'r')
        self.cloudcover = Dataset.variables['tcc'][:]
        Dataset.close()
        # obtain TLE file path
        m_name = self.config['label']
        self.sat = self.config['satellite_name']
        self.tlefile = self.config['TLE_files']

        self.get_orbit_predictor()
        self.get_orbit_path()

    def start_day(self, site_pool):
        '''
        Find out the site in the site_pool that can be seen by satellite 
        '''
        # Set start of work, satellite can work 24 hours per day
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(1))

        # find out the site that can be seen by satellite
        viewable_sites = self.calc_viewable_sites(site_pool)
        if len(viewable_sites) == 0:
            self.worked_today = False
            daily_site_plans = []
        # check daylight and cloud_cover for each site inside the site pool
        else:
            daily_site_plans = []
            for site in viewable_sites:
                sat_dl, sat_cc = self.assess_weather(site)
                if sat_dl and sat_cc:
                    plan = self.plan_visit(site)
                    daily_site_plans.append(plan)

        return daily_site_plans

    def plan_visit(self, site):
        return {
            'site': site,
            'go_to_site': True,
            'LDAR_mins': 0,  # we assume the survey time and travel time for Satellite is 0 mins
            'remaining_mins': 0,
        }

    def calc_viewable_sites(self, site_pool):
        """
        Subset possible sites that could be surveyed with a given satellite location.
        Generic utility function to check whether a satellite can see a given patch of ground
        satstate: dictionary containing satellite lon, lat, and altitude
        lon: longitude of location to assess
        lat: latitude of location to assess
        975 m is the average elevation in Alberta 
        Returns True to denote the satellite can see the location and False otherwise
        """
        valid_site = []
        # ind = 0
        sat_date = self.sat_date
        path = self.orbit_path
        date = self.state['t'].current_date.date()
        # find daily pathes
        DP = path[sat_date == date]
        for s in site_pool:
            fac_lat = np.float16(s['lat'])
            fac_lon = np.float16(s['lon'])
            PT = Point(fac_lon, fac_lat)
            for dp in DP:
                if dp.contains(PT):
                    valid_site.append(s)
                    break
        return valid_site

    def assess_weather(self, site):
        """
        Function to perform satellite specific checks of the weather for the purposes of visiting
        site: the site
        """

        site_lat = np.float16(site['lat'])
        site_lon = np.float16(site['lon'])

        lat_idx = geo_idx(site_lat, self.state['weather'].latitude)
        lon_idx = geo_idx(site_lon, self.state['weather'].longitude)
        ti = self.state['t'].current_timestep

        # check daylight
        date = self.state['t'].current_date
        sr, ss = quick_cal_daylight(date, site_lat, site_lon)

        if sr <= self.state['t'].current_date.hour <= ss:
            sat_daylight = True
        else:
            sat_daylight = False
        # check cloud cover

        CC = self.cloudcover[ti, lat_idx, lon_idx] * 100
        CC = round(CC)
        arr = np.zeros(100)
        arr[:CC] = 1
        np.random.shuffle(arr)

        if np.random.choice(arr, 1)[0] == 0:
            sat_cc = True
        else:
            sat_cc = False

        # do some checks and return true or false whether this site checks our weather checks
        return (sat_daylight, sat_cc)

    def get_orbit_predictor(self):
        # build a satellite orbit object
        wd = self.parameters['working_directory']
        TLEs = []
        with open(wd+self.tlefile) as f:
            for line in f:
                TLEs.append(line.rstrip())
        i = 0
        for x in TLEs:
            if x == self.sat:
                break
            i += 1
        TLE_LINES = (TLEs[i+1], TLEs[i+2])
        self.predictor = get_predictor_from_tle_lines(TLE_LINES)
        return

    def get_orbit_path(self):

        #### initiate the orbit path ####
        T1 = self.state['t'].start_date
        T2 = self.state['t'].end_date
        # calculate the orbit path polygon for satellite
        self.sat_datetime, self.orbit_path = init_orbit_poly(
            self.predictor, T1, T2, 15)
        self.sat_date = [d.date() for d in self.sat_datetime]

        self.sat_date = np.array(self.sat_date)
        self.orbit_path = np.array(self.orbit_path)

        return

    def update_schedule(self, work_mins):
        self.state['t'].current_date += timedelta(minutes=int(work_mins))

    def end_day(self, site_pool, itinerary):
        """ Travel home; update time to travel to homebase
        """
        return
