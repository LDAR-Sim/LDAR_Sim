from datetime import timedelta
import numpy as np


from geography.homebase import find_homebase
from geography.distance import get_distance
from utils.performance import timer


class Schedule:
    def __init__(self, id, lat, lon, state, config, parameters, deployment_days, home_bases=None):
        self.parameters = parameters
        self.config = config
        self.state = state
        self.deployment_days = deployment_days
        self.crew_lat = lat
        self.crew_lon = lon
        self.home_bases = home_bases
        self.work_hours = None
        self.start_hour = None
        self.end_hour = None
        self.allowed_end_time = None
        self.last_site_travel_home_min = None
        self.rollover = {}

    @timer
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

    @ timer
    def get_work_hours(self):
        if self.config['consider_daylight']:
            daylight_hours = self.state['daylight'].get_daylight(
                self.state['t'].current_timestep)
            if daylight_hours <= self.config['max_workday']:
                self.work_hours = daylight_hours
            elif daylight_hours > self.config['max_workday']:
                self.work_hours = self.config['max_workday']
        elif not self.config['consider_daylight']:
            self.work_hours = self.config['max_workday']

        if self.work_hours < 24 and self.work_hours != 0:
            self.start_hour = (24 - self.work_hours) / 2
            self.end_hour = self.start_hour + self.work_hours
        else:
            print(
                'Unreasonable number of work hours specified for crew ' +
                str(self.crewstate['id']))

        self.allowed_end_time = self.state['t'].current_date.replace(
            hour=int(self.end_hour), minute=0, second=0)

    @ timer
    def plan_site_trip(self, site):
        name = self.config['label']
        site['{}_attempted_today?'.format(name)] = True
        if not self.deployment_days[site['lon_index'], site['lat_index'],
                                    self.state['t'].current_timestep]:
            return None
        if site['facility_ID'] in self.rollover:
            # Remove facility from rollover list, and retrieve remaining survey minutes
            LDAR_mins = self.rollover.pop(site['facility_ID'])
        else:
            # Get survey minutes
            LDAR_mins = int(site['{}_time'.format(name)])
        # Get travel time minutes, and check if there is enough time.
        travel_to_plan = self.get_travel_plan(next_loc=site)
        travel_home_plan = self.get_travel_plan()
        survey_times = self.check_survey_time(
            LDAR_mins, travel_to_plan['travel_time'],
            travel_home_plan['travel_time'])
        # The site passes all the tests! Choose it!s
        return {
            'site': site,
            'go_to_site': survey_times['go_to_site'],
            'travel_to_mins': travel_to_plan['travel_time'],
            'travel_home_mins': travel_home_plan['travel_time'],
            'LDAR_mins_onsite': survey_times['LDAR_mins_onsite'],
            # mins is LDAR + Travel to time. Home time is called at end of day
            'LDAR_mins': survey_times['LDAR_mins'],
            'LDAR_wtravel_site': survey_times['LDAR_wtravel_site'],
            'remaining_mins': survey_times['remaining_mins'],
        }

    @ timer
    def get_travel_plan(self, next_loc=None, homebase=False):
        if self.config['scheduling']['geography']:
            # start day by reading the location of the LDAR team
            # find nearest home base
            if homebase and next_loc:
                next_loc, distance = find_homebase(
                    self.crew_lat, self.crew_lon, self.homebases)
            if homebase and not next_loc:
                next_loc, distance = find_homebase(
                    self.crew_lat, self.crew_lon, self.homebases)
            else:
                distance = get_distance(
                    self.crew_lat, self.crew_lon,
                    next_loc['lat'], next_loc['lon'], "Haversine")
            speed = np.random.choice(self.config['scheduling']['speed_list'])
            travel_time = (distance/speed)*60
        # ----------------------------------------------------------
        else:
            travel_time = np.random.choice(self.config['t_bw_sites'])
        out_dict = {
            'travel_time': travel_time,
            'next_site': next_loc,
        }
        return out_dict

    @ timer
    def check_survey_time(self, survey_mins, travel_to_mins, travel_home_mins):
        """Check the survey and travel times, determine if there is enough
           time to go to site.

        Args:
            survey_mins (float): minutes required to perform or finish survey
            travel_to_mins (float): minutes required to travel to site
            travel_home_mins (float): minutes required to travel home from site

        Returns:
            dict:   'go_to_site' (boolean): go_to_site,
                    'LDAR_wtravel_site' (minutes): survey time today + travel to and from,
                    'LDAR_mins_onsite' (minutes): survey time today,
                    'travel_to_mins' (minutes): travel time to site,
                    'travel_home_mins' (minutes): travel time from site,
                    'remaining_mins' (minutes): minutes left in survey that can be rolled over
                     to another day,
        """
        mins_left_in_day = (self.allowed_end_time - self.state['t'].current_date) \
            .total_seconds()/60
        if travel_to_mins >= mins_left_in_day:
            # Not enough time to travel to site
            go_to_site = False
            LDAR_wtravel_site = 0
            LDAR_mins_onsite = 0
        elif travel_to_mins + travel_home_mins >= mins_left_in_day:
            # Not enough time to travel to and from site
            # --HBD-- Should consider, splitting up travel, if site is too far to do in a day.
            go_to_site = False
            LDAR_wtravel_site = 0
            LDAR_mins_onsite = 0
        elif (travel_to_mins + travel_home_mins + survey_mins) \
                > mins_left_in_day:
            # Enough time to travel, but not enough time to work go, and rollover minutes.
            go_to_site = True
            LDAR_wtravel_site = mins_left_in_day
            LDAR_mins_onsite = mins_left_in_day - \
                (travel_to_mins + travel_home_mins)
        else:
            # Enough time to travel and work
            go_to_site = True
            LDAR_wtravel_site = survey_mins + travel_to_mins + travel_home_mins
            LDAR_mins_onsite = survey_mins
        remaining_mins = survey_mins - LDAR_mins_onsite
        LDAR_mins = travel_to_mins + LDAR_mins_onsite
        if go_to_site:
            self.last_site_travel_home_min = travel_home_mins
        out_dict = {
            'LDAR_mins': LDAR_mins,
            'go_to_site': go_to_site,
            'LDAR_wtravel_site': LDAR_wtravel_site,
            'LDAR_mins_onsite': LDAR_mins_onsite,
            'travel_to_mins': travel_to_mins,
            'travel_home_mins': travel_home_mins,
            'remaining_mins': remaining_mins,
        }
        return out_dict

    @ timer
    def update_schedule(self, work_mins, next_lat=None, next_lon=None):

        if self.config['scheduling']['geography']:
            self.crew_lat, self.crew_lon = next_lat, next_lon
        self.state['t'].current_date += timedelta(minutes=int(work_mins))

    def start_day(self, site_pool):
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(self.start_hour))  # Set start of work
        return self.get_due_sites(site_pool)

    @ timer
    def end_day(self):
        self.update_schedule(self.last_site_travel_home_min)
        self.last_site_travel_home_min = None
