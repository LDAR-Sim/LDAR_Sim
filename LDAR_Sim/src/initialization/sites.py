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

import array
import copy
import fnmatch
import os
import pickle
import re
from typing import Literal
import numpy as np

import pandas as pd

from initialization.infrastructure_const import Infrastructure_Constants
from initialization.emissions import Emission


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
        self._RS: dict = propagating_params["Method_Specific_Params"].pop(
            "Method_Survey_Frequencies"
        )
        self.create_equipment_groups(equipment_groups, infrastructure_inputs, propagating_params)

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
                        ]
                        + self._site_ID,
                        infrastructure_inputs,
                        prop_params,
                        site_equipment_group,
                    )
                )
        else:
            # TODO Implement logic for when a site has no equipment groups
            return

    def generate_emissions(self) -> None:
        for eqg in self._equipment_groups:
            eqg.generate_emissions()


class Equipment_Group:
    def __init__(self, id, infrastructure_inputs, prop_params, info):
        self._id: str = id
        self.update_prop_params(info, prop_params)
        self.create_equipment(
            infrastructure_inputs=infrastructure_inputs, prop_params=prop_params, info=info
        )

    def update_prop_params(self, info, prop_params) -> None:
        meth_specific_params = prop_params.pop("Method_Specific_Params")

        for param in meth_specific_params.keys():
            for method in meth_specific_params[param].keys():
                eqg_val = info.get(method + param, None)
                if eqg_val is not None:
                    meth_specific_params[param][method] = eqg_val

        for param in prop_params.keys():
            eqg_val = info.get(param, None)
            if eqg_val is not None:
                prop_params[param] = eqg_val

        prop_params["Method_Specific_Params"] = meth_specific_params

    def create_equipment(self, infrastructure_inputs, prop_params, info) -> None:
        self._equipment = []
        for col, val in info.iteritems():
            if "equipment" in col:
                for count in range(0, val):
                    self._equipment.append(
                        Equipment(col, count, infrastructure_inputs, prop_params)
                    )

    def generate_emissions(self) -> None:
        for eqmt in self._equipment:
            eqmt.generate_emissions()

    def report_func(self):
        # some reporting agregate function?
        return


class Equipment:
    def __init__(self, equip_type, equip_id, infrastructure_inputs, prop_params) -> None:
        STR_FILTER = r"equipment"
        self._equip_type = re.sub(STR_FILTER, "", equip_type)
        self._equipment_ID: str = self._equip_type + "_" + equip_id
        self.create_sources(infrastructure_inputs=infrastructure_inputs, prop_params=prop_params)

    def create_sources(self, infrastructure_inputs, prop_params) -> None:
        self._sources = []
        sources_info = infrastructure_inputs["sources"]
        sources = sources_info.loc[
            sources_info[Infrastructure_Constants.Sources_File_Constants.EQUIPMENT]
            == self._equip_type
        ]
        for source in sources:
            src_prop_params = copy.deepcopy(prop_params)
            src_id = source[Infrastructure_Constants.Sources_File_Constants.SOURCE]
            self._sources.append(Source(src_id, source, src_prop_params))

    def generate_emissions(self) -> None:
        for src in self._sources:
            src.generate_emissions()


class Source:
    REP_PREFIX = "repairable_"
    NON_REP_PREFIX = "non_repairable_"

    def __init__(self, id: str, info, prop_params) -> None:
        self._source_ID: str = id
        self._repairable = info[Infrastructure_Constants.Sources_File_Constants.REPAIRABLE]
        self._persistent = info[Infrastructure_Constants.Sources_File_Constants.PERSISTENT]
        self._active_duration = info[Infrastructure_Constants.Sources_File_Constants.ACTIVE_DUR]
        self._inactive_duration = info[Infrastructure_Constants.Sources_File_Constants.INACTIVE_DUR]
        self.update_prop_params(info=info, prop_params=prop_params)
        self.set_source_properties(prop_params=prop_params)

    def update_prop_params(self, info, prop_params) -> None:
        meth_specific_params = prop_params.pop("Method_Specific_Params")

        prefix: Literal["repairable", "non_repairable"] = (
            Source.REP_PREFIX if self._repairable else Source.NON_REP_PREFIX
        )

        for param in meth_specific_params.keys():
            for method in meth_specific_params[param].keys():
                src_val = info.get(method + param, None)
                if src_val is not None:
                    meth_specific_params[param][method] = src_val

        for param in prop_params.keys():
            if prefix in param:
                src_param = re.sub(prefix, "", param)
                src_val = info.get(src_param, None)
                if src_val is not None:
                    del prop_params[param]
                    prop_params[src_param] = src_val
            else:
                del prop_params[param]

        prop_params["Method_Specific_Params"] = meth_specific_params

    def set_source_properties(self, prop_params) -> None:
        self._emis_rate_source = prop_params[
            Infrastructure_Constants.Sources_File_Constants.EMIS_ERS
        ]
        self._emis_prod_rate = prop_params[Infrastructure_Constants.Sources_File_Constants.EMIS_EPR]
        self._emis_duration = prop_params[Infrastructure_Constants.Sources_File_Constants.EMIS_DUR]

        self._meth_spat_covs = prop_params["Method_Specific_Params"][
            Infrastructure_Constants.Sources_File_Constants.SPATIAL_PLACEHOLDER
        ]

        self._meth_surv_times = prop_params["Method_Specific_Params"][
            Infrastructure_Constants.Sources_File_Constants.SURVEY_TIME_PLACEHOLDER
        ]

        self._meth_surv_costs = prop_params["Method_Specific_Params"][
            Infrastructure_Constants.Sources_File_Constants.SURVEY_COST_PLACEHOLDER
        ]

        if self._repairable:
            self._emis_rep_delay = prop_params[
                Infrastructure_Constants.Sources_File_Constants.REPAIR_DELAY
            ]
            self._emis_rep_cost = prop_params[
                Infrastructure_Constants.Sources_File_Constants.REPAIR_COST
            ]

    def generate_emissions(self) -> None:
        sim_dur = 365
        self._emis_ts = array.array(Emission)
        for day in range(0, sim_dur + self._emis_duration):
            emission = None
            create_emis: int = np.random.binomial(1, self._emis_prod_rate)
            if create_emis:
                emission = self.create_emission()
            self._emis_ts.append(emission)

    def create_emissions(self) -> None:
        return None

    # def create_emission(self):
    #     if type(self._emis_rate_source) == str and emiss_type.lower() == 'sample':

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


