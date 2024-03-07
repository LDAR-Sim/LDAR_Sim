"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        sources
Purpose: The sources module. Sources are used to create emissions.

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

from datetime import date, timedelta
import re
import sys
from typing import Literal

import numpy as np
import pandas as pd
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
)
from virtual_world.emissions import Emission
from virtual_world.fugitive_emission import FugitiveEmission
from virtual_world.infrastructure_const import Infrastructure_Constants


class Source:
    WIP_NON_FUG_EMIS_GENERATION_MSG = (
        "Error: Non-Fugitive Emissions generation is still in development."
        " Please remove these sources for now"
    )
    INVALID_REPAIR_DELAY_COL_MSG = "Error, Invalid repair delay column provided: {key}"
    INVALID_REPAIR_DELAY_ERR_MSG = "Error, Invalid repair delay provided: {delay}"
    REP_PREFIX = "repairable_"
    NON_REP_PREFIX = "non_repairable_"

    def __init__(self, id: str, info, prop_params) -> None:
        self._source_ID: str = id
        self._repairable: bool = info[Infrastructure_Constants.Sources_File_Constants.REPAIRABLE]
        self._persistent: bool = info[Infrastructure_Constants.Sources_File_Constants.PERSISTENT]
        self._active_duration: int = info[
            Infrastructure_Constants.Sources_File_Constants.ACTIVE_DUR
        ]
        self._inactive_duration: int = info[
            Infrastructure_Constants.Sources_File_Constants.INACTIVE_DUR
        ]
        self._generated_emissions: dict[int, list[Emission]] = {}
        self._emis_rate_source: EmissionsSource = None
        self._emis_prod_rate: float = None
        self._emis_duration: int = None
        self._meth_spat_covs: dict[str, float] = None
        self._emis_rep_delay: int = None
        self._emis_rep_cost: float = None
        self._update_prop_params(info=info, prop_params=prop_params)
        self._set_source_properties(prop_params=prop_params)
        self._next_emission: Emission = None

    def __reduce__(self):
        args = (
            self._source_ID,
            self._repairable,
            self._persistent,
            self._active_duration,
            self._inactive_duration,
            self._generated_emissions,
            self._emis_rate_source,
            self._emis_prod_rate,
            self._emis_duration,
            self._meth_spat_covs,
            self._emis_rep_delay,
            self._emis_rep_cost,
            self._next_emission,
        )
        return (self.__class__._reconstruct, args)

    @classmethod
    def _reconstruct(
        cls,
        source_ID,
        repairable,
        persistent,
        active_duration,
        inactive_duration,
        generated_emissions,
        emis_rate_source,
        emis_prod_rate,
        emis_duration,
        meth_spat_covs,
        emis_rep_delay,
        emis_rep_cost,
        next_emission,
    ):
        # Create a new instance without invoking __init__
        instance = cls.__new__(cls)
        # Restore the instance's attributes
        instance._source_ID = source_ID
        instance._repairable = repairable
        instance._persistent = persistent
        instance._active_duration = active_duration
        instance._inactive_duration = inactive_duration
        instance._generated_emissions = generated_emissions
        instance._emis_rate_source = emis_rate_source
        instance._emis_prod_rate = emis_prod_rate
        instance._emis_duration = emis_duration
        instance._meth_spat_covs = meth_spat_covs
        instance._emis_rep_delay = emis_rep_delay
        instance._emis_rep_cost = emis_rep_cost
        instance._next_emission = next_emission
        return instance

    def _update_prop_params(self, info, prop_params) -> None:
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

    def _set_source_properties(self, prop_params) -> None:
        self._emis_rate_source = prop_params[
            Infrastructure_Constants.Sources_File_Constants.EMIS_ERS
        ]
        self._emis_prod_rate = prop_params[Infrastructure_Constants.Sources_File_Constants.EMIS_EPR]
        self._emis_duration = prop_params[Infrastructure_Constants.Sources_File_Constants.EMIS_DUR]

        self._meth_spat_covs = prop_params["Method_Specific_Params"][
            Infrastructure_Constants.Sources_File_Constants.SPATIAL_PLACEHOLDER
        ]

        if self._repairable:
            # TODO look at processing for these values
            self._emis_rep_delay = prop_params[
                Infrastructure_Constants.Sources_File_Constants.REPAIR_DELAY
            ]["vals"]
            self._emis_rep_cost = prop_params[
                Infrastructure_Constants.Sources_File_Constants.REPAIR_COST
            ]["vals"]

    def _get_rate(self, emission_rate_source_dictionary: dict[str, EmissionsSource]):
        return emission_rate_source_dictionary[self._emis_rate_source].get_a_rate()

    def _get_repairable(self):
        return self._repairable

    def _get_rep_delay(self, repair_delay_dataframe: pd.DataFrame):
        if isinstance(self._emis_rep_delay, int):
            return self._emis_rep_delay
        elif isinstance(self._emis_rep_delay, list):
            return np.random.choice(self._emis_rep_delay)
        elif isinstance(self._emis_rep_delay, str):
            if self._emis_rep_delay in repair_delay_dataframe:
                return np.random.choice(repair_delay_dataframe[self._emis_rep_delay])
            else:
                print(self.INVALID_REPAIR_DELAY_COL_MSG.format(key=self._emis_rep_delay))
                sys.exit()
        else:
            print(self.INVALID_REPAIR_DELAY_ERR_MSG.format(delay=self._emis_rep_delay))
            sys.exit()

    def _get_rep_cost(self):
        return self._emis_rep_cost

    def _get_emis_duration(self):
        return self._emis_duration

    def _create_emission(
        self,
        leak_count,
        start_date,
        sim_start_date,
        emission_rate_source_dictionary: dict[str, EmissionsSource],
        repair_delay_dataframe: pd.DataFrame,
    ) -> Emission:
        if self._repairable:
            return FugitiveEmission(
                emission_n=leak_count,
                rate=self._get_rate(emission_rate_source_dictionary),
                start_date=start_date,
                simulation_sd=sim_start_date,
                repairable=self._get_repairable(),
                tech_spat_cov_probs=self._meth_spat_covs,
                repair_delay=self._get_rep_delay(repair_delay_dataframe),
                repair_cost=self._get_rep_cost(),
                nrd=self._get_emis_duration(),
            )
        else:
            print(Source.WIP_NON_FUG_EMIS_GENERATION_MSG)
            sys.exit()

    def generate_emissions(
        self,
        sim_start_date: date,
        sim_end_date: date,
        sim_number: int,
        emission_rate_source_dictionary: dict[str, EmissionsSource],
        repair_delay_dataframe: pd.DataFrame,
    ) -> dict[str, list[Emission]]:
        # Using a list as a FIFO queue for less overhead and to be able to pickle it
        emissions_fifo: list[Emission] = []

        # Initialize a counter to give all emissions for the source a unique "ID"
        leak_count: int = 0

        # TODO: re-do this logic to reflect the brainstorming session
        #  RNG the number of emissions to create and RNG the date for each emission

        # Generate Pre-Existing Emissions to exist at the start of simulation
        # The loop is working backwards in time, starting from 1 day before simulation start
        for day in range(1, self._emis_duration + 1):
            create_emis: int = np.random.binomial(1, self._emis_prod_rate)
            if create_emis:
                emis_start_date: date = sim_start_date - timedelta(days=day)
                emission: Emission = self._create_emission(
                    leak_count=leak_count,
                    start_date=emis_start_date,
                    sim_start_date=sim_start_date,
                    emission_rate_source_dictionary=emission_rate_source_dictionary,
                    repair_delay_dataframe=repair_delay_dataframe,
                )
                leak_count += 1
                emissions_fifo.append(emission)

        # Generate Emissions for the course of the simulation
        date_diff: timedelta = sim_end_date - sim_start_date
        sim_dur: int = date_diff.days

        for day in range(0, sim_dur):
            create_emis: int = np.random.binomial(1, self._emis_prod_rate)
            if create_emis:
                emis_start_date: date = sim_start_date + timedelta(days=day)
                emission: Emission = self._create_emission(
                    leak_count=leak_count,
                    start_date=emis_start_date,
                    sim_start_date=sim_start_date,
                    emission_rate_source_dictionary=emission_rate_source_dictionary,
                    repair_delay_dataframe=repair_delay_dataframe,
                )
                leak_count += 1
                emissions_fifo.append(emission)
        self._generated_emissions[sim_number] = emissions_fifo
        return {self._source_ID: emissions_fifo}

    def activate_emissions(self, date: date, sim_number: int) -> list[Emission]:
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

        activate_emissions: bool = False
        focus_emission: Emission = None

        if self._next_emission is None:
            if sim_emissions:
                focus_emission: Emission = sim_emissions.pop(0)
                activate_emissions = focus_emission.activate(date)
        else:
            focus_emission: Emission = self._next_emission
            activate_emissions = focus_emission.activate(date)

        while activate_emissions:
            newly_activated_emissions.append(focus_emission)
            if sim_emissions:
                focus_emission = sim_emissions.pop(0)
                activate_emissions = focus_emission.activate(date)
            else:
                activate_emissions = False
                focus_emission = None

        self._next_emission = focus_emission

        return newly_activated_emissions

    def set_pregen_emissions(self, src_emissions, sim_number) -> None:
        self._generated_emissions.clear()
        self._generated_emissions[sim_number] = src_emissions

    def get_id(self) -> str:
        return self._source_ID


# TODO : make an if/else function to determine emission sample from list or distribution
# TODO: make function that is called by above function to get single value for emission
