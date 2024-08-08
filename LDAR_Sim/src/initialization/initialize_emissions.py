"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        initialize_emissions
Purpose: Module for initializing emissions

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

import logging
from pathlib import Path
import pickle
import sys
from datetime import date
import numpy as np
from virtual_world.infrastructure import Infrastructure
from initialization.preseed import gen_seed_timeseries
from constants.file_name_constants import Generator_Files
from constants.output_messages import RuntimeMessages as rm
from constants.error_messages import Input_Processing_Messages as ipm


def initialize_emissions(
    n_sims: int,
    preseed: bool,
    emis_preseed_val: list[int],
    hash_file_exist: bool,
    infrastructure: Infrastructure,
    start_date: date,
    end_date: date,
    generator_dir: Path,
    force_remake: bool = False,
):
    n_sim_loc = generator_dir / Generator_Files.N_SIM_SAVE_FILE
    n_simulation_saved: int = 0
    # Store params used to generate the pickle files for change detection
    if not hash_file_exist or force_remake:
        # Generate emissions for all simulation sets
        for i in range(n_sims):
            if preseed:
                np.random.seed(emis_preseed_val[i])
            emissions: dict = {}
            emis_file_loc = generator_dir / Generator_Files.GEN_INFRA_EMISS.format(i=i)
            print(rm.GEN_EMISS.format(i=i))
            emissions.update(
                infrastructure.generate_emissions(
                    sim_start_date=start_date,
                    sim_end_date=end_date,
                    sim_number=i,
                )
            )
            with open(emis_file_loc, "wb") as f:
                pickle.dump(emissions, f)

        with open(n_sim_loc, "wb") as f:
            pickle.dump(n_sims, f)
    else:
        try:
            with open(n_sim_loc, "rb") as f:
                n_simulation_saved = pickle.load(f)
        except FileNotFoundError:
            # Handle the case when the file is missing
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(ipm.GENERATOR_ERROR.format(file=Generator_Files.N_SIM_SAVE_FILE))
            sys.exit()

        if n_simulation_saved < n_sims:
            with open(n_sim_loc, "wb") as f:
                pickle.dump(n_sims, f)

            # More simulations are required. Generated emissions can still be re-used,
            # but it is necessary to generate more emissions scenarios for the extra simulations
            # Generate emissions for remaining simulation sets
            for i in range(n_simulation_saved, n_sims):
                if preseed:
                    np.random.seed(emis_preseed_val[i])
                print(rm.GEN_EMISS.format(i=i))
                emis_file_loc = generator_dir / Generator_Files.GEN_INFRA_EMISS.format(i=i)
                emissions: dict = {}
                emissions.update(
                    infrastructure.generate_emissions(
                        sim_start_date=start_date,
                        sim_end_date=end_date,
                        sim_number=i,
                    )
                )
                with open(emis_file_loc, "wb") as f:
                    pickle.dump(emissions, f)

    if preseed:
        seed_timeseries = gen_seed_timeseries(
            sim_end_date=end_date, sim_start_date=start_date, gen_dir=generator_dir
        )
    else:
        seed_timeseries = None
    return seed_timeseries


def read_in_emissions(infrastructure: Infrastructure, generator_dir: Path, sim_numb: int):
    # Load emissions into the pregenerated infrastructure
    emissions: dict = {}
    emis_file_loc = generator_dir / Generator_Files.GEN_INFRA_EMISS.format(i=sim_numb)
    with open(emis_file_loc, "rb") as f:
        emissions: dict = pickle.load(f)
    infrastructure.set_pregen_emissions(emissions[sim_numb], sim_numb)
    return infrastructure
