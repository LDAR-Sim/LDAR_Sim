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
        Stationary crew has been choicen but need to determine if a survey can be completed
        that day.
        """
        site = self.site
        m_name = self.config['label']
        out_dict = {'site': site,
                    'go_to_site': False,
                    'remaining_mins': None,
                    'LDAR_mins': None,
                    }

        # --Check 1--: Has a survey at the site been attempted today?
        if site['{}_attempted_today?'.format(m_name)]:
            return out_dict

        # --Check 2--: Is flagged site ready for follow_up?
        if self.config['is_follow_up']:
            if (self.state['t'].current_date - site['date_flagged']).days < \
                    self.parameters['methods'][site['flagged_by']]['reporting_delay']:
                return out_dict

        # If passed Checks 1, 2 mark as attempted, regardless of weather.
        site['{}_attempted_today?'.format(m_name)] = True

        # --Check 3--: Check for weather
        if not self.deployment_days[site['lon_index'], site['lat_index'],
                                    self.state['t'].current_timestep]:
            return out_dict

        # If passes Check 3, go to site
        mins_left_in_day = (self.allowed_end_time - self.state['t'].current_date) \
            .total_seconds()/60
        out_dict.update({'remaining_mins': 0, 'LDAR_mins': mins_left_in_day})
        return out_dict

    def update_schedule(self, work_mins):
        self.state['t'].current_date += timedelta(minutes=int(work_mins))

    def end_day(self):
        pass
