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


import os
from pathlib import Path, WindowsPath
from typing import Any
import pandas as pd
<<<<<<< Updated upstream
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
from initialization.sites import generate_sites
from initialization.update_methods import (
    est_n_crews,
    est_site_p_day,
    est_t_bw_sites,
    est_min_time_bt_surveys,
)
from campaigns.methods import update_campaigns, setup_campaigns
from methods.company import BaseCompany
from numpy.random import binomial, choice
from out_processing.plotter import make_plots
from utils.attribution import update_tag

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
=======
import numpy as np
from virtual_world.infrastructure import Infrastructure
from time_counter import TimeCounter
from programs.program import Program
from file_processing.output_processing.output_utils import (
    EMIS_SUMMARY_FINAL_COL_ORDER,
    TIMESERIES_COLUMNS,
    TIMESERIES_COL_ACCESSORS as tca,
    EmisRepairInfo,
    TsEmisData,
    TsMethodData,
)
>>>>>>> Stashed changes


class LdarSim:
    SIMULATION_NAME_STR = "{program}_{sim_number}"

    def __init__(
        self,
        sim_number: int,
        simulation_settings,
        virtual_world,
        program: Program,
        infrastructure: Infrastructure,
        input_dir: WindowsPath,
        output_dir: WindowsPath,
        preseed_timeseries,
    ):
        """
        Construct the simulation.
        """
        self._tc: TimeCounter = TimeCounter(virtual_world["start_date"], virtual_world["end_date"])
        self._sim_number: int = sim_number
        self._infrastructure: Infrastructure = infrastructure
        # TODO remove if unused
        self.simulation_settings = simulation_settings
        self._program: Program = program

