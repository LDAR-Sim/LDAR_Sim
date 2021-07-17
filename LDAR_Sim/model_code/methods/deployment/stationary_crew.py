from datetime import timedelta
import numpy as np

from methods.deployment.base import sched_crew as base_sched_crew


class Schedule(base_sched_crew):
    def __init__(self, id, lat, lon, state, config, parameters, deployment_days, home_bases=None):
        self.parameters = parameters
        self.config = config
        self.state = state
        self.deployment_days = deployment_days
        self.crew_lat = lat
        self.crew_lon = lon
        self.work_hours = None
        self.start_hour = None
        self.end_hour = None
        self.allowed_end_time = None
        self.rollover = {}
        self.scheduling = self.config['scheduling']

    # --- inherited ---
    # base.crew ->  get_work_hours()

    def plan_visit(self, site, next_site=None):
        """ Check survey and travel times and see if there is enough time
            to go to site. If a site survey was started on a previous day
            the amount of minutes rolled over will be used for survey time.

        Args:
            site (dict): single site

        Returns:
            {
                'site': same as input
                'go_to_site': whether there is enough time to go to site
                'travel_to_mins': travel time in minutes
                'travel_home_mins': travel time in minutes
                'LDAR_mins_onsite': minutes onsite
                'LDAR_mins': travel to and survey time (excludes travel home time)
                'remaining_mins': minutes left in survey
        }
        """
        name = self.config['label']
        site['{}_attempted_today?'.format(name)] = True
        # Cannot survey because of weather
        if not self.deployment_days[site['lon_index'], site['lat_index'],
                                    self.state['t'].current_timestep]:
            return None
        return {
            'site': site,
            'go_to_site': True,
            # Stationary has no set LDAR minutes
            'LDAR_mins': 0,
            'remaining_mins': 0,
        }

    def update_schedule(self, work_mins):
        return

    def start_day(self):
        return

    def end_day(self):
        return
