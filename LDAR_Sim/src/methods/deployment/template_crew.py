# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.template_crew
# Purpose:     Template crew specific deployment classes and methods (ie. Scheduling)
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
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
        """ Start day method. Get daily itinerary for crew. Can include other functions
            i.e. initialize time to account for work hours, and set the crews location.
        Args:
            site_pool (list): List of sites ready for survey.

        Returns:
            list: daily itinerary:
                {'site': (dict),
                'go_to_site: (boolean),
                'LDAR_mins': (int) work-onsite mins,
                'remaining_mins':(int)  minutes remaining in survey at site
                }
        """
        return  # itinerary

    def end_day(self, site_pool):
        """ End day function
        """
        self.update_schedule(self.last_site_travel_home_min)
