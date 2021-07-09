from datetime import timedelta
import numpy as np
from geography.homebase import find_homebase
from geography.distance import get_distance


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

    def get_work_hours(self):
        if self.config['consider_daylight']:
            daylight_hours = self.state['daylight'].get_daylight(self.state['t'].current_timestep)
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

    def start_day(self):
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(self.start_hour))  # Set start of work

    def choose_site(self, rollover=None):
        """
        Choose a site to survey.
        """
        m_name = self.config['label']
        out_dict = None

        if self.config['is_follow_up']:
            site_pool = self.state['flags']
        else:
            site_pool = self.state['sites']
        # Sort all sites based on a neglect ranking
        site_pool = sorted(
            site_pool,
            key=lambda k: k['{}_t_since_last_LDAR'.format(m_name)],
            reverse=True)

        # Then, starting with the most neglected site, check if conditions are suitable for LDAR
        for site in site_pool:
            # Check 1: Has a survey at the site been attempted today?
            if site['{}_attempted_today?'.format(m_name)]:
                continue

            # Check 2a: Is flagged site ready for follow_up?
            if self.config['is_follow_up']:
                if (self.state['t'].current_date - site['date_flagged']).days < \
                        self.parameters['methods'][site['flagged_by']]['reporting_delay']:
                    continue
            else:
                # Check 2b: Is the site ready for Scheduled LDAR?
                # Because they are sorted, if this fails all other sites will as well
                if site['{}_t_since_last_LDAR'.format(m_name)] \
                        < int(site['{}_min_int'.format(m_name)]):
                    self.state['t'].current_date = self.state['t'].current_date.replace(hour=23)
                    break
                # Check 2c: has the site already met its annual survey quota (RS)
                elif site['{}_surveys_done_this_year'.format(m_name)] \
                        >= int(site['{}_RS'.format(m_name)]):
                    continue

            # Mark as attempted, regardless of weather.
            site['{}_attempted_today?'.format(m_name)] = True

            # Check 3: Check for weather
            if not self.deployment_days[site['lon_index'], site['lat_index'],
                                        self.state['t'].current_timestep]:
                continue

            # --- Estimate survey and travel times ---
            if site['facility_ID'] in self.rollover:
                # This also removes from rollover dict
                LDAR_mins = self.rollover.pop(site['facility_ID'])
            else:
                LDAR_mins = int(site['{}_time'.format(m_name)])
            travel_to_plan = self.get_travel_plan(next_loc=site)
            travel_home_plan = self.get_travel_plan()
            survey_times = self.check_survey_time(
                LDAR_mins, travel_to_plan['travel_time'],
                travel_home_plan['travel_time'])

            # The site passes all the tests! Choose it!s
            out_dict = {
                'site': site,
                'go_to_site': survey_times['go_to_site'],
                'travel_to_mins': travel_to_plan['travel_time'],
                'travel_home_mins': travel_home_plan['travel_time'],
                'LDAR_mins_site': survey_times['LDAR_mins_site'],
                # mins is LDAR + Travel to time. Home time is calced at end of day
                'LDAR_mins': travel_to_plan['travel_time'] + survey_times['LDAR_mins_site'],
                'LDAR_wtravel_site': survey_times['LDAR_wtravel_site'],
                'remaining_mins': survey_times['remaining_mins'],
            }
            break

        return out_dict

    def get_travel_plan(self, next_loc=None, homebase=False):
        if self.config['scheduling']['geography']:
            # start day by reading the location of the LDAR team
            # find nearest home base
            if homebase and next_loc:
                next_loc, distance = find_homebase(self.crew_lat, self.crew_lon, self.homebases)
            if homebase and not next_loc:
                next_loc, distance = find_homebase(self.crew_lat, self.crew_lon, self.homebases)
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

    def check_survey_time(self, survey_mins, travel_to_mins, travel_home_mins):
        mins_left_in_day = (self.allowed_end_time - self.state['t'].current_date) \
            .total_seconds()/60
        if travel_to_mins > mins_left_in_day:
            go_to_site = False
            LDAR_wtravel_site = 0
            LDAR_mins_site = 0
        elif (travel_to_mins + travel_home_mins + survey_mins) \
                > mins_left_in_day:
            go_to_site = True
            LDAR_wtravel_site = mins_left_in_day
            LDAR_mins_site = mins_left_in_day - (travel_to_mins + travel_home_mins)
        else:
            go_to_site = True
            LDAR_wtravel_site = survey_mins + travel_to_mins + travel_home_mins
            LDAR_mins_site = survey_mins
        remaining_mins = survey_mins - LDAR_mins_site
        if go_to_site:
            self.last_site_travel_home_min = travel_home_mins
        out_dict = {
            'go_to_site': go_to_site,
            'LDAR_wtravel_site': LDAR_wtravel_site,
            'LDAR_mins_site': LDAR_mins_site,
            'travel_to_mins': travel_to_mins,
            'travel_home_mins': travel_home_mins,
            'remaining_mins': remaining_mins,
        }
        return out_dict

    def update_schedule(self, minutes, next_lat=None, next_lon=None):
        if self.config['scheduling']['geography']:
            self.crew_lat, self.crew_lon = next_lat, next_lon
        self.state['t'].current_date += timedelta(minutes=int(minutes))

    def end_day(self):
        self.update_schedule(self.last_site_travel_home_min)
        self.last_site_travel_home_min = None
