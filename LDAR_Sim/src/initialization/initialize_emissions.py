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

# TODO create logic to read in the generated emission file
# TODO move over and cleanup all logic to read in previously
# generated infrastructure and emissions
from pathlib import Path
import pickle
from datetime import date
import numpy as np
from virtual_world.infrastructure import Infrastructure
from initialization.preseed import gen_seed_timeseries, get_seed_timeseries


def initialize_emissions(
    n_sims: int,
    preseed: bool,
    hash_file_exist: bool,
    infrastructure: Infrastructure,
    start_date: date,
    end_date: date,
    generator_dir: Path,
):

    # Store params used to generate the pickle files for change detection
    if not hash_file_exist:
        if preseed:
            seed_timeseries = gen_seed_timeseries(
                sim_end_date=end_date, sim_start_date=start_date, gen_dir=generator_dir
            )
            emissions_preseed: list[int] = []
        else:
            seed_timeseries = None
        # Generate emissions for all simulation sets
        for i in range(n_sims):
            if preseed:
                emis_preseed: int = np.random.randint(0, 255)
                np.random.seed(emis_preseed)
                emissions_preseed.append(emis_preseed)
            emissions: dict = {}
            emis_file_loc = generator_dir / f"gen_infrastructure_emissions_{i}.p"
            print(f"Generating emissions for Set_{i} simulations")
            emissions.update(
                infrastructure.generate_emissions(
                    sim_start_date=start_date,
                    sim_end_date=end_date,
                    sim_number=i,
                )
            )

            pickle.dump(emissions, open(emis_file_loc, "wb"))
        if preseed:
            emis_preseed_loc = generator_dir / "emis_preseed.p"
            pickle.dump(emissions_preseed, open(emis_preseed_loc, "wb"))
    else:
        n_sim_loc = generator_dir / "n_sim_saved.p"
        n_simulation_saved = 0
        with open(n_sim_loc, "rb") as f:
            n_simulation_saved = pickle.load(f)

        if n_simulation_saved < n_sims:
            n_sim = n_simulation_saved
            pickle.dump(n_sim, open(n_sim_loc, "wb"))
            if preseed:
                emis_preseed_loc = generator_dir / "emis_preseed.p"
                emissions_preseed: list[int] = []
                with open(emis_preseed_loc, "rb") as f:
                    emissions_preseed = pickle.load(f)
            # More simulations are required. Generated emissions can still be re-used,
            # but it is necessary to generate more emissions scenarios for the extra simulations
            # Generate emissions for remaining simulation sets
            # TODO: need to account for if you have pre-gen seed files but no actual emission files.
            for i in range(n_simulation_saved, n_sims):
                if preseed:
                    emis_preseed: int = np.random.randint(0, 255)
                    np.random.seed(emis_preseed)
                    emissions_preseed.append(emis_preseed)
                print(f"Generating emissions for Set_{i} simulations")
                emis_file_loc = generator_dir / f"gen_infrastructure_emissions_{i}.p"
                emissions: dict = {}
                emissions.update(
                    infrastructure.generate_emissions(
                        sim_start_date=start_date,
                        sim_end_date=end_date,
                        sim_number=i,
                    )
                )

                pickle.dump(emissions, open(emis_file_loc, "wb"))
            if preseed:
                pickle.dump(emissions_preseed, open(emis_preseed_loc, "rb"))
        if preseed:
            seed_timeseries = get_seed_timeseries(generator_dir)
        else:
            seed_timeseries = None
    return seed_timeseries


def read_in_emissions(infrastructure: Infrastructure, generator_dir: Path, sim_numb: int):
    # Load emissions into the pregenerated infrastructure
    emissions: dict = {}
    emis_file_loc = generator_dir / f"gen_infrastructure_emissions_{sim_numb}.p"
    emissions: dict = pickle.load(open(emis_file_loc, "rb"))
    infrastructure.set_pregen_emissions(emissions[sim_numb], sim_numb)
    return infrastructure