def init_generator_files(generator_dir, sim_params, in_dir, virtual_world):
    sites_file = virtual_world["infrastructure"]["sites_file"]
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


def read_in_files(virtual_world, in_dir):
    input_dict = {}

    input_dict["sites"] = pd.read_csv(in_dir / virtual_world["infrastructure"]["sites_file"])

    if virtual_world["infrastructure"]["site_type_file"]:
        input_dict["site_types"] = pd.read_csv(
            in_dir / virtual_world["infrastructure"]["site_type_file"]
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
    site_type_info,
    methods,
):
    prop_params_dict = {}
    if site_type_info is not None:
        # Updating propagating parameters with site type info
        for param in Infrastructure_Constants.Site_Type_File_Constants.PROPAGATING_PARAMS:
            site_type_val = site_type_info.get(param, None)
            prop_params_dict[param] = site_type_val

        # Update method specific propagating params with site type info
        prop_params_dict["Method_Specific_Params"] = {}
        for param in Infrastructure_Constants.Site_Type_File_Constants.METH_SPEC_PROP_PARAMS:
            prop_params_dict["Method_Specific_Params"][param] = {}

        for method in methods:
            for param in Infrastructure_Constants.Site_Type_File_Constants.METH_SPEC_PROP_PARAMS:
                site_type_val = site_type_info.get(method + param, None)
                prop_params_dict["Method_Specific_Params"][param][method] = site_type_val

        # Updating propagating parameters with site info
        for param in Infrastructure_Constants.Sites_File_Constants.PROPAGATING_PARAMS:
            site_val = site_row_df_info.get(param, None)
            if site_val is not None:
                prop_params_dict[param] = site_val

        # Update method specific propagating params with site info
        for method in methods:
            for param in Infrastructure_Constants.Sites_File_Constants.METH_SPEC_PROP_PARAMS:
                site_val = site_row_df_info.get(method + param, None)
                if site_val is not None:
                    prop_params_dict["Method_Specific_Params"][param][method] = site_val

    else:
        # Updating propagating parameters with site info
        for param in Infrastructure_Constants.Sites_File_Constants.PROPAGATING_PARAMS:
            site_val = site_row_df_info.get(param, None)
            prop_params_dict[param] = site_val

        # Update method specific propagating params with site info
        prop_params_dict["Method_Specific_Params"] = {}

        for param in Infrastructure_Constants.Sites_File_Constants.METH_SPEC_PROP_PARAMS:
            prop_params_dict["Method_Specific_Params"][param] = {}

        for method in methods:
            for param in Infrastructure_Constants.Sites_File_Constants.METH_SPEC_PROP_PARAMS:
                site_val = site_row_df_info.get(method + param, None)
                if site_val is not None:
                    prop_params_dict["Method_Specific_Params"][param][method] = site_val

    return prop_params_dict


def generate_infrastructure(virtual_world, in_dir, start_date, end_date) -> list[Site]:
    """[summary]

    Args:
        virtual_world (dict): The virtual world parameters informing site generation.
        in_dir (Path): The path to the inputs directory

    Returns:
        [dict]: sites, Union[dict, None]: leak_timeseries, Union[dict, None]: initial_leaks
    """
    infrastructure_inputs: dict[str, pd.DataFrame] = read_in_files(virtual_world, in_dir)
    sites_types_provided: bool = "site_types" in infrastructure_inputs

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
        site_type_info = None
        if sites_types_provided:
            site_types_info = infrastructure_inputs["site_types"]
            site_type = srow[Infrastructure_Constants.Sites_File_Constants.ID]
            site_types_info = site_types_info.loc[
                site_types_info[Infrastructure_Constants.Site_Type_File_Constants.TYPE] == site_type
            ].iloc[0]
        propagating_params = generate_propagating_params(
            site_row_df_info=srow, site_type_info=site_type_info, methods=methods
        )
        new_site = Site(
            id=srow[Infrastructure_Constants.Sites_File_Constants.ID],
            lat=srow[Infrastructure_Constants.Sites_File_Constants.LAT],
            long=srow[Infrastructure_Constants.Sites_File_Constants.LON],
            equipment_groups=srow[Infrastructure_Constants.Sites_File_Constants.EQG],
            propagating_params=propagating_params,
            infrastructure_inputs=infrastructure_inputs,
        )

        sites.append(new_site)

    # Generate Emissions for all infrastructure
    for site in sites:
        site.generate_emissions()

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
