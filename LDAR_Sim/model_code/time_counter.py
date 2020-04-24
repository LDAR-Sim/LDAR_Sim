#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Time counter
# Purpose:     Initialize time object and keeps track of simulation time
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
        