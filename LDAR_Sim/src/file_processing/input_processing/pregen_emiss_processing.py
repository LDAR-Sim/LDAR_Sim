"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        pregen_processing
Purpose: Module for processing generated emissions

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
import pickle
from datetime import date


from virtual_world.infrastructure import Infrastructure


def process_gen_emissions(
    n_sims,
    hash_file_exist,
    n_sims_match,
    infrastructure,
    virtual_world,
    generator_dir,
):
    # Store params used to generate the pickle files for change detection
    n_simulations: int = n_sims
    emis_file_loc = generator_dir / "gen_infrastructure_emissions.p"

    if not hash_file_exist:
        # Generate emissions for all simulation sets
        emissions: dict = {}
        for i in range(n_simulations):
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
        emissions: dict = pickle.load(open(emis_file_loc, "rb"))

        # Check if the same amount of simulations are required
        if n_sims_match:
            # Load Previously Generated Emissions back into Previously Generated infrastructure
            for i in range(n_simulations):
                infrastructure.set_pregen_emissions(emissions[i], i)
        else:
            # More simulations are required. Generated emissions can still be re-used,
            # but it is necessary to generate more emissions scenarios for the extra simulations

            hash_file_loc = generator_dir / "gen_infrastructure_hashes.p"
            gen_infra_hash_dict = pickle.load(open(hash_file_loc, "rb"))

            # Read the previous number of simulations
            gen_n_simulations = gen_infra_hash_dict["n_simulations"]
            # Load Emissions back into pregenerated infrastructure
            for i in range(gen_n_simulations):
                infrastructure.set_pregen_emissions(emissions[i], i)

            # Generate emissions for remaining simulation sets
            for i in range(gen_n_simulations, n_simulations):
                print(f"Generating emissions for Set_{i} simulations")
                emissions.update(
                    infrastructure.generate_emissions(
                        sim_start_date=date(*virtual_world["start_date"]),
                        sim_end_date=date(*virtual_world["end_date"]),
                        sim_number=i,
                    )
                )

            pickle.dump(emissions, open(emis_file_loc, "wb"))

        # Generate emissions for all simulation sets
        emissions: dict = {}
        for i in range(n_simulations):
            print(f"Generating emissions for Set_{i} simulations")
            emissions.update(
                infrastructure.generate_emissions(
                    sim_start_date=date(*virtual_world["start_date"]),
                    sim_end_date=date(*virtual_world["end_date"]),
                    sim_number=i,
                )
            )

        pickle.dump(emissions, open(emis_file_loc, "wb"))
    return None
