#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Time counter
# Purpose:     Initialize time object and keeps track of simulation time
#
# Copyright (C) 2019  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This file is for peer review. Do not distribute or modify it in any way.
# This program is presented WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#------------------------------------------------------------------------------

from datetime import datetime
from datetime import timedelta

class time_counter:
    def __init__ (self, parameters):
        '''
        Initialize a calendar and clock to count through the simulation.

        '''
        print('Initializing timeseries...')
        self.parameters = parameters
        self.start_date = datetime(parameters['start_year'],1,1)
        self.current_date = self.start_date
        self.current_timestep = 0
        self.end_date = self.start_date + timedelta(days = parameters['timesteps'])
        return
        
        
    def next_day (self):
        '''
        Go to the next day in the simulation

        '''        
        self.current_date += timedelta(days = 1)
        self.current_timestep += 1
        return
        