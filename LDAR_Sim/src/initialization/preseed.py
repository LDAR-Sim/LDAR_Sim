# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.leaks
# Purpose:     Generate Leaks, Generate initial leaks and leak timeseries
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

import random
from datetime import datetime, timedelta
from utils.distributions import leak_rvs


def generate_preseeds(params):
    start_date = datetime(*params['start_date'])
    n_timesteps = (datetime(*params['end_date'])-start_date).days
    return [random.randrange(1, 50, 1) for i in range(n_timesteps)]