<<<<<<< Updated upstream
        #  --- state variables ---
        self.state["campaigns"] = {}
        state["candidate_flags"] = {}
        # Read in data files
        if virtual_world["emissions"]["leak_file"] is not None:
            state["empirical_leaks"] = np.array(
                pd.read_csv(input_dir / virtual_world["emissions"]["leak_file"])
            )
        if program_parameters["economics"]["repair_costs"]["file"] is not None:
            repair_cost_df = pd.read_csv(
                input_dir / program_parameters["economics"]["repair_costs"]["file"]
            )
            program_parameters["economics"]["repair_costs"]["vals"] = repair_cost_df[
                repair_cost_df.columns[0]
            ].tolist()
            # Read in the sites as a list of dictionaries
        if len(state["sites"]) < 1:
            state["sites"], _, _ = generate_sites(
                virtual_world, input_dir, virtual_world["pregenerate_leaks"]
            )
        state["max_leak_rate"] = virtual_world["emissions"]["max_leak_rate"]
        state["t"].set_UTC_offset(state["sites"])
        if virtual_world["subtype_file"] is not None:
            state["subtypes"] = pd.read_csv(
                input_dir / virtual_world["subtype_file"], index_col="subtype_code"
            ).to_dict()
        # Sample sites if they have not been provided from pregeneration step
        if not virtual_world["pregenerate_leaks"]:
            if virtual_world["site_samples"] is not None:
                state["sites"] = random.sample(state["sites"], virtual_world["site_samples"])
            # Shuffle all the entries to randomize order for identical 't_Since_last_LDAR' values
            random.shuffle(state["sites"])

        n_subtype_rs = {}
        n_screening_rs_sets = {}
        sites_per_subtype = {}
        # Additional variable(s) for each site
        for site in state["sites"]:
            if site["subtype_code"] not in n_subtype_rs:
                n_subtype_rs.update({site["subtype_code"]: {"natural": -1}})
                sites_per_subtype.update({site["subtype_code"]: 0})
                add_subtype = True
            else:
                add_subtype = False
            sites_per_subtype[site["subtype_code"]] += 1
            n_rs = n_subtype_rs[site["subtype_code"]]
            for m_label, m_obj in program_parameters["methods"].items():
                # Site parameter overwrite of RS and Time (used for sensitivity analysis)
                m_RS = "{}_RS".format(m_label)
                if m_obj["RS"] is not None:
                    site[m_RS] = m_obj["RS"]

                m_min_time_bt_surveys = "{}_min_time_bt_surveys".format(m_label)
                # when provided by user in method
                if m_obj["scheduling"]["min_time_bt_surveys"] is not None:
                    site[m_min_time_bt_surveys] = m_obj["scheduling"]["min_time_bt_surveys"]
                # when not provided
                if (
                    not m_obj["is_follow_up"]
                    and m_obj["deployment_type"] == "mobile"
                    and site[m_RS] > 0
                ):
                    if not (m_min_time_bt_surveys in site):
                        site[m_min_time_bt_surveys] = est_min_time_bt_surveys(
                            m_RS, len(m_obj["scheduling"]["deployment_months"]), site
                        )

                if m_RS in site and m_obj["measurement_scale"] != "component":
                    if m_label not in n_screening_rs_sets:
                        n_screening_rs_sets.update({m_label: site[m_RS]})
                    elif n_screening_rs_sets[m_label] != site[m_RS]:
                        n_screening_rs_sets.update({m_label: "varies"})

                m_time = "{}_time".format(m_label)
                if m_obj["time"] is not None:
                    site[m_time] = m_obj["time"]
                if add_subtype:
                    if m_RS in site:
                        # if scheduled capture the RS value
                        n_subtype_rs[site["subtype_code"]].update({m_label: site[m_RS]})
                    else:
                        # If set rs value to -1 (used for tracking later)
                        n_subtype_rs[site["subtype_code"]].update({m_label: -1})
                        # If the value changes set to None
                elif m_RS in site and (n_rs[m_label] != site[m_RS] or n_rs[m_label] is None):
                    n_subtype_rs[site["subtype_code"]].update({m_label: None})
                # Calculate the site minimum interval
                if m_RS in site and site[m_RS] != 0:
                    n_months = len(
                        program_parameters["methods"][m_label]["scheduling"]["deployment_months"]
                    )
                    n_days = 30.4167 * n_months
                    site["{}_min_int".format(m_label)] = floor(n_days / site[m_RS])
                # Automatically assign 1 crew to followup if left unspecified
                elif m_obj["n_crews"] is None:
                    m_obj["n_crews"] = 1

            if virtual_world["pregenerate_leaks"]:
                initial_leaks = virtual_world["initial_leaks"][site["facility_ID"]]
                n_leaks = len(virtual_world["initial_leaks"][site["facility_ID"]])
            else:
                initial_leaks = generate_initial_leaks(virtual_world, site)
                n_leaks = len(initial_leaks)
            site.update(
                {
                    "total_emissions_kg": 0,
                    "active_leaks": initial_leaks,
                    "repaired_leaks": [],
                    "last_component_survey": None,
                    "historic_t_since_LDAR": None,
                    "tags": [],
                    "initial_leak_cnt": n_leaks,
                    "currently_flagged": False,
                    "flagged_by": None,
                    "date_flagged": None,
                    "crew_ID": None,
                    "lat_index": min(
                        range(len(state["weather"].latitude)),
                        key=lambda i: abs(state["weather"].latitude[i] - float(site["lat"])),
                    ),
                    "lon_index": min(
                        range(len(state["weather"].longitude)),
                        key=lambda i: abs(state["weather"].longitude[i] - float(site["lon"]) % 360),
                    ),
                }
            )

            in_grid, exit_msg = grid_contains_point(
                [site["lat"], site["lon"]],
                [state["weather"].latitude, state["weather"].longitude],
            )
            if not in_grid:
                sys.exit(exit_msg)
        n_sites = len(state["sites"])

        # Setup Campaigns
        setup_campaigns(
            self.state["campaigns"],
            program_parameters,
            virtual_world,
            n_sites,
            n_screening_rs_sets,
=======
        self._input_dir: WindowsPath = input_dir
        self._output_dir: WindowsPath = output_dir / program.name
        self.name_str: str = self.SIMULATION_NAME_STR.format(
            program=program.name, sim_number=sim_number
>>>>>>> Stashed changes
        )
        if preseed_timeseries is not None:
            self._preseed = True
            self._preseed_ts = preseed_timeseries
        else:
            self._preseed = False
        return

    def run_simulation(self):
        ts_columns = self._init_ts_columns()
        timeseries = pd.DataFrame(columns=ts_columns)
        while not self._tc.at_simulation_end():
            if self._preseed:
                np.random.seed(self._preseed_ts[self._tc.current_date])
            new_row: dict[str, Any] = self._init_ts_row()
            new_row[tca.NEW_LEAKS] = self._infrastructure.activate_emissions(
                self._tc.current_date, self._sim_number
            )
            ts_methods_info: list[TsMethodData] = self._program.do_daily_program_deployment()
            ts_emis_rep_info: EmisRepairInfo = EmisRepairInfo()
            ts_emis_info: TsEmisData = self._infrastructure.update_emissions_state(ts_emis_rep_info)
            self._update_ts_row_w_emis_info(
                new_row=new_row, ts_emis_info=ts_emis_info, ts_emis_rep_info=ts_emis_rep_info
            )
            self._update_ts_row_w_methods_info(new_row=new_row, ts_methods_info=ts_methods_info)
            timeseries.loc[len(timeseries)] = new_row
            self._program.update_date()
            self._tc.next_day()

        overall_emission_data: pd.DataFrame = self._infrastructure.gen_summary_emis_data()

<<<<<<< Updated upstream
        self.update_state()  # Update state of sites and leaks
        self.add_leaks()  # Add leaks to the leak pool
        self.deploy_crews()  # Find leaks
        self.repair_leaks()  # Repair leaks
        self.report()  # Assemble any reporting about model state

        # After reporting update campaign

        return

    def update_state(self):
        """
        update the state of active leaks
        """
        if len(self.state["campaigns"]) > 0:
            update_campaigns(
                self.state["campaigns"],
                self.state["sites"],
                self.state["t"].current_timestep,
                self.state["t"].current_date,
            )
        self.active_leaks = []
        for site in self.state["sites"]:
            for leak in site["active_leaks"]:
                leak["days_active"] += 1
                self.active_leaks.append(leak)
                # Tag by natural if leak is due for NR
                if self.virtual_world["subtype_file"] is not None:
                    if leak["days_active"] == self.state["subtypes"]["NRd"][site["subtype_code"]]:
                        update_tag(
                            leak,
                            None,
                            site,
                            self.timeseries,
                            self.state["t"],
                            "natural",
                        )
                else:
                    if leak["days_active"] == self.virtual_world["NRd"]:
                        update_tag(
                            leak,
                            None,
                            site,
                            self.timeseries,
                            self.state["t"],
                            "natural",
                        )

        self.timeseries["active_leaks"].append(len(self.active_leaks))
        self.timeseries["datetime"].append(self.state["t"].current_date)
        #

    def add_leaks(self):
        """
        add new leaks to the leak pool
        """
        # First, determine whether each site gets a new leak or not
        virtual_world = self.virtual_world
        for site in self.state["sites"]:
            new_leak = None
            sidx = site["facility_ID"]
            if virtual_world["pregenerate_leaks"]:
                new_leak = virtual_world["leak_timeseries"][sidx][self.state["t"].current_timestep]
            elif binomial(1, self.virtual_world["emissions"]["LPR"]):
                new_leak = generate_leak(
                    virtual_world, site, self.state["t"].current_date, site["cum_leaks"]
                )
            if new_leak is not None:
                site.update({"n_new_leaks": 1})
                site["cum_leaks"] += 1
                site["active_leaks"].append(new_leak)
            else:
                site.update({"n_new_leaks": 0})
        return

    def deploy_crews(self):
        """
        Loop over all your methods in the simulation and ask them to find some leaks.
        """

        for m in self.state["methods"]:
            m.deploy_crews()

        return

    def repair_leaks(self):
        """
        Repair tagged leaks and remove from tag pool.
        """
        cur_date = self.state["t"].current_date
        cur_ts = self.state["t"].current_timestep
        virtual_world = self.virtual_world
        program_parameters = self.program_parameters
        timeseries = self.timeseries
        state = self.state
        for site in state["sites"]:
            has_repairs = False
            for lidx, lk in enumerate(site["active_leaks"]):
                repair = False
                if lk["tagged"]:
                    # if company is natural then repair immediately
                    if lk["tagged_by_company"] == "natural":
                        repair = True
                    elif (cur_date - lk["date_tagged"]).days >= (
                        site["repair_delay"]
                        + program_parameters["methods"][lk["tagged_by_company"]]["reporting_delay"]
                    ):
                        repair = True

                # Repair Leaks
                if repair:
                    has_repairs = True
                    lk["status"] = "repaired"
                    lk["date_repaired"] = state["t"].current_date
                    lk["repair_delay"] = (lk["date_repaired"] - lk["date_tagged"]).days

                    if lk["day_ts_began"] < 0:
                        duration = cur_ts
                    else:
                        duration = cur_ts - lk["day_ts_began"]

                    lk["volume"] = duration * lk["rate"] * 86.4
                    repair_cost = int(
                        choice(program_parameters["economics"]["repair_costs"]["vals"])
                    )

                    if lk["tagged_by_company"] != "natural":
                        timeseries["repair_cost"][state["t"].current_timestep] += repair_cost
                        timeseries["verification_cost"][
                            state["t"].current_timestep
                        ] += program_parameters["economics"]["verification_cost"]
                        timeseries["total_daily_cost"][state["t"].current_timestep] += (
                            repair_cost + program_parameters["economics"]["verification_cost"]
                        )

                        est_duration = cur_ts - lk["estimated_date_began"]
                        # check if estimate is needed to be kept track of
                        if "estimate_A" in site.keys():
                            if site["estimate_A"]:
                                # Estimated volume in kg. g/s => kg/day is 86.4
                                lk["estimated_volume"] = est_duration * lk["measured_rate"] * 86.4
                            elif site["estimate_B"]:
                                # Estimated volume in kg. g/s => kg/day is 86.4
                                lk["estimated_volume_b"] = est_duration * lk["measured_rate"] * 86.4
                        else:
                            lk["estimated_volume_b"] = 0
                            lk["estimated_volume_a"] = 0
                    else:
                        timeseries["nat_repair_cost"][state["t"].current_timestep] += repair_cost
                        timeseries["total_daily_cost"][state["t"].current_timestep] += repair_cost

            # Update site leaks
            if has_repairs:
                site["repaired_leaks"] += [
                    lk for lk in site["active_leaks"] if lk["status"] == "repaired"
                ]
                site["active_leaks"] = [
                    lk for lk in site["active_leaks"] if lk["status"] != "repaired"
                ]

        return

    def report(self):
        """
        Daily reporting of leaks, repairs, and emissions.
        """
        timeseries = self.timeseries
        state = self.state
        new_leaks = 0
        n_tags = 0
        cum_repaired_leaks = 0
        daily_emissions_kg = 0
        # Update timeseries
        for site in state["sites"]:
            new_leaks += site["n_new_leaks"]
            cum_repaired_leaks += len(site["repaired_leaks"])
            n_tags += site["n_new_leaks"]
            # convert g/s to kg/day
            daily_emissions_kg += sum([lk["rate"] for lk in site["active_leaks"]]) * 86.4
        cur_ts = [state["t"].current_timestep]
        timeseries["new_leaks"][cur_ts] = new_leaks
        timeseries["cum_repaired_leaks"][cur_ts] = cum_repaired_leaks
        timeseries["daily_emissions_kg"][cur_ts] = daily_emissions_kg
        timeseries["rolling_cost_estimate"][cur_ts] = (
            sum(timeseries["total_daily_cost"])
            / (len(timeseries["rolling_cost_estimate"]) + 1)
            * 365
            / 200
        )
        timeseries["n_tags"][state["t"].current_timestep] = n_tags
        return

    def finalize(self):
        """
        Compile and write output files.
        """
        virtual_world = self.virtual_world
        simulation_settings = self.simulation_settings
        program_parameters = self.program_parameters
        leaks = []
        cur_ts = self.state["t"].current_timestep

        # Attribute individual leak emissions to site totals
        for site in self.state["sites"]:
            for lk in site["active_leaks"]:
                if lk["day_ts_began"] < 0:
                    duration = cur_ts
                else:
                    duration = cur_ts - lk["day_ts_began"]
                lk["volume"] = duration * lk["rate"] * 86.4
            site["active_leak_cnt"] = len(site["active_leaks"])
            site["repaired_leak_cnt"] = len(site["repaired_leaks"])
            site["active_leak_emis"] = sum([lk["volume"] for lk in site["active_leaks"]])
            site["repaired_leak_emis"] = sum([lk["volume"] for lk in site["repaired_leaks"]])
            site["total_emissions_kg"] = site["active_leak_emis"] + site["repaired_leak_emis"]
            leaks += site["active_leaks"] + site["repaired_leaks"]
            del site["n_new_leaks"]

        leak_df = pd.DataFrame(leaks)
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
        leaks_active = leak_df[leak_df.status != "repaired"].sort_values("rate", ascending=False)
        leaks_repaired = leak_df[leak_df.status == "repaired"].sort_values("rate", ascending=False)

        if len(leaks_active) > 0:
            leaks_active["cum_frac_leaks"] = list(np.linspace(0, 1, len(leaks_active)))
            leaks_active["cum_rate"] = np.cumsum(leaks_active["rate"])
            leaks_active["cum_frac_rate"] = leaks_active["cum_rate"] / max(leaks_active["cum_rate"])

        if len(leaks_repaired) > 0:
            leaks_repaired["cum_frac_leaks"] = list(np.linspace(0, 1, len(leaks_repaired)))
            leaks_repaired["cum_rate"] = np.cumsum(leaks_repaired["rate"])
            leaks_repaired["cum_frac_rate"] = leaks_repaired["cum_rate"] / max(
                leaks_repaired["cum_rate"]
            )

        leak_df = pd.concat([leaks_active, leaks_repaired])

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
=======
        overall_emission_data = overall_emission_data[
            EMIS_SUMMARY_FINAL_COL_ORDER
            + [
                col
                for col in overall_emission_data.columns
                if col not in EMIS_SUMMARY_FINAL_COL_ORDER
            ]
>>>>>>> Stashed changes
        ]

        self.gen_sim_directory()
        summary_filename = "_".join([self.name_str, "emissions_summary.csv"])
        self.save_results(overall_emission_data, summary_filename)
        self.format_timeseries(timeseries)
        timeseries_filename = "_".join([self.name_str, "timeseries.csv"])
        self.save_results(timeseries, timeseries_filename)

    def _init_ts_columns(self) -> list[str]:
        ts_columns = TIMESERIES_COLUMNS
        for method in self._program.method_names:
            ts_columns.append(tca.METH_DAILY_DEPLOY_COST.format(method=method))
            ts_columns.append(tca.METH_DAILY_FLAGS.format(method=method))
            ts_columns.append(tca.METH_DAILY_TAGS.format(method=method))
            ts_columns.append(tca.METH_DAILY_SITES_VIS.format(method=method))
            ts_columns.append(tca.METH_DAILY_TRAVEL_TIME.format(method=method))
            ts_columns.append(tca.METH_DAILY_SURVEY_TIME.format(method=method))
        return ts_columns

    def _init_ts_row(self):
        new_ts_row: dict[str, Any] = {
            tca.DATE: self._tc.current_date,
            tca.EMIS: 0,
            tca.COST: 0,
            tca.ACT_LEAKS: 0,
            tca.NEW_LEAKS: 0,
            tca.REP_LEAKS: 0,
            tca.NAT_REP_LEAKS: 0,
            tca.TAGGED_LEAKS: 0,
            tca.REP_COST: 0,
            tca.NAT_REP_COST: 0,
        }
        return new_ts_row

    def _update_ts_row_w_emis_info(
        self, new_row: dict[str, Any], ts_emis_info: TsEmisData, ts_emis_rep_info: EmisRepairInfo
    ):
        new_row[tca.EMIS] = ts_emis_info.daily_emis
        new_row[tca.ACT_LEAKS] = ts_emis_info.active_leaks
        new_row[tca.REP_COST] = ts_emis_rep_info.repair_cost
        new_row[tca.REP_LEAKS] = ts_emis_rep_info.leaks_repaired
        new_row[tca.NAT_REP_COST] = ts_emis_rep_info.nat_repair_cost
        new_row[tca.NAT_REP_LEAKS] = ts_emis_rep_info.leaks_nat_repaired

    def _update_ts_row_w_methods_info(
        self, new_row: dict[str, Any], ts_methods_info: list[TsMethodData]
    ) -> None:
        total_daily_cost: float = 0.0
        total_leaks_tagged: int = 0
        for method_info in ts_methods_info:
            total_daily_cost += method_info.daily_deployment_cost
            total_leaks_tagged += np.nan_to_num(method_info.daily_tags)
            new_row[tca.METH_DAILY_DEPLOY_COST.format(method=method_info.method_name)] = (
                method_info.daily_deployment_cost
            )
            new_row[tca.METH_DAILY_TAGS.format(method=method_info.method_name)] = (
                method_info.daily_tags
            )
            new_row[tca.METH_DAILY_FLAGS.format(method=method_info.method_name)] = (
                method_info.daily_flags
            )
            new_row[tca.METH_DAILY_SITES_VIS.format(method=method_info.method_name)] = (
                method_info.sites_visited
            )
            new_row[tca.METH_DAILY_TRAVEL_TIME.format(method=method_info.method_name)] = (
                method_info.travel_time
            )
            new_row[tca.METH_DAILY_SURVEY_TIME.format(method=method_info.method_name)] = (
                method_info.survey_time
            )
        new_row[tca.COST] = total_daily_cost
        new_row[tca.TAGGED_LEAKS] = total_leaks_tagged

    def format_timeseries(self, timeseries: pd.DataFrame) -> None:
        return None

    def gen_sim_directory(self) -> None:
        if not os.path.exists(self._output_dir):
            os.mkdir(self._output_dir)

    def save_results(self, data: pd.DataFrame, filename: str) -> None:
        if data is None:
            return
        filepath: Path = self._output_dir / filename
        data.to_csv(filepath, index=False)
