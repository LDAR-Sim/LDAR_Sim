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
from virtual_world.fugitive_emission import FugitiveEmission
from virtual_world.infrastructure import Infrastructure
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

# from methods.company import BaseCompany
from numpy.random import binomial
from out_processing.plotter import make_plots
from programs.program import Program


class LdarSim:
    def __init__(
        self,
        sim_number,
        simulation_settings,
        virtual_world,
        program: Program,
        infrastructure: Infrastructure,
        input_dir,
        output_dir,
    ):
        """
        Construct the simulation.
        """
        self._tc: TimeCounter = TimeCounter(
            virtual_world["start_date"], virtual_world["end_date"]
        )
        self.sim_number: int = sim_number
        self.infrastructure: Infrastructure = infrastructure
        self.simulation_settings = simulation_settings
        self.program = program

        self.input_dir = input_dir
        self.output_dir = output_dir

        return

    def run_simulation(self):
        while not self._tc.at_simulation_end():
            self.program.do_daily_program_deployment()
            self.program.update_date()
            self._tc.next_day()

    def update(self):
        """
        this rolls the model forward one timestep
        returns nothing
        """
        # TODO : this should be in programs? - Add emissions should still be LDAR_sim, but deploys crews can go
        self.add_emissions()  # Add leaks to the leak pool
        # self.update_state()  # Update state of sites and leaks
        return

    def update_state(self):
        """
        update the state of active leaks
        """
        cur_date = self.state["t"].current_date

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

    def finalize(self):
        """
        Compile and write output files.
        """

        # Write metadata
        f_name = self.output_dir / "metadata_{}.txt".format(virtual_world["simulation"])
        metadata = open(f_name, "w")
        metadata.write(str(virtual_world) + "\n" + str(datetime.datetime.now()))
        metadata.close()

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
        metadata = {
            key: value
            for key, value in virtual_world.items()
            if key in wanted_meta_cols
        }

        metadata.update(
            {
                key: value
                for key, value in program_parameters.items()
                if key in wanted_meta_cols
            }
        )
        metadata.update(
            {
                key: value
                for key, value in simulation_settings.items()
                if key in wanted_meta_cols
            }
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
