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

from virtual_world.infrastructure import Infrastructure


def initialize_emissions(
    n_sims,
    hash_file_exist,
    n_sims_match,
    infrastructure,
    virtual_world,
    generator_dir,
):
    # Store params used to generate the pickle files for change detection
    n_simulations: int = n_sims
    if not hash_file_exist:
        # Generate emissions for all simulation sets
        for i in range(n_simulations):
            emissions: dict = {}
            emis_file_loc = generator_dir / f"gen_infrastructure_emissions_{i}.p"
            print(f"Generating emissions for Set_{i} simulations")
            emissions.update(
                infrastructure.generate_emissions(
                    sim_start_date=date(*virtual_world["start_date"]),
                    sim_end_date=date(*virtual_world["end_date"]),
                    sim_number=i,
                )
            )

            pickle.dump(emissions, open(emis_file_loc, "wb"))
    else:
        # Check if the same amount of simulations are required
        if not n_sims_match:
            # More simulations are required. Generated emissions can still be re-used,
            # but it is necessary to generate more emissions scenarios for the extra simulations

            hash_file_loc = generator_dir / "gen_infrastructure_hashes.p"
            gen_infra_hash_dict = pickle.load(open(hash_file_loc, "rb"))

            # Read the previous number of simulations
            gen_n_simulations = gen_infra_hash_dict["n_simulations"]
            # Generate emissions for remaining simulation sets
            for i in range(gen_n_simulations, n_simulations):
                print(f"Generating emissions for Set_{i} simulations")
                emis_file_loc = generator_dir / f"gen_infrastructure_emissions_{i}.p"
                emissions: dict = {}
                emissions.update(
                    infrastructure.generate_emissions(
                        sim_start_date=date(*virtual_world["start_date"]),
                        sim_end_date=date(*virtual_world["end_date"]),
                        sim_number=i,
                    )
                )

                pickle.dump(emissions, open(emis_file_loc, "wb"))
    return None


def read_in_emissions(infrastructure: Infrastructure, generator_dir: Path, sim_numb: int):
    # Load emissions into the pregenerated infrastructure
    emissions: dict = {}
    emis_file_loc = generator_dir / f"gen_infrastructure_emissions_{sim_numb}.p"
    emissions: dict = pickle.load(open(emis_file_loc, "rb"))
    infrastructure.set_pregen_emissions(emissions[sim_numb], sim_numb)
    return infrastructure
