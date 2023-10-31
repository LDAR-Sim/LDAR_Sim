# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.sites
# Purpose:     Pregenerate sites and regenerate sites
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

import copy
import fnmatch
import os
import pickle

import numpy as np
import pandas as pd

from initialization.infrastructure_const import Infrastructure_Constants
from initialization.leaks import generate_initial_leaks, generate_leak_timeseries
from utils.distributions import fit_dist, unpackage_dist
from utils.emis_inputs import assign_vents
from methods.init_func.repair_delay import determine_delay
from initialization.emissions import FugitiveEmission


def init_generator_files(generator_dir, sim_params, in_dir, virtual_world):
    sites_file = virtual_world["infrastructure_file"]
    sites_in = pd.read_csv(in_dir / sites_file)
    sim_sites = sites_in.to_dict("records")
    if not os.path.exists(generator_dir):
        os.mkdir(generator_dir)
    gen_files = fnmatch.filter(os.listdir(generator_dir), "*.p")
    if len(gen_files) > 0:
        try:
            old_sites = pickle.load(open(generator_dir / "sites.p", "rb"))
            old_params = pickle.load(open(generator_dir / "params.p", "rb"))
        except FileNotFoundError:
            old_sites = None
            old_params = None
            # Check to see if params used to generate the pickle files have changed
        if old_params != sim_params or old_sites != sim_sites:
            for file in gen_files:
                os.remove(generator_dir / file)
    pickle.dump(sim_sites, open(generator_dir / "sites.p", "wb"))
    pickle.dump(sim_params, open(generator_dir / "params.p", "wb"))


def get_subtype_dist(program, wd):
    # Get Sub_type data
    if program["emissions"]["subtype_leak_dist_file"]:
        subtypes = pd.read_csv(
            wd / program["emissions"]["subtype_leak_dist_file"],
            index_col="subtype_code",
        )
        program["subtypes"] = subtypes.to_dict("index")
        for st in program["subtypes"]:
            program["subtypes"][st]["leak_rate_units"] = program["emissions"]["units"]
        unpackage_dist(program, wd)
    elif program["emissions"]["leak_file_use"] == "fit":
        program["subtypes"] = {
            0: {
                "leak_rate_dist": fit_dist(samples=program["empirical_leaks"], dist_type="lognorm"),
                "leak_rate_units": ["gram", "second"],
            }
        }
    elif not program["emissions"]["subtype_leak_dist_file"]:
        program["subtypes"] = {
            0: {
                "dist_type": program["emissions"]["leak_dist_type"],
                "dist_scale": program["emissions"]["leak_dist_params"][0],
                "dist_shape": program["emissions"]["leak_dist_params"][1:],
                "leak_rate_units": program["emissions"]["units"],
            }
        }
        unpackage_dist(program, wd)


def get_site_type_file(program, wd):
    if program["subtype_file"]:
        subtypes = pd.read_csv(wd / program["subtype_file"], index_col="subtype_code")
        program["subtypes"] = subtypes.to_dict("index")
        for st in program["subtypes"]:
            program["subtypes"][st]["leak_rate_units"] = program["emissions"]["units"]
        unpackage_dist(program, wd)
        assign_vents(program, wd)
    elif program["emissions"]["leak_file_use"] == "fit":
        program["subtypes"] = {
            0: {
                "leak_rate_dist": fit_dist(samples=program["empirical_leaks"], dist_type="lognorm"),
                "leak_rate_units": ["gram", "second"],
            }
        }
    elif not program["subtype_file"]:
        program["subtypes"] = {
            0: {
                "dist_type": program["emissions"]["leak_dist_type"],
                "dist_scale": program["emissions"]["leak_dist_params"][0],
                "dist_shape": program["emissions"]["leak_dist_params"][1:],
                "leak_rate_units": program["emissions"]["units"],
            }
        }
        unpackage_dist(program, wd)


def read_in_files(virtual_world, in_dir):
    input_dict = {}

    input_dict["sites"] = pd.read_csv(in_dir / virtual_world["infrastructure"]["sites_file"])

    if virtual_world["infrastructure"]["subtype_file"]:
        input_dict["subtypes"] = pd.read_csv(
            in_dir / virtual_world["infrastructure"]["subtype_file"]
        )

    if virtual_world["infrastructure"]["equipment_group_file"]:
        input_dict["equipment_groups"] = pd.read_csv(
            in_dir / virtual_world["infrastructure"]["equipment_group_file"]
        )

    if virtual_world["infrastructure"]["sources_file"]:
        input_dict["sources"] = pd.read_csv(
            in_dir / virtual_world["infrastructure"]["sources_file"]
        )

    return input_dict


