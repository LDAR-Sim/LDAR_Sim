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

from methods.deployment._base import SchedCrew as BaseSchedCrew


class Schedule(BaseSchedCrew):
    def __init__(self, id, lat, lon, state, config, parameters, deployment_days, home_bases=None):
        self.parameters = parameters
        self.config = config
        self.state = state
        self.deployment_days = deployment_days
        self.scheduling = self.config['scheduling']

    # --- inherited methods ---
    # _base.crew ->  get_work_hours()
    # _base.crew ->  update_schedule()

    def start_day(self, site_pool):
        """ Start day method. Get daily itinerary for crew.

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
        name = self.config['label']
        itinerary = []
        for site in site_pool:
            site['{}_attempted_today?'.format(name)] = True
            # Check weather conditions
            if self.deployment_days[site['lon_index'], site['lat_index'],
                                    self.state['t'].current_timestep]:
                site_plan = {
                    'site': site,
                    'go_to_site': True,
                    # Stationary has no set LDAR minutes
                    'LDAR_mins': 0,
                    'remaining_mins': 0,
                }
                itinerary.append(site_plan)
        return itinerary

    def end_day(self, site_pool, itinerary):
        """ End day function
        """
        return
