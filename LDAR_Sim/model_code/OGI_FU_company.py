# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        OGI follow-up company
# Purpose:     Company managing follow-up OGI surveys.
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

from OGI_FU_crew import OGI_FU_crew
import numpy as np


class OGI_FU_company:
    def __init__(self, state, parameters, config, timeseries):
        """
        Initialize a follow-up company to manage the OGI_FU crews (e.g. a contracting company).

        """
        self.name = config['label']
        self.state = state
        self.parameters = parameters
        self.config = config
        self.timeseries = timeseries
        self.crews = []
        self.deployment_days = self.state['weather'].deployment_days(
            method_name=self.name,
            start_date=self.state['t'].start_date,
            start_work_hour=8,  # Start hour in day
            consider_weather=parameters['consider_weather'])
        self.timeseries['OGI_FU_prop_sites_avail'] = []
        self.timeseries['OGI_FU_cost'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['OGI_FU_redund_tags'] = np.zeros(self.parameters['timesteps'])
        self.timeseries['OGI_FU_sites_visited'] = np.zeros(self.parameters['timesteps'])

        # Additional variable(s) for each site
        for site in self.state['sites']:
            site.update({'OGI_FU_t_since_last_LDAR': 0})
            site.update({'attempted_today_OGI_FU?': False})
            site.update({'OGI_FU_surveys_conducted': 0})
            site.update({'OGI_FU_missed_leaks': 0})

        # Initialize 2D matrices to store deployment day (DD) counts and MCBs
        self.DD_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))
        self.MCB_map = np.zeros(
            (len(self.state['weather'].longitude),
             len(self.state['weather'].latitude)))

        # Initialize the individual OGI_FU crews (the agents)
        for i in range(config['n_crews']):
            self.crews.append(OGI_FU_crew(state, parameters, config,
                                          timeseries, self.deployment_days, id=i + 1))

        return

    def deploy_crews(self):
        """
        The OGI_FU company tells all the crews to get to work.
        """

        for i in self.crews:
            i.work_a_day()

        # Update method-specific site variables each day
        for site in self.state['sites']:
            site['OGI_FU_t_since_last_LDAR'] += 1
            site['attempted_today_OGI_FU?'] = False

        self.state['flags'] = [flag for flag in self.state['sites'] if flag['currently_flagged']]

        # Calculate proportion sites available
        available_sites = 0
        for site in self.state['sites']:
            if self.deployment_days[site['lon_index'],
                                    site['lat_index'],
                                    self.state['t'].current_timestep]:
                available_sites += 1
        prop_avail = available_sites / len(self.state['sites'])
        self.timeseries['OGI_FU_prop_sites_avail'].append(prop_avail)

        return

    def site_reports(self):
        """
        Writes site-level deployment days (DDs) and maximum condition blackouts (MCBs)
        for each site.
        """

        for site in self.state['sites']:
            site['OGI_FU_prop_DDs'] = self.DD_map[site['lon_index'], site['lat_index']]
            site['OGI_FU_MCB'] = self.MCB_map[site['lon_index'], site['lat_index']]

        return
