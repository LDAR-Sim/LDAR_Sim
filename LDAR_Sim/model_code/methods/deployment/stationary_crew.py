from datetime import timedelta
import numpy as np


class Schedule:
    def __init__(self, id, lat, lon, state, config, parameters, deployment_days, home_bases=None):
        self.parameters = parameters
        self.config = config
        self.state = state
        self.deployment_days = deployment_days
        self.work_hours = None
        self.start_hour = None
        self.end_hour = None
        self.allowed_end_time = None
        self.rollover = {}

    def plan_visit(self, site):
        name = self.config['label']
        return {
            'site': None,
            'go_to_site': None,
            'LDAR_mins': None,
            'remaining_mins': None,
        }

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

    def update_schedule(self, work_mins, next_lat=None, next_lon=None):
        pass

    def start_day(self):
        self.state['t'].current_date = self.state['t'].current_date.replace(
            hour=int(self.start_hour))  # Set start of work
        return

    def end_day(self):
        pass
