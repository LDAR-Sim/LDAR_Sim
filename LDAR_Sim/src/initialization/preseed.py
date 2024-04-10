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
import os
from constants.file_name_constants import Generator_Files


def gen_seed_timeseries(sim_start_date: date, sim_end_date: date, gen_dir) -> list[int]:
    seed_ts_dict: dict[date, int] = {}
    preseed_loc = gen_dir / Generator_Files.PRESEED_FILE
    current_date = sim_start_date

    if os.path.isfile(preseed_loc):
        seed_ts_dict = get_seed_timeseries(gen_dir)
        # check that the sim length matches
        if (sim_end_date - sim_start_date).days + 1 == len(seed_ts_dict):
            return seed_ts_dict
    print("Generating Random seed values for simulation...")
    while current_date <= sim_end_date:
        seed_ts_dict[current_date] = np.random.randint(0, 255)
        current_date += timedelta(days=1)
    with open(preseed_loc, "wb") as f:
        pickle.dump(seed_ts_dict, f)

    return seed_ts_dict


def get_seed_timeseries(gen_dir) -> list[int]:
    preseed_loc = gen_dir / Generator_Files.PRESEED_FILE
    with open(preseed_loc, "rb") as f:
        seed_ts = pickle.load(f)
    return seed_ts


def gen_seed_emis(n_sim: int, gen_dir):
    preseed_val: list[int] = []
    preseed_loc = gen_dir / Generator_Files.EMISSION_PRESEED_FILE
    if not os.path.exists(gen_dir):
        os.mkdir(gen_dir)

    if os.path.isfile(preseed_loc):
        preseed_val = get_emis_seed(gen_dir)
        if len(preseed_val) < n_sim:
            print("Generating additional Random Seed values for emissions...")
            for i in range(len(preseed_val), n_sim):
                emis_preseed: int = np.random.randint(0, 255)
                preseed_val.append(emis_preseed)
            with open(preseed_loc, "wb") as f:
                pickle.dump(preseed_val, f)
    else:
        print("Generating Random Seed values for emissions...")
        for i in range(n_sim):
            emis_preseed: int = np.random.randint(0, 255)
            preseed_val.append(emis_preseed)
        with open(preseed_loc, "wb") as f:
            pickle.dump(preseed_val, f)
    return preseed_val


def get_emis_seed(gen_dir) -> list[int]:
    preseed_loc = gen_dir / Generator_Files.EMISSION_PRESEED_FILE
    with open(preseed_loc, "rb") as f:
        emis_seed = pickle.load(f)
    return emis_seed
