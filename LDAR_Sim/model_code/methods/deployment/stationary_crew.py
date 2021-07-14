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
    def plan_visit(self, site):
        name = self.config['label']
        return {
            'site': None,
            'go_to_site': None,
            'LDAR_mins': None,
            'remaining_mins': None,
        }

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
                    'LDAR_mins': (int) number of minutes required for survey
                    'remaining_mins' (minutes): minutes left in survey
        """
        mins_left_in_day = (self.allowed_end_time - self.state['t'].current_date) \
            .total_seconds()/60
        out_dict = {
            'LDAR_mins': None,
            'go_to_site': None,
            'remaining_mins': None,
        }
        return out_dict

    @ timer
    def update_schedule(self, work_mins, next_lat=None, next_lon=None):
        pass

    def start_day(self):
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(self.start_hour))  # Set start of work
        self.get_work_hours()
        return

    @ timer
    def end_day(self):
        pass
