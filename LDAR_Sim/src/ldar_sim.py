# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim
# Purpose:     Primary module of LDAR-Sim
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


import datetime
import random
import sys
import warnings
from math import floor
import numpy as np
import pandas as pd
from initialization.emissions import FugitiveEmission
from initialization.infrastructure import Infrastructure
from time_counter import TimeCounter
from weather.daylight_calculator import DaylightCalculatorAve
from config.output_flag_mapping import (
    OUTPUTS,
    SITE_VISITS,
    SITES,
    LEAKS,
    TIMESERIES,
    PLOTS,
)
from geography.vector import grid_contains_point
from initialization.leaks import generate_initial_leaks, generate_leak
from initialization.update_methods import (
    est_n_crews,
    est_site_p_day,
    est_t_bw_sites,
    est_min_time_bt_surveys,
)
from campaigns.methods import update_campaigns, setup_campaigns
from methods.company import BaseCompany
from numpy.random import binomial
from out_processing.plotter import make_plots

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class LdarSim:
    def __init__(
        self,
        sim_number,
        simulation_settings,
        state,
        program_parameters,
        virtual_world,
        infrastructure: Infrastructure,
        timeseries,
        input_dir,
        output_dir,
    ):
        """
        Construct the simulation.
        """
        self.sim_number: int = sim_number
        self.state = state
        self.infrastructure: Infrastructure = infrastructure
        self.simulation_settings = simulation_settings
        self.virtual_world = virtual_world
        self.program_parameters = program_parameters
        self.timeseries = timeseries
        self.active_leaks = []
        self.input_dir = input_dir
        self.output_dir = output_dir

        #  --- state variables ---
        self.state["campaigns"] = {}
        state["candidate_flags"] = {}
        state["max_leak_rate"] = virtual_world["emissions"]["max_leak_rate"]

        #  --- timeseries variables ---
        timeseries["total_daily_cost"] = np.zeros(virtual_world["timesteps"])
        timeseries["repair_cost"] = np.zeros(virtual_world["timesteps"])
        timeseries["nat_repair_cost"] = np.zeros(virtual_world["timesteps"])
        timeseries["verification_cost"] = np.zeros(virtual_world["timesteps"])
        timeseries["natural_redund_tags"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["natural_n_tags"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["new_leaks"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["cum_repaired_leaks"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["daily_emissions_kg"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["n_tags"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["rolling_cost_estimate"] = np.zeros(self.virtual_world["timesteps"])
        timeseries["rolling_cost_estimate_b"] = np.zeros(self.virtual_world["timesteps"])

        # Initialize method(s) to be used; append to state
        calculate_daylight = False
        infrastructure.initialize_survey_schedules(program_parameters["methods"])
        method_est_crews: dict = infrastructure.estimate_method_crews_required(
            program_parameters["methods"].items()
        )
        for m_label, m_obj in program_parameters["methods"].items():
            # Initialize method site_visit tracking
            state["site_visits"][m_label] = []
            # Update method parameters
            m_obj_wr = program_parameters["methods"][m_label]
            if m_obj["n_crews"] is None:
                m_obj_wr["n_crews"] = method_est_crews[m_label]
            if m_obj["t_bw_sites"]["file"] is not None:
                m_obj_wr["t_bw_sites"]["vals"] = np.array(
                    pd.read_csv(input_dir / m_obj["t_bw_sites"]["file"]).iloc[:, 0]
                )
            if m_obj["consider_daylight"]:
                calculate_daylight = True
            try:
                state["methods"].append(
                    BaseCompany(
                        state,
                        infrastructure,
                        program_parameters,
                        virtual_world,
                        simulation_settings,
                        m_obj,
                        timeseries,
                        m_label,
                    )
                )
            except AttributeError:
                print("Cannot add this method: " + m_label)

        # Initialize daylight
        if calculate_daylight:
            state["daylight"] = DaylightCalculatorAve(state, virtual_world)

        return

    def update(self):
        """
        this rolls the model forward one timestep
        returns nothing
        """

        self.add_emissions()  # Add leaks to the leak pool
        self.deploy_crews()  # Find leaks
        self.update_state()  # Update state of sites and leaks
        return

    def update_state(self):
        """
        update the state of active leaks
        """
        timeseries = self.timeseries
        cur_ts = self.state["t"].current_timestep
        cur_date = self.state["t"].current_date
        program_economics = self.program_parameters["economics"]

        if len(self.state["campaigns"]) > 0:
            update_campaigns(self.state["campaigns"], self.state["sites"], cur_ts, cur_date)

        new_leaks = 0
        daily_emissions_kg = 0
        n_tags = 0
        cum_repaired_leaks = 0
        active_leaks = 0

        for site in self.state["sites"]:
            new_leaks += site["n_new_leaks"]

            has_repairs = False
            for leak in site["active_leaks"]:
                leak: FugitiveEmission

                active_leaks += 1

                daily_emissions_kg += leak.get_daily_emissions()

                if leak.tagged_today():
                    n_tags += 1

                leak_status = leak.update_emissions()
                if "repaired" in leak_status:
                    cum_repaired_leaks += 1
                    repair_cost: float = leak.get_repair_cost()
                    timeseries["total_daily_cost"][cur_ts] += repair_cost
                    has_repairs = True

                    if leak_status == "nat_repaired":
                        timeseries["nat_repair_cost"][cur_ts] += repair_cost
                        timeseries["natural_n_tags"][cur_ts] += 1
                    elif leak_status == "repaired":
                        verification_cost = program_economics["verification_cost"]
                        timeseries["verification_cost"][cur_ts] += verification_cost
                        timeseries["total_daily_cost"][cur_ts] += verification_cost
                        timeseries["repair_cost"][cur_ts] += repair_cost
            if has_repairs:
                site["repaired_leaks"] += [
                    lk for lk in site["active_leaks"] if lk.get_status() == "repaired"
                ]
                site["active_leaks"] = [
                    lk for lk in site["active_leaks"] if lk.get_status() != "repaired"
                ]

        timeseries["new_leaks"][cur_ts] = new_leaks
        timeseries["daily_emissions_kg"][cur_ts] = daily_emissions_kg
        timeseries["n_tags"][cur_ts] = n_tags
        timeseries["cum_repaired_leaks"][cur_ts] = cum_repaired_leaks

        timeseries["rolling_cost_estimate"][cur_ts] = (
            sum(timeseries["total_daily_cost"])
            / (len(timeseries["rolling_cost_estimate"]) + 1)
            * 365
            / 200
        )

        timeseries["datetime"].append(cur_date)
        timeseries["active_leaks"].append(active_leaks)

        return

    def add_emissions(self):
        """
        add new emissions to infrastructure in the simulation
        """
        time_counter: TimeCounter = self.state["t"]
        cur_date: datetime = time_counter.current_date
        infrastructure: Infrastructure = self.infrastructure
        infrastructure.activate_emissions(cur_date, self.sim_number)
        return

    def deploy_crews(self):
        """
        Loop over all your methods in the simulation and ask them to find some leaks.
        """

        for m in self.state["methods"]:
            m.deploy_crews()

        return

    def finalize(self):
        """
        Compile and write output files.
        """
        virtual_world = self.virtual_world
        simulation_settings = self.simulation_settings
        program_parameters = self.program_parameters
        leaks: list[FugitiveEmission] = []

        # Attribute individual leak emissions to site totals
        for site in self.state["sites"]:
            active_leak_emis = 0
            repaired_leak_emis = 0

            for lk in site["active_leaks"]:
                lk: FugitiveEmission
                active_leak_emis += lk.get_emis_vol()

            for lk in site["repaired_leaks"]:
                lk: FugitiveEmission
                repaired_leak_emis += lk.get_emis_vol()

            site["active_leak_cnt"] = len(site["active_leaks"])
            site["repaired_leak_cnt"] = len(site["repaired_leaks"])
            site["active_leak_emis"] = active_leak_emis
            site["repaired_leak_emis"] = repaired_leak_emis
            site["total_emissions_kg"] = site["active_leak_emis"] + site["repaired_leak_emis"]
            leaks += site["active_leaks"] + site["repaired_leaks"]
            del site["n_new_leaks"]

        leaks_data = [leak.get_summary_dict() for leak in leaks]
        leak_df = pd.DataFrame(leaks_data)
        leaks_data = [leak.get_summary_dict() for leak in leaks]
        leak_df = pd.DataFrame(leaks_data)
        time_df = pd.DataFrame(self.timeseries)
        site_df = pd.DataFrame(self.state["sites"])

        # Create site_visit dataframes
        site_visits: dict[str, pd.DataFrame] = {}
        for meth, meth_visits in self.state["site_visits"].items():
            site_visits[meth] = pd.DataFrame((meth_visits))

        # Create some new variables for plotting
        site_df["cum_frac_sites"] = list(site_df.index)
        site_df["cum_frac_sites"] = site_df["cum_frac_sites"] / max(site_df["cum_frac_sites"])
        site_df["cum_frac_emissions"] = np.cumsum(
            sorted(site_df["total_emissions_kg"], reverse=True)
        )
        site_df["cum_frac_emissions"] = site_df["cum_frac_emissions"] / max(
            site_df["cum_frac_emissions"]
        )
        site_df["mean_rate_kg_day"] = site_df["total_emissions_kg"] / virtual_world["timesteps"]

        # Write csv files
        if simulation_settings[OUTPUTS][LEAKS]:
            leak_df.to_csv(
                self.output_dir
                / "leaks_output_{}_{}.csv".format(
                    virtual_world["simulation"], program_parameters["program_name"]
                ),
                index=False,
            )

        if simulation_settings[OUTPUTS][TIMESERIES]:
            time_df.to_csv(
                self.output_dir
                / "timeseries_output_{}_{}.csv".format(
                    virtual_world["simulation"], program_parameters["program_name"]
                ),
                index=False,
            )

        if simulation_settings[OUTPUTS][SITES]:
            site_df.to_csv(
                self.output_dir
                / "sites_output_{}_{}.csv".format(
                    virtual_world["simulation"], program_parameters["program_name"]
                ),
                index=False,
            )

        if simulation_settings[OUTPUTS][SITE_VISITS]:
            for meth, meth_vis_df in site_visits.items():
                meth_vis_df.to_csv(
                    self.output_dir / f"site_visits_{meth}_{virtual_world['simulation']}.csv",
                    index=False,
                )

        # Write metadata
        f_name = self.output_dir / "metadata_{}.txt".format(virtual_world["simulation"])
        metadata = open(f_name, "w")
        metadata.write(str(virtual_world) + "\n" + str(datetime.datetime.now()))
        metadata.close()

        # Make plots
        if self.simulation_settings[OUTPUTS][PLOTS]:
            make_plots(leak_df, time_df, site_df, virtual_world["simulation"], self.output_dir)

        # Extract necessary information from the parameters
        wanted_c_economics = [
            "sale_price_natgas",
            "GWP_CH4",
            "carbon_price_tonnesCO2e",
            "cost_CCUS",
        ]
        carbon_economics = {
            key: value
            for key, value in program_parameters["economics"].items()
            if key in wanted_c_economics
        }

        # Extract Metadata
        wanted_meta_cols = ["program_name", "simulation", "NRd", "start_date"]
        metadata = {key: value for key, value in virtual_world.items() if key in wanted_meta_cols}

        metadata.update(
            {key: value for key, value in program_parameters.items() if key in wanted_meta_cols}
        )
        metadata.update(
            {key: value for key, value in simulation_settings.items() if key in wanted_meta_cols}
        )

        sim_summary = {
            "meta": metadata,
            "leaks": leak_df,
            "timeseries": time_df,
            "sites": site_df,
            "program_name": program_parameters["program_name"],
            "p_c_economics": carbon_economics,
        }

        return sim_summary
