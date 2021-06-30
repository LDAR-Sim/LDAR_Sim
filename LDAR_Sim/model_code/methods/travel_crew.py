# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        crew
# Purpose:     Initialize each crew under company
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
import pandas as pd

from methods.base_crew import crew as base_crew


class travel_crew(base_crew):
    """
    """

    def __init__(self, state, parameters, config, timeseries, deployment_days, id):
        super(travel_crew, self).__init__(state, parameters,
                                          config, timeseries, deployment_days, id)
        # --- Travel specific Initalization ---
        self.worked_today = False
        self.rollover = []
        self.scheduling = self.config['scheduling']

        # IF there is scheduling or routeplanning load home bases and init LDAR Crew locations
        if self.config['scheduling']['route_planning'] or self.config['scheduling']['geography']:
            hb_file = parameters['working_directory'] + self.scheduling['home_bases']
            self.state['homebases'] = pd.read_csv(hb_file, sep=',')
            self.HX = self.state['homebases']['lon']
            self.HY = self.state['homebases']['lat']
            # initiate the location of LDAR crew
            self.state['current_x'] = self.scheduling['LDAR_crew_init_location'][0]
            self.state['current_y'] = self.scheduling['LDAR_crew_init_location'][1]
        # -------------------------------------------
    # --- Travel specific methods ---
    # -------------------------------------
