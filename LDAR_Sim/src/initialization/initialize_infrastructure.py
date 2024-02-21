import os
import pickle
from virtual_world.infrastructure import Infrastructure
import hashlib
import json
import numpy as np


def hash_file(file_path) -> str:
    # Construct the hasher object
    hasher: hashlib._Hash = hashlib.md5()

    # Open the file to hash
    with open(file_path, "rb") as f:
        # Add bytes from the file to the hasher chunk by chunk
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    # Return the string containing the hex representation of the hash
    return hasher.hexdigest()


def hash_dict(in_dict) -> str:
    # Convert the dictionary to a string after sorting it by keys.
    # This ensure the same dictionary will produce the same string
    json_str = json.dumps(in_dict, sort_keys=True)
    # Construct the hasher object
    hasher: hashlib._Hash = hashlib.md5()
    # Add the bytes of the string to the hasher
    hasher.update(json_str.encode("utf-8"))
    # Return the string containing the hex representation of the hash
    return hasher.hexdigest()


def initialize_infrastructure(
    methods, virtual_world, generator_dir, in_dir, preseed, preseed_val
) -> Infrastructure:

    if not os.path.exists(generator_dir):
        os.mkdir(generator_dir)

    # Generate Infrastructure for all simulations.
    # If previously generated infrastructure exists, use it instead.
    hash_file_loc = generator_dir / "gen_infrastructure_hashes.p"
    infra_file_loc = generator_dir / "gen_infrastructure.p"
    preseed_loc = generator_dir / "emis_preseed.p"
    # emis_file_loc = generator_dir / "gen_infrastructure_emissions.p"
    # TODO Also add logic to hash the emissions rate sources file. Add logic elsewhere to make
    # that a standard input.

    # Generate md5 hashes for files that can contain infrastructure defining information.
    # A md5 hash is a unique* number
    # (Different files can get the same hash with md5 hashing but it is very uncommon)
    # representing a set of bytes (The contents of any file).
    # By Saving these and comparing them to previously saved values,
    # this allows us to know if the inputs that influence infrastructure have changed so that
    # we can generate new Infrastructure instead of using the old one in that case.
    print("Hashing files")
    sites_file_hash: str = hash_file(in_dir / virtual_world["infrastructure"]["sites_file"])
    site_type_file_hash: str = (
        hash_file(in_dir / virtual_world["infrastructure"]["site_type_file"])
        if virtual_world["infrastructure"]["site_type_file"] is not None
        else None
    )
    equip_group_file_hash: str = (
        hash_file(in_dir / virtual_world["infrastructure"]["equipment_group_file"])
        if virtual_world["infrastructure"]["equipment_group_file"] is not None
        else None
    )
    sources_file_hash: str = (
        hash_file(in_dir / virtual_world["infrastructure"]["sources_file"])
        if virtual_world["infrastructure"]["sources_file"] is not None
        else None
    )
    virtual_world_hash: str = hash_dict(virtual_world)
    print("Done hashing files")

    if not os.path.isfile(hash_file_loc) or not os.path.isfile(infra_file_loc):
        # No previously generated Infrastructure found, generate new Infrastructure
        print("Generating Infrastructure")
        if preseed:
            np.random.seed(preseed_val[0])

        infrastructure: Infrastructure = Infrastructure(
            virtual_world=virtual_world, methods=methods, in_dir=in_dir
        )

        # Save the generated Infrastructure and the input file hashes and the virtual world hash.
        pickle.dump(
            {
                "sites_file": sites_file_hash,
                "site_type_file": site_type_file_hash,
                "equipment_group_file": equip_group_file_hash,
                "sources_file": sources_file_hash,
                "virtual_world": virtual_world_hash,
            },
            open(hash_file_loc, "wb"),
        )
        pickle.dump({"infrastructure": infrastructure}, open(infra_file_loc, "wb"))
        hash_file_exist = False
    else:
        # Read in all the saved hashes from the infrastructure used to generate
        # the previously generated sites.
        gen_infra_hash_dict = pickle.load(open(hash_file_loc, "rb"))
        gen_sites_file_hash: str = gen_infra_hash_dict["sites_file"]
        gen_site_type_file_hash: str = gen_infra_hash_dict["site_type_file"]
        gen_equip_group_file_hash: str = gen_infra_hash_dict["equipment_group_file"]
        gen_sources_file_hash: str = gen_infra_hash_dict["sources_file"]
        gen_virtual_world_hash: str = gen_infra_hash_dict["virtual_world"]

        # Check if all previous hashes match current hashes
        hashes_match: bool = (
            gen_sites_file_hash == sites_file_hash
            and gen_site_type_file_hash == site_type_file_hash
            and gen_equip_group_file_hash == equip_group_file_hash
            and gen_sources_file_hash == sources_file_hash
            and gen_virtual_world_hash == virtual_world_hash
        )

        # Determine what to do next based on if all current hashes match previous hashes
        if hashes_match:
            # The hashes match, meaning it's okay to reuse the previously generated infrastructure,
            # and the previously generated emissions
            infrastructure = pickle.load(open(infra_file_loc, "rb"))["infrastructure"]
            hash_file_exist = True
        else:
            # The hashes do not match,
            # meaning something has changed with the infrastructure or virtual world.
            # Either way, the sites need to be generated anew.
            print("Generating Infrastructure")

            if preseed:
                np.random.seed(preseed_val[0])

            infrastructure: Infrastructure = Infrastructure(
                virtual_world=virtual_world, methods=methods, in_dir=in_dir
            )
            pickle.dump(preseed_val, open(preseed_loc, "wb"))
            # Save the generated Infrastructure,
            # the input file hashes and the virtual world hash.
            pickle.dump(
                {
                    "sites_file": sites_file_hash,
                    "site_type_file": site_type_file_hash,
                    "equipment_group_file": equip_group_file_hash,
                    "sources_file": sources_file_hash,
                    "virtual_world": virtual_world_hash,
                },
                open(hash_file_loc, "wb"),
            )
            pickle.dump({"infrastructure": infrastructure}, open(infra_file_loc, "wb"))

            hash_file_exist = False
    return infrastructure, hash_file_exist
