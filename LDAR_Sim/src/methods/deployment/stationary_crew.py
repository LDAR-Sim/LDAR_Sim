# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.deployment.stationary_crew
# Purpose:     Stationary crew specific deployment classes and methods (ie. Scheduling)
#
# Copyright (C) 2018-2021  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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


class Schedule:
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
        rollover,
        home_bases=None,
    ):
        self.config = config
        self.state = state
        self.consider_weather = virtual_world["consider_weather"]
        self.in_dir = simulation_settings["input_directory"]
        self.deployment_days = deployment_days
        self.work_hours = 24
        self.start_hour = 0
        self.end_hour = 23
        self.scheduling = self.config["scheduling"]

    def start_day(self, site_pool):
        """Start day method. Get daily itinerary for crew.

        Args:
            site_pool (list): List of sites ready for survey.

        Returns:
            list: daily itinerary:
                {'site': (dict),
                'go_to_site: (boolean),
                'LDAR_mins': (int) Always zero for Stationary
                'remaining_mins':(int)  Always zero for Stationary
                }
        """
        name = self.config["label"]
        itinerary = []
        for site in site_pool:
            site["{}_attempted_today?".format(name)] = True
            # Check weather conditions
            if (
                not self.consider_weather
                or self.deployment_days[
                    site["lon_index"],
                    site["lat_index"],
                    self.state["t"].current_timestep,
                ]
            ):
                site_plan = {
                    "site": site,
                    "go_to_site": True,
                    # Stationary has no set LDAR minutes
                    "LDAR_mins": 0,
                    "remaining_mins": 0,
                }
                itinerary.append(site_plan)
        return itinerary

    def end_day(self, site_pool, itinerary):
        """End day function"""
        self.state["t"].current_date = self.state["t"].current_date.replace(hour=int(self.end_hour))
        return
