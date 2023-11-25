from datetime import datetime
import math
import numpy as np
import pandas as pd

from initialization.infrastructure_const import (
    Infrastructure_Constants,
    Virtual_World_To_Prop_Params_Mapping,
)
from initialization.scheduling import GenericSchedule, create_schedule
from initialization.sites import Site


# TODO: create logic for wrapping up the emissions into a dictionary
# TODO: create logic for unwrapping the emissions dictionary


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
        # TODO: Review the math that was used to update this
        # TODO: to move this function over to scheduling
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

    def get_flagged_sites(self, company_id) -> list[Site]:
        return [site for site in self._sites if site.flagged_for_follow_up(company_id)]
