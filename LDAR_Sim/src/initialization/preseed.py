# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.preseed
# Purpose:     Generate a timeseries of integers for preseeding random functions
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

import numpy as np
from datetime import date, timedelta
import pickle


def gen_seed_timeseries(sim_start_date: date, sim_end_date: date, gen_dir) -> list[int]:
    seed_ts_dict: dict[date, int] = {}

    preseed_loc = gen_dir / "preseed.p"
    current_date = sim_start_date
    while current_date <= sim_end_date:
        seed_ts_dict[current_date] = np.random.randint(0, 255)
        current_date += timedelta(days=1)
    pickle.dump(seed_ts_dict, open(preseed_loc, "wb"))

    return seed_ts_dict


def get_seed_timeseries(gen_dir) -> list[int]:
    preseed_loc = gen_dir / "preseed.p"
    return pickle.load(open(preseed_loc, "rb"))
