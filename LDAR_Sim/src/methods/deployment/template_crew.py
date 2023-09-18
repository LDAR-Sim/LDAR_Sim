# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.template_crew
# Purpose:     Template crew specific deployment classes and methods (ie. Scheduling)
#
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


class Schedule():

    def __init__(
            self,
            id,
            lat,
            lon,
            state,
            config,
            virtual_world,
            simulation_settings,
            deployment_days,
            home_bases=None
    ):
        self.config = config
        self.state = state
        self.consider_weather = virtual_world["consider_weather"]
        self.in_dir = simulation_settings["input_directory"]
        self.deployment_days = deployment_days
        self.crew_lat = lat
        self.crew_lon = lon
        self.work_hours = None
        self.start_hour = None
        self.end_hour = None
        self.allowed_end_time = None
        self.scheduling = self.config['scheduling']
        # define a list of home bases for crew and redefine the initial location of crew

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
