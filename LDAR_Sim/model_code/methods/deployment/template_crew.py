# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.template_crew
# Purpose:     Template crew specific deployment classes and methods (ie. Scheduling)
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------


import numpy as np
import pandas as pd
from geography.homebase import find_homebase, find_homebase_opt
from geography.distance import get_distance
from methods.deployment._base import SchedCrew as BaseSchedCrew


class Schedule(BaseSchedCrew):

    # --- inherited methods ---
    # _base.crew ->  get_work_hours()
    # _base.crew ->  update_schedule()

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
        self.scheduling = self.config['scheduling']
        # define a list of home bases for crew and redefine the the initial location of crew

    def start_day(self, site_pool):
        """ Start day method. Initialize time to account for work hours, and set
            the crews location.
        Args:
            site_pool (list): List of sites ready for survey.

        Returns:
            list: Daily itinerary:
                {'site': (dict),
                'go_to_site: (boolean),
                'LDAR_mins': (int) work-onsite mins,
                'remaining_mins':(int)  minutes remaining in survey at site
                }
        """
        return site_plans_today

    def end_day(self, site_pool):
        """ End day function
        """
        self.update_schedule(self.last_site_travel_home_min)

    def plan_visit(self, site, next_site=None):
        """ 
        Args:
            site (dict): single site
            next_site (dict): single site used for estimating next

        Returns:
            {
                'site': same as input
                'go_to_site': whether there is enough time to go to site
                'LDAR_mins': survey time 
                'remaining_mins': minutes left in survey
        }
        """
        name = self.config['label']
        site['{}_attempted_today?'.format(name)] = True

        # Check weather conditions
        if not self.deployment_days[site['lon_index'], site['lat_index'],
                                    self.state['t'].current_timestep]:
            return None
        return {
            'site': site,
            'go_to_site': None,
            'LDAR_mins': None,
            'remaining_mins': None,
        }