def generate_propagating_params(
    site_row_df_info,
    methods,
):
    prop_params_dict = {}
    prop_params_dict[Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS] = site_row_df_info[
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS
    ]
    prop_params_dict[Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR] = site_row_df_info[
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR
    ]
    prop_params_dict[Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED] = site_row_df_info[
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED
    ]

    prop_params_dict[Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD] = site_row_df_info[
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD
    ]
    prop_params_dict[Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC] = site_row_df_info[
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC
    ]
    prop_params_dict[
        Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ERS
    ] = site_row_df_info[Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ERS]

    prop_params_dict["Method_Specific_Params"] = {}
    prop_params_dict["Method_Specific_Params"][
        Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER
    ] = {}
    prop_params_dict["Method_Specific_Params"][
        Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER
    ] = {}
    prop_params_dict["Method_Specific_Params"][
        Infrastructure_Constants.Sites_File_Constants.SURVEY_TIME_PLACEHOLDER
    ] = {}
    prop_params_dict["Method_Specific_Params"][
        Infrastructure_Constants.Sites_File_Constants.SURVEY_COST_PLACEHOLDER
    ] = {}

    for method in methods:
        prop_params_dict["Method_Specific_Params"][
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER
        ][method] = site_row_df_info.get(
            method + Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER,
            None,
        )
        prop_params_dict["Method_Specific_Params"][
            Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER
        ][method] = site_row_df_info.get(
            method + Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER,
            None,
        )
        prop_params_dict["Method_Specific_Params"][
            Infrastructure_Constants.Sites_File_Constants.SURVEY_TIME_PLACEHOLDER
        ][method] = site_row_df_info.get(
            method + Infrastructure_Constants.Sites_File_Constants.SURVEY_TIME_PLACEHOLDER,
            None,
        )
        prop_params_dict["Method_Specific_Params"][
            Infrastructure_Constants.Sites_File_Constants.SURVEY_COST_PLACEHOLDER
        ][method] = site_row_df_info.get(
            method + Infrastructure_Constants.Sites_File_Constants.SURVEY_COST_PLACEHOLDER,
            None,
        )

    return prop_params_dict


def generate_infrastructure(virtual_world, in_dir, pregen_leaks, start_date, end_date):
    """[summary]

    Args:
        virtual_world (dict): The virtual world parameters informing site generation.
        in_dir (Path): The path to the inputs directory
        pregen_leaks (boolean): Boolean indicating whether or not to pregenerate leaks.

    Returns:
        [dict]: sites, Union[dict, None]: leak_timeseries, Union[dict, None]: initial_leaks
    """
    infrastructure_inputs: dict[str, pd.DataFrame] = read_in_files(virtual_world, in_dir)

    sites_in: pd.DataFrame = infrastructure_inputs["sites"]

    # Sample sites and shuffle
    n_samples = virtual_world["site_samples"]
    if n_samples is None:
        n_samples = len(sites_in)
    # even if n_samples is None, the sample function is still used to shuffle
    sites_to_make = sites_in.sample(n_samples)

    sites: list[Site] = []
    methods = None  # TODO Update this placeholder with logic to get actual methods

    for sidx, srow in sites_to_make.iterrows():
        propagating_params = generate_propagating_params(srow, methods)
        new_site = Site(
            id=srow[Infrastructure_Constants.Sites_File_Constants.ID],
            lat=srow[Infrastructure_Constants.Sites_File_Constants.LAT],
            long=srow[Infrastructure_Constants.Sites_File_Constants.LON],
            equipment_groups=srow[Infrastructure_Constants.Sites_File_Constants.EQG],
            propagating_params=propagating_params,
            infrastructure_inputs=infrastructure_inputs,
        )

        sites.append(new_site)

    # Get leaks from file
    if virtual_world["emissions"]["leak_file"] is not None:
        virtual_world["emissions"]["empirical_leaks"] = np.array(
            pd.read_csv(in_dir / virtual_world["emissions"]["leak_file"]).iloc[:, 0]
        )

    # get_subtype_dist(program, in_dir)
    get_site_type_file(virtual_world, infrastructure_inputs)

    leak_timeseries = {}
    initial_leaks: dict[str, list[FugitiveEmission]] = {}
    # Additional variable(s) for each site
    for site in sites:
        # Add a distribution and unit for each leak
        if len(virtual_world["subtypes"]) > 1:
            # Get all keys from subtypes
            for col in virtual_world["subtypes"][next(iter(virtual_world["subtypes"]))]:
                site[col] = virtual_world["subtypes"][site["subtype_code"]][col]
        elif len(virtual_world["subtypes"]) > 0:
            site.update(virtual_world["subtypes"][0])

        # Determine repair delay for each site
        site["repair_delay"] = determine_delay(virtual_world)

        if pregen_leaks:
            initial_site_leaks: list[FugitiveEmission] = generate_initial_leaks(
                virtual_world, site, start_date
            )
            initial_leaks.update({site["facility_ID"]: initial_site_leaks})
            site_timeseries: list[FugitiveEmission] = generate_leak_timeseries(
                virtual_world, site, start_date, end_date
            )
            leak_timeseries.update({site["facility_ID"]: site_timeseries})
            if "leak_rate_dist" in site:
                del site["leak_rate_dist"]

    return sites


