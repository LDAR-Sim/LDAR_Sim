"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        infrastructure
Purpose: The infrastructure module.

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

from datetime import date
import numpy as np
import pandas as pd
from file_processing.output_processing.output_utils import EmisRepairInfo, TsEmisData
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
    process_emission_sources,
)
from file_processing.input_processing.repair_delay_processing import (
    read_in_repair_delay_sources_file,
)
from virtual_world.infrastructure_const import (
    Infrastructure_Constants,
    Virtual_World_To_Prop_Params_Mapping,
)
from virtual_world.sites import Site
from file_processing.input_processing.infrastructure_processing import (
    read_in_infrastructure_files,
    check_site_file,
    get_equip,
)

# TODO: create logic for wrapping up the emissions into a dictionary
# TODO: create logic for unwrapping the emissions dictionary


class Infrastructure:

    def __init__(self, virtual_world, methods, in_dir) -> None:
        self.emission_rate_source_dictionary: dict[str, EmissionsSource] = process_emission_sources(
            inputs_path=in_dir, virtual_world=virtual_world
        )
        self.repair_delay_dataframe: pd.DataFrame = read_in_repair_delay_sources_file(
            inputs_path=in_dir, virtual_world=virtual_world
        )
        self._sites: list[Site] = []
        self.generate_infrastructure(virtual_world=virtual_world, methods=methods, in_dir=in_dir)

    def __reduce__(self):
        args = (self.emission_rate_source_dictionary, self.repair_delay_dataframe, self._sites)
        return (self.__class__._reconstruct, args)

    @classmethod
    def _reconstruct(cls, emission_rate_dict, repair_df, sites):
        instance = cls.__new__(cls)
        instance.emission_rate_source_dictionary = emission_rate_dict
        instance.repair_delay_dataframe = repair_df
        instance._sites = sites
        return instance

    def generate_propagating_params(self, virtual_world, methods) -> dict:
        prop_params_dict: dict = {}
        for (
            param,
            mapping,
        ) in Virtual_World_To_Prop_Params_Mapping.PROPAGATING_PARAMS.items():
            mapping: str
            access_path = mapping.split(".")
            val = virtual_world
            for path in access_path:
                val = val[path]
            prop_params_dict[param] = val

        prop_params_dict["Method_Specific_Params"] = {}
        for (
            param,
            mapping,
        ) in Virtual_World_To_Prop_Params_Mapping.METH_SPEC_PROP_PARAMS.items():
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
        self,
        prop_params: dict,
        site_row_df_info: pd.Series,
        site_type_info: pd.Series,
        methods: list[str],
    ) -> None:
        if site_type_info is not None:
            # Updating propagating parameters with site type info
            for param in Infrastructure_Constants.Site_Type_File_Constants.PROPAGATING_PARAMS:
                site_type_val = site_type_info.get(param, None)
                if site_type_val is not None:
                    prop_params[param] = site_type_val

            for method in methods:
                for (
                    param
                ) in Infrastructure_Constants.Site_Type_File_Constants.METH_SPEC_PROP_PARAMS:
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

    def set_pregen_emissions(self, emissions, sim_number) -> None:
        for site in self._sites:
            site.set_pregen_emissions(emissions[site.get_id()], sim_number)

    # Generate Emissions for all infrastructure
    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        infrastructure_emissions: dict = {}
        for site in self._sites:
            infrastructure_emissions.update(
                site.generate_emissions(
                    sim_start_date,
                    sim_end_date,
                    sim_number,
                    self.emission_rate_source_dictionary,
                    self.repair_delay_dataframe,
                )
            )
        return {sim_number: infrastructure_emissions}

    def activate_emissions(self, date: date, sim_number: int) -> int:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (date): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        new_emissions: int = 0
        for site in self._sites:
            new_emissions += site.activate_emissions(date, sim_number)
        return new_emissions

    def update_emissions_state(self, emis_rep_info: EmisRepairInfo) -> TsEmisData:
        emis_data = TsEmisData()
        for site in self._sites:
            emis_data += site.update_emissions_state(emis_rep_info)
        return emis_data

    def generate_infrastructure(
        self,
        virtual_world,
        methods,
        in_dir,
    ) -> None:
        """[summary]

        Args:
            virtual_world (dict): The virtual world parameters informing site generation.
            in_dir (Path): The path to the inputs directory

        Returns:
            [dict]: sites, Union[dict, None]: leak_timeseries, Union[dict, None]: initial_leaks
        """
        infrastructure_inputs: dict[str, pd.DataFrame] = read_in_infrastructure_files(
            virtual_world, in_dir
        )
        check_site_file(infrastructure_inputs)
        sites_types_provided: bool = "site_types" in infrastructure_inputs

        sites_in: pd.DataFrame = infrastructure_inputs["sites"]

        # Sample sites and shuffle
        n_samples = virtual_world["site_samples"]
        if n_samples is None:
            n_samples = len(sites_in)
        # even if n_samples is None, the sample function is still used to shuffle
        sites_to_make = sites_in.sample(n_samples)

        sites: list[Site] = []

        for header in Infrastructure_Constants.Sites_File_Constants.OPTIONAL_SHARED_HEADERS:
            if (
                header not in sites_to_make.columns.to_list()
                and sites_types_provided
                and header in infrastructure_inputs["site_types"].columns.to_list()
            ):
                sites_to_make[header] = sites_to_make.apply(
                    get_equip, args=(infrastructure_inputs["site_types"],), axis=1
                )

            else:
                sites_to_make[header] = 0

        for sidx, srow in sites_to_make.iterrows():
            site_type_info = None
            if sites_types_provided:
                site_types_info = infrastructure_inputs["site_types"]
                site_type = srow[Infrastructure_Constants.Sites_File_Constants.TYPE]
                site_types_info = site_types_info.loc[
                    site_types_info[Infrastructure_Constants.Site_Type_File_Constants.TYPE]
                    == site_type
                ].iloc[0]
            propagating_params = self.generate_propagating_params(
                virtual_world=virtual_world, methods=methods
            )
            self.update_propagating_params(
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
                start_date=date(*virtual_world["start_date"]),
                methods=methods,
            )

            sites.append(new_site)

        self._sites: list[Site] = sites

    # TODO
    def get_flagged_sites(self, company_id) -> list[Site]:
        return [site for site in self._sites if site.flagged_for_follow_up(company_id)]

    def get_site_avrg_lat_lon(self) -> tuple[int, int]:
        lat_list = []
        lon_list = []
        for site in self._sites:
            lat, lon = site.get_loc()
            lat_list.append(float(lat))
            lon_list.append(float(lon))
        lat_ave = np.mean(lat_list)
        lon_ave = np.mean(lon_list)
        return (lat_ave, lon_ave)

    def gen_summary_emis_data(self, emis_df: pd.DataFrame) -> None:
        row_index: int = 0
        for site in self._sites:
            row_index = site.gen_emis_data(emis_df, row_index)

    def setup(self, methods: list[str]) -> None:
        for site in self._sites:
            site.setup(methods)
