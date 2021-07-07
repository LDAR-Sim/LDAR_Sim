from datetime import timedelta
import numpy as np
from geography.homebase import find_homebase
from geography.distance import get_distance


class Schedule:
    def __init__(self, config, cur_loc=None, home_bases=None):
        self.config = config
        self.cur_loc = cur_loc
        self.home_bases = home_bases

    def get_travel_plan(self, next_loc=None, homebase=False):
        if self.configscheduling['geography']:
            # start day by reading the location of the LDAR team
            # find nearest home base
            if homebase and next_loc:
                next_loc, distance = find_homebase(self.cur_loc, self.homebases)
            if homebase and not next_loc:
                next_loc, distance = find_homebase(self.cur_loc, self.homebases)
            else:
                distance = get_distance(
                    self.cur_loc, [next_loc['lat'], next_loc['lon']], "Haversine")
            speed = np.random.choice(self.config['scheduling']['speed_list'])
            travel_time = timedelta(minutes=(distance/speed)*60)
        # ----------------------------------------------------------
        else:
            travel_time = timedelta(minutes=int(np.random.choice(self.config['t_bw_sites'])))
        return travel_time, next_loc

    def travel(self, travel_time, next_loc=None):
        if self.scheduling['geography']:
            self.cur_loc = next_loc
        self.state['t'].current_date += timedelta(minutes=int(travel_time))
