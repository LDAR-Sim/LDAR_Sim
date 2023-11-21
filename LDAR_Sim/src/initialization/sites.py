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
from datetime import datetime, timedelta
import fnmatch
import math
import os
import pickle
import re
from typing import Literal
import numpy as np

import pandas as pd

from initialization.infrastructure_const import (
    Infrastructure_Constants,
    Virtual_World_To_Prop_Params_Mapping,
)
from initialization.emissions import Emission, FugitiveEmission

PLACEHOLDER_EQUIPMENT_COUNT = 10
PLACEHOLDER_EQUIPMENT = "Placeholder_Equipment"
SOURCE_CREATION_ERROR_MESSAGE = (
    "Invalid LDAR-Sim infrastructure inputs: Failure to read in sources infrastructure input"
)


class Source:
    REP_PREFIX = "repairable_"
    NON_REP_PREFIX = "non_repairable_"

    def __init__(self, id: str, info, prop_params) -> None:
        self._source_ID: str = id
        self._repairable = info[Infrastructure_Constants.Sources_File_Constants.REPAIRABLE]
        self._persistent = info[Infrastructure_Constants.Sources_File_Constants.PERSISTENT]
        self._active_duration = info[Infrastructure_Constants.Sources_File_Constants.ACTIVE_DUR]
        self._inactive_duration = info[Infrastructure_Constants.Sources_File_Constants.INACTIVE_DUR]
        self._generated_emissions: dict[int, list[Emission]] = {}
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

        prop_params_keys = list(prop_params.keys())
        for param in prop_params_keys:
            if prefix in param:
                src_param = re.sub(prefix, "", param)
                src_val = info.get(src_param, None)
                if src_val is not None:
                    prop_params[src_param] = src_val
                else:
                    prop_val = prop_params[param]
                    prop_params[src_param] = prop_val

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

        if self._repairable:
            self._emis_rep_delay = prop_params[
                Infrastructure_Constants.Sources_File_Constants.REPAIR_DELAY
            ]
            self._emis_rep_cost = prop_params[
                Infrastructure_Constants.Sources_File_Constants.REPAIR_COST
            ]

    def _get_rate(self):
        return self._emis_rate_source

    def _get_repairable(self):
        return self._repairable

    def _get_rep_delay(self):
        return self._emis_rep_delay

    def _get_rep_cost(self):
        return self._emis_rep_cost

    def _get_emis_duration(self):
        return self._emis_duration

    def _create_emission(self, leak_count, start_date, sim_start_date) -> Emission:
        if self._repairable:
            return FugitiveEmission(
                emission_n=leak_count,
                rate=self._get_rate(),
                start_date=start_date,
                simulation_sd=sim_start_date,
                repairable=self._get_repairable(),
                repair_delay=self._get_rep_delay(),
                repair_cost=self._get_rep_cost(),
                nrd=self._get_emis_duration(),
            )

    def generate_emissions(
        self, sim_start_date: datetime, sim_end_date: datetime, sim_number: int
    ) -> dict[str, list[Emission]]:
        emissions: list[Emission] = []

        # Initialize a counter to give all leaks for the source a unique "ID"
        leak_count: int = 0

        # Generate Pre-Existing Emissions to exist at the start of simulation
        # The loop is working backwards in time, starting from 1 day before simulation start
        for day in range(1, self._emis_duration + 1):
            create_emis: int = np.random.binomial(1, self._emis_prod_rate)
            if create_emis:
                emis_start_date: datetime = sim_start_date - timedelta(days=day)
                emission: Emission = self._create_emission(
                    leak_count=leak_count, start_date=emis_start_date, sim_start_date=sim_start_date
                )
                leak_count += 1
                emissions.append(emission)

        # Generate Emissions for the course of the simulation
        date_diff: timedelta = sim_end_date - sim_start_date
        sim_dur: int = date_diff.days

        for day in range(0, sim_dur):
            create_emis: int = np.random.binomial(1, self._emis_prod_rate)
            if create_emis:
                emis_start_date: datetime = sim_start_date + timedelta(days=day)
                emission: Emission = self._create_emission(
                    leak_count=leak_count, start_date=emis_start_date, sim_start_date=sim_start_date
                )
                leak_count += 1
                emissions.append(emission)
        self._generated_emissions[sim_number] = emissions
        return {self._source_ID: emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> list[Emission]:
        """Activate any emissions produced by the source that are due to begin on the current date
        for the given simulation and return them in a list.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.

        Returns:
            list[Emission]: The list of emissions that are newly active on the current date
        """
        newly_activated_emissions: list[Emission] = []
        sim_emissions: list[Emission] = self._generated_emissions[sim_number]
        for emission in sim_emissions:
            activate_status: str = emission.activate(date)
            if activate_status == "Inactive":
                break
            elif activate_status == "Newly_Active":
                newly_activated_emissions.append[emission]
        return newly_activated_emissions

    def set_pregen_emissions(self, src_emissions, sim_number) -> None:
        self._generated_emissions[sim_number] = src_emissions

    def get_id(self) -> str:
        return self._source_ID

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


class Equipment:
    def __init__(self, equip_type, equip_id, infrastructure_inputs, prop_params) -> None:
        STR_FILTER = r"_equipment"
        pattern: re.Pattern[str] = re.compile(re.escape(STR_FILTER), re.IGNORECASE)
        self._equip_type: str = re.sub(pattern, "", equip_type)
        self._equipment_ID: str = self._equip_type + "_" + str(equip_id)
        self.create_sources(infrastructure_inputs=infrastructure_inputs, prop_params=prop_params)

    def create_sources(self, infrastructure_inputs, prop_params) -> None:
        self._sources: list[Source] = []
        if self._equip_type != "Placeholder" and "sources" in infrastructure_inputs:
            sources_info = infrastructure_inputs["sources"]
            sources = sources_info.loc[
                sources_info[Infrastructure_Constants.Sources_File_Constants.EQUIPMENT]
                == self._equip_type
            ]
            for source in sources:
                src_prop_params = copy.deepcopy(prop_params)
                src_id = source[Infrastructure_Constants.Sources_File_Constants.SOURCE]
                self._sources.append(Source(src_id, source, src_prop_params))
        elif self._equip_type == "Placeholder":
            src_id = "Placeholder_Non_Rep"
            placeholder_source_info = {
                Infrastructure_Constants.Sources_File_Constants.REPAIRABLE: True,
                Infrastructure_Constants.Sources_File_Constants.PERSISTENT: True,
                Infrastructure_Constants.Sources_File_Constants.ACTIVE_DUR: 1,
                Infrastructure_Constants.Sources_File_Constants.INACTIVE_DUR: 0,
            }
            self._sources.append(Source(src_id, placeholder_source_info, prop_params))
        else:
            print(SOURCE_CREATION_ERROR_MESSAGE)

    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        equip_emissions = {}
        for src in self._sources:
            equip_emissions.update(src.generate_emissions(sim_start_date, sim_end_date, sim_number))

        return {self._equipment_ID: equip_emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        for source in self._sources:
            active_emissions: list[Emission] = source.activate_emissions(date, sim_number)

    def set_pregen_emissions(self, equipment_emissions, sim_number) -> None:
        for src in self._sources:
            src.set_pregen_emissions(equipment_emissions[src.get_id()], sim_number)

    def get_id(self) -> str:
        return self._equipment_ID


class Equipment_Group:
    def __init__(self, id, infrastructure_inputs, prop_params, info) -> None:
        self._id: str = id
        self.update_prop_params(info, prop_params)
        self.set_method_specific_params(prop_params)
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
        self._equipment: list[Equipment] = []
        for col, val in info.items():
            if "equipment" in col.lower():
                for count in range(0, val):
                    self._equipment.append(
                        Equipment(col, count, infrastructure_inputs, prop_params)
                    )

    def set_method_specific_params(self, prop_params):
        self._meth_survey_times = prop_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER
        )
        self._meth_survey_costs = prop_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER
        )

    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        eqg_emissions = {}
        for eqmt in self._equipment:
            eqg_emissions.update(eqmt.generate_emissions(sim_start_date, sim_end_date, sim_number))

        return {self._id: eqg_emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        for equipment in self._equipment:
            equipment.activate_emissions(date, sim_number)

    def set_pregen_emissions(self, eqg_emissions, sim_number) -> None:
        for equipment in self._equipment:
            equipment.set_pregen_emissions(eqg_emissions[equipment.get_id()], sim_number)

    def get_survey_time(self, method_name) -> float:
        survey_time: float = self._meth_survey_times[method_name]
        return survey_time

    def report_func(self):
        # some reporting agregate function?
        return

    def get_id(self) -> str:
        return self._id


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
        self._survey_frequencies: dict = propagating_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER
        )
        self.create_equipment_groups(equipment_groups, infrastructure_inputs, propagating_params)

    def create_equipment_groups(
        self, equipment_groups, infrastructure_inputs, propagating_params
    ) -> None:
        self._equipment_groups: list[Equipment_Group] = []
        if isinstance(equipment_groups, list) and len(equipment_groups) > 0:
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
        elif isinstance(equipment_groups, (int, float)):
            for i in range(0, equipment_groups):
                equip_group_info = pd.Series(
                    {
                        PLACEHOLDER_EQUIPMENT: math.ceil(
                            PLACEHOLDER_EQUIPMENT_COUNT / equipment_groups
                        )
                    }
                )
                prop_params = copy.deepcopy(propagating_params)
                self._equipment_groups.append(
                    Equipment_Group(i, infrastructure_inputs, prop_params, equip_group_info)
                )
        else:
            equip_group_info = pd.Series(
                {PLACEHOLDER_EQUIPMENT: math.ceil(PLACEHOLDER_EQUIPMENT_COUNT)}
            )
            prop_params = copy.deepcopy(propagating_params)
            self._equipment_groups.append(
                Equipment_Group(i, infrastructure_inputs, prop_params, equip_group_info)
            )

    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        site_emissions: dict = {}
        for eqg in self._equipment_groups:
            eqg: Equipment_Group
            site_emissions.update(eqg.generate_emissions(sim_start_date, sim_end_date, sim_number))

        return {self._site_ID: site_emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        for eqg in self._equipment_groups:
            eqg.activate_emissions(date, sim_number)

    def set_pregen_emissions(self, site_emissions, sim_number) -> None:
        for eqg in self._equipment_groups:
            eqg.set_pregen_emissions(site_emissions[eqg.get_id()], sim_number)

    def get_required_surveys(self, method_name) -> int:
        return self._survey_frequencies[method_name]

    def get_method_survey_time(self, method_name) -> float:
        survey_time: float = 0
        for eqg in self._equipment_groups:
            survey_time += eqg.get_survey_time(method_name=method_name)
        return survey_time

    def get_id(self) -> str:
        return self._site_ID


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


def generate_propagating_params(virtual_world, methods) -> dict:
    prop_params_dict: dict = {}
    for param, mapping in Virtual_World_To_Prop_Params_Mapping.PROPAGATING_PARAMS.items():
        mapping: str
        access_path = mapping.split(".")
        val = virtual_world
        for path in access_path:
            val = val[path]
        prop_params_dict[param] = val

    prop_params_dict["Method_Specific_Params"] = {}
    for param, mapping in Virtual_World_To_Prop_Params_Mapping.METH_SPEC_PROP_PARAMS.items():
        prop_params_dict["Method_Specific_Params"][param] = {}
        for method in methods:
            access_path: list[str] = mapping.split(".")
            val = None
            val = methods[method]
            for path in access_path:
                val = val[path]
            prop_params_dict["Method_Specific_Params"][param][method] = val

    return prop_params_dict


def update_propagating_params(
    prop_params,
    site_row_df_info,
    site_type_info,
    methods,
):
    if site_type_info is not None:
        # Updating propagating parameters with site type info
        for param in Infrastructure_Constants.Site_Type_File_Constants.PROPAGATING_PARAMS:
            site_type_val = site_type_info.get(param, None)
            if site_type_val is not None:
                prop_params[param] = site_type_val

        for method in methods:
            for param in Infrastructure_Constants.Site_Type_File_Constants.METH_SPEC_PROP_PARAMS:
                site_type_val = site_type_info.get(method + param, None)
                if site_type_val is not None:
                    prop_params["Method_Specific_Params"][param][method] = site_type_val

        # Updating propagating parameters with site info
        for param in Infrastructure_Constants.Sites_File_Constants.PROPAGATING_PARAMS:
            site_val = site_row_df_info.get(param, None)
            if site_val is not None:
                prop_params[param] = site_val

        # Update method specific propagating params with site info
        for method in methods:
            for param in Infrastructure_Constants.Sites_File_Constants.METH_SPEC_PROP_PARAMS:
                site_val = site_row_df_info.get(method + param, None)
                if site_val is not None:
                    prop_params["Method_Specific_Params"][param][method] = site_val


class Infrastructure:
    def __init__(self, virtual_world, methods, in_dir) -> None:
        self.generate_infrastructure(virtual_world=virtual_world, methods=methods, in_dir=in_dir)

    def set_pregen_emissions(self, emissions, sim_number) -> None:
        for site in self._sites:
            site.set_pregen_emissions(emissions[site.get_id()], sim_number)

    # Generate Emissions for all infrastructure
    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        sim_start_date = datetime(*sim_start_date)
        sim_end_date = datetime(*sim_end_date)
        infrastructure_emissions: dict = {}
        for site in self._sites:
            infrastructure_emissions.update(
                site.generate_emissions(sim_start_date, sim_end_date, sim_number)
            )
        return {sim_number: infrastructure_emissions}

    def get_average_method_survey_time(self, method_name, avg_travel_time) -> float:
        return np.average(
            [(site.get_method_survey_time(method_name) + avg_travel_time) for site in self._sites]
        )

    def get_average_method_surveys_required(self, method_name) -> float:
        return np.average([site.get_required_surveys(method_name) for site in self._sites])

    def estimate_method_crews_required(self, methods) -> dict:
        method_req_crews_dict: dict = {}
        for method in methods:
            method_name: str = method[0]
            if not method[1]["is_follow_up"]:
                avg_travel_time: float = np.average(method[1]["t_bw_sites"]["vals"])
                avg_method_s_time: float = self.get_average_method_survey_time(
                    method_name, avg_travel_time
                )
                average_req_surveys: float = self.get_average_method_surveys_required(method_name)
                # Subtract average travel time here to account the method needing to return
                # at the end of the day
                daily_work_time: float = (method[1]["max_workday"] * 60) - avg_travel_time
                est_avg_sites_p_day: float = daily_work_time / avg_method_s_time
                avg_days_for_surveys: float = 365 / average_req_surveys
                estimate_req_n_crews: int = math.ceil(
                    len(self._sites) / (est_avg_sites_p_day * avg_days_for_surveys)
                )
                method_req_crews_dict[method_name] = estimate_req_n_crews

            else:
                method_req_crews_dict[method_name] = 1

        return method_req_crews_dict

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        for site in self._sites:
            site.activate_emissions(date, sim_number)

    def generate_infrastructure(self, virtual_world, methods, in_dir) -> list[Site]:
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

        for sidx, srow in sites_to_make.iterrows():
            site_type_info = None
            if sites_types_provided:
                site_types_info = infrastructure_inputs["site_types"]
                site_type = srow[Infrastructure_Constants.Sites_File_Constants.ID]
                site_types_info = site_types_info.loc[
                    site_types_info[Infrastructure_Constants.Site_Type_File_Constants.TYPE]
                    == site_type
                ].iloc[0]
            propagating_params = generate_propagating_params(
                virtual_world=virtual_world, methods=methods
            )
            update_propagating_params(
                propagating_params,
                site_row_df_info=srow,
                site_type_info=site_type_info,
                methods=methods,
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

        self._sites: list[Site] = sites
