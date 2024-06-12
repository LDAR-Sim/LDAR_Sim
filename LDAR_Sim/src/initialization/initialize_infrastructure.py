import os
import pickle
from virtual_world.infrastructure import Infrastructure
import hashlib
import json
import numpy as np
from constants.file_name_constants import Generator_Files
import constants.param_default_const as pc
from constants.output_messages import RuntimeMessages as rm


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
    methods,
    programs,
    virtual_world,
    generator_dir,
    in_dir,
    preseed,
    preseed_val,
    force_remake,
    site_measured_df,
) -> Infrastructure:

    if not os.path.exists(generator_dir):
        os.mkdir(generator_dir)

    # Generate Infrastructure for all simulations.
    # If previously generated infrastructure exists, use it instead.
    hash_file_loc = generator_dir / Generator_Files.HASH_FILE
    infra_file_loc = generator_dir / Generator_Files.INFRA_FILE

    # Generate md5 hashes for files that can contain infrastructure defining information.
    # A md5 hash is a unique* number
    # (Different files can get the same hash with md5 hashing but it is very uncommon)
    # representing a set of bytes (The contents of any file).
    # By Saving these and comparing them to previously saved values,
    # this allows us to know if the inputs that influence infrastructure have changed so that
    # we can generate new Infrastructure instead of using the old one in that case.
    print(rm.HASHING)
    sites_file_hash: str = hash_file(
        in_dir / virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.SITE]
    )
    site_type_file_hash: str = (
        hash_file(
            in_dir / virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.SITE_TYPE]
        )
        if virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.SITE_TYPE]
        is not None
        else None
    )
    equip_group_file_hash: str = (
        hash_file(
            in_dir / virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.EQUIP]
        )
        if virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.EQUIP] is not None
        else None
    )
    sources_file_hash: str = (
        hash_file(
            in_dir / virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.SOURCE]
        )
        if virtual_world[pc.Virtual_World_Params.INFRA][pc.Virtual_World_Params.SOURCE] is not None
        else None
    )
    virtual_world_hash: str = hash_dict(virtual_world)
    program_hash: str = hash_dict(programs)
    print(rm.HASHING_COMPLETE)

    if not os.path.isfile(hash_file_loc) or not os.path.isfile(infra_file_loc) or force_remake:
        # No previously generated Infrastructure found, generate new Infrastructure
        print(rm.GEN_INFRA)
        if preseed:
            np.random.seed(preseed_val[0])

        infrastructure: Infrastructure = Infrastructure(
            virtual_world=virtual_world,
            methods=methods,
            in_dir=in_dir,
            site_measured_df=site_measured_df,
        )

        # Save the generated Infrastructure and the input file hashes and the virtual world hash.
        with open(hash_file_loc, "wb") as f:
            pickle.dump(
                {
                    pc.Virtual_World_Params.SITE: sites_file_hash,
                    pc.Virtual_World_Params.SITE_TYPE: site_type_file_hash,
                    pc.Virtual_World_Params.EQUIP: equip_group_file_hash,
                    pc.Virtual_World_Params.SOURCE: sources_file_hash,
                    pc.Levels.VIRTUAL: virtual_world_hash,
                    pc.Levels.PROGRAM: program_hash,
                },
                f,
            )
        with open(infra_file_loc, "wb") as f:
            pickle.dump({pc.Virtual_World_Params.INFRA: infrastructure}, f)
        hash_file_exist = False
    else:
        # Read in all the saved hashes from the infrastructure used to generate
        # the previously generated sites.
        with open(hash_file_loc, "rb") as f:
            gen_infra_hash_dict = pickle.load(f)
        gen_sites_file_hash: str = gen_infra_hash_dict[pc.Virtual_World_Params.SITE]
        gen_site_type_file_hash: str = gen_infra_hash_dict[pc.Virtual_World_Params.SITE_TYPE]
        gen_equip_group_file_hash: str = gen_infra_hash_dict[pc.Virtual_World_Params.EQUIP]
        gen_sources_file_hash: str = gen_infra_hash_dict[pc.Virtual_World_Params.SOURCE]
        gen_virtual_world_hash: str = gen_infra_hash_dict[pc.Levels.VIRTUAL]
        gen_program_hash: str = gen_infra_hash_dict[pc.Levels.PROGRAM]

        # Check if all previous hashes match current hashes
        hashes_match: bool = (
            gen_sites_file_hash == sites_file_hash
            and gen_site_type_file_hash == site_type_file_hash
            and gen_equip_group_file_hash == equip_group_file_hash
            and gen_sources_file_hash == sources_file_hash
            and gen_virtual_world_hash == virtual_world_hash
            and gen_program_hash == program_hash
        )

        # Determine what to do next based on if all current hashes match previous hashes
        if hashes_match:
            # The hashes match, meaning it's okay to reuse the previously generated infrastructure,
            # and the previously generated emissions
            with open(infra_file_loc, "rb") as f:
                infrastructure = pickle.load(f)[pc.Virtual_World_Params.INFRA]
            hash_file_exist = True
        else:
            # The hashes do not match,
            # meaning something has changed with the infrastructure or virtual world.
            # Either way, the sites need to be generated anew.
            print(rm.GEN_INFRA)

            if preseed:
                np.random.seed(preseed_val[0])

            infrastructure: Infrastructure = Infrastructure(
                virtual_world=virtual_world,
                methods=methods,
                in_dir=in_dir,
                site_measured_df=site_measured_df,
            )
            # Save the generated Infrastructure,
            # the input file hashes and the virtual world hash.
            with open(hash_file_loc, "wb") as f:
                pickle.dump(
                    {
                        pc.Virtual_World_Params.SITE: sites_file_hash,
                        pc.Virtual_World_Params.SITE_TYPE: site_type_file_hash,
                        pc.Virtual_World_Params.EQUIP: equip_group_file_hash,
                        pc.Virtual_World_Params.SOURCE: sources_file_hash,
                        pc.Levels.VIRTUAL: virtual_world_hash,
                        pc.Levels.PROGRAM: program_hash,
                    },
                    f,
                )
            with open(infra_file_loc, "wb") as f:
                pickle.dump({pc.Virtual_World_Params.INFRA: infrastructure}, f)

            hash_file_exist = False
    return infrastructure, hash_file_exist