def regenerate_sites(virtual_world, prog_0_sites, in_dir):
    """
    Regenerate sites allows site level parameters to update on pregenerated
    sites. This is necessary when programs have different site level params
    for example, the survey frequency or survey time could be different.
    """
    # Read in the sites as a list of dictionaries
    sites_in = pd.read_csv(in_dir / virtual_world["infrastructure_file"], index_col="facility_ID")
    # Add facility ID back into object
    sites_in["facility_ID"] = sites_in.index
    sites = sites_in.to_dict("index")
    out_sites = []
    for site_or in prog_0_sites:
        s_idx = site_or["facility_ID"]
        new_site = copy.deepcopy(sites[s_idx])
        new_site.update(
            {
                "cum_leaks": site_or["cum_leaks"],
                "initial_leaks": site_or["initial_leaks"],
                "leak_rate_units": site_or["leak_rate_units"],
                "repair_delay": site_or["repair_delay"],
            }
        )
        if "empirical_leak_rates" in site_or:
            new_site.update({"empirical_leak_rates": site_or["empirical_leak_rates"]})
        if "leak_rate_dist" in site_or:
            new_site.update(
                {
                    "leak_rate_dist": site_or["leak_rate_dist"],
                }
            )
        if "empirical_vent_rates" in site_or:
            new_site.update({"empirical_vent_rates": site_or["empirical_vent_rates"]})
        out_sites.append(new_site)
    return out_sites


class Site_Type:
    def __init__(
        self, equipment_groups: list, infrastructure_inputs: dict, site_type: str = None
    ) -> None:
        self._site_type: str = site_type
        self._RS: dict = {}
        self._spatial_coverage: dict = {}
        self._survey_time: dict = {}
        self._survey_cost: dict = {}
        self.create_equipment_groups(equipment_groups, infrastructure_inputs)

    def create_Sites(self, infrastructure_inputs):
        return

    def add_RS(self, method, survey_frequency):
        self._RS[method] = survey_frequency

    def add_spatial_coverage(self, method, spatial_coverage):
        self._spatial_coverage[method] = spatial_coverage

    def add_survey_time(self, method, survey_time):
        self._survey_time[method] = survey_time

    def add_survey_cost(self, method, survey_cost):
        self._survey_cost[method] = survey_cost


class Site:
    def __init__(
        self,
        id: str,
        lat: float,
        long: float,
        equipment_groups: list,
        propagating_params: dict,
        infrastructure_inputs: dict,
        site_type: str = None,
    ) -> None:
        self._site_ID: str = id
        self._lat: float = lat
        self._long: float = long

        self._site_type: str = site_type
        self._RS: dict = propagating_params.pop("Method_Survey_Frequencies")
        self.create_equipment_groups(equipment_groups, infrastructure_inputs, propagating_params)

    def add_RS(self, method, survey_frequency):
        self._RS[method] = survey_frequency

    def add_spatial_coverage(self, method, spatial_coverage):
        self._spatial_coverage[method] = spatial_coverage

    def add_survey_time(self, method, survey_time):
        self._survey_time[method] = survey_time

    def add_survey_cost(self, method, survey_cost):
        self._survey_cost[method] = survey_cost

    def create_equipment_groups(
        self, equipment_groups, infrastructure_inputs, propagating_params, methods
    ) -> None:
        self._equipment_groups = []
        if len(equipment_groups) > 0:
            equip_groups_in: pd.DataFrame = infrastructure_inputs["equipment_groups"]
            for equipment_group in equipment_groups:
                site_equipment_group = equip_groups_in.loc[
                    equip_groups_in[
                        Infrastructure_Constants.Equipment_Group_File_Constants.EQUIPMENT_GROUP
                    ]
                    == equipment_group
                ].iloc[0]
                prop_params = copy.deepcopy(propagating_params)
                self._equipment_groups.append(
                    Equipment_Group(
                        site_equipment_group[
                            Infrastructure_Constants.Equipment_Group_File_Constants.EQUIPMENT_GROUP
                        ],
                        infrastructure_inputs,
                        prop_params,
                        site_equipment_group,
                    )
                )
        else:
            # TODO Implement logic for when a site has no equipment groups
            return


class Equipment_Group:
    def __init__(self, id, infrastructure_inputs, prop_params, info):
        self._id: str = id
        self.update_prop_params(info, prop_params)
        self.create_equipment(
            infrastructure_inputs=infrastructure_inputs, prop_params=prop_params, info=info
        )

    def update_prop_params(self, info, prop_params) -> None:
        meth_specific_params = prop_params.pop("Method_Specific_Params")
        eqg_info = info["equipment_groups"]

        for param in meth_specific_params.keys():
            for method in meth_specific_params[param].keys():
                eqg_val = eqg_info.get(param + method, None)
                if eqg_val is not None:
                    meth_specific_params[param][method] = eqg_val

        for param in prop_params.keys():
            eqg_val = eqg_info.get(param, None)
            if eqg_val is not None:
                prop_params[param] = eqg_val

        prop_params["Method_Specific_Params"] = meth_specific_params

    def create_equipment(self, infrastructure_inputs, prop_params, info) -> None:
        self._equipment = []
        for col, val in info.iteritems():
            if "equipment" in col:
                for count in range(0, val):
                    self._equipment.append(Equipment(col, count))

    def report_func(self):
        # some reporting agregate function?
        return


class Equipment:
    def __init__(self, id, repair_delay) -> None:
        self._equipment_ID: str = id
        self._site_ID: Site = None
        self._repair_delay = repair_delay
        self._surveytime: dict = {}
        self._spatialcoverage: dict = {}

    def add_surveytime(self, method, surveytime):
        # Create a parameter dictionary for the given method
        self._surveytime[method] = surveytime  # Store the parameters in the dictionary

    def add_spatialcoverage(self, method, spatialcoverage):
        # Create a parameter dictionary for the given method

        self._spatialcoverage[method] = spatialcoverage  # Store the parameters in the dictionary

    def get_spatialcoverage(self, method):
        # Retrieve parameters for the given method, or return an empty dictionary if not found
        return self._spatialcoverage.get(method, {})

    def list_methods(self):
        # List all methods for which parameters are defined
        return list(self._parameters.keys())


class Source:
    def __init__(
        self,
        id: str,
        emiss_prob: float,
        duration: int,
        repairable: bool,
        emiss_source,
        emiss_type: str,
        equipment_ID: str,
    ) -> None:
        self._source_ID: str = id

        self._emiss_prob: float = emiss_prob
        self._duration: int = duration
        self._repairable: bool = repairable
        self._equipment_ID: str = equipment_ID

        self._emiss_source = emiss_source
        self._emiss_type: str = emiss_type

    # def create_emission(self):
    #     if type(self._emiss_source) == str and emiss_type.lower() == 'sample':

    #         # add in code to deal with source file
    #     elif type(self._emiss_source) == str and emiss_type.lower() == 'fit':
    #         # add in code to deal with source file and fitting to distribution
    #     elif type(self._emiss_source) == list and emiss_type.lower() == 'sample':
    #         emiss_val = emiss_source
    #     elif type(self._emiss_source) == float or type(emiss_source) == int:
    #         emiss_val = [emiss_source]
    #     elif type(self._emiss_source) == list and emiss_type.lower() == 'dist':
    #         # add in code to deal with handling a distribution

    # the above may be required to be moved to the emissions object.
