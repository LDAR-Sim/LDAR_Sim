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
import logging
import re
import sys
from typing import Literal

import numpy as np
import pandas as pd
from constants.error_messages import Initialization_Messages as im
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
)
from virtual_world import emission_types
from constants.infrastructure_const import (
    Infrastructure_Constants as IC,
)
from constants.general_const import Emission_Constants as ec
import constants.param_default_const as pdc


class Source:

    def __init__(self, id: str, info, prop_params) -> None:
        self._source_ID: str = id
        self._set_source_only_properties(info=info)
        self._multi_emissions: bool = None
        self._generated_emissions: dict[int, list[emission_types.Emission]] = {}
        self._emis_rate_source: EmissionsSource = None
        self._emis_prod_rate: float = None
        self._emis_duration: int = None
        self._meth_spat_covs: dict[str, float] = None
        self._emis_rep_delay: int = None
        self._emis_rep_cost: float = None
        self._prefix: Literal["repairable", "non_repairable"] = None
        self._set_prefix()
        self._update_prop_params(info=info, prop_params=prop_params)
        self._set_propagating_source_properties(prop_params=prop_params)
        self._next_emission: emission_types.Emission = None

    def __reduce__(self):
        args = (
            self._source_ID,
            self._repairable,
            self._persistent,
            self._active_duration,
            self._inactive_duration,
            self._multi_emissions,
            self._generated_emissions,
            self._emis_rate_source,
            self._emis_prod_rate,
            self._emis_duration,
            self._meth_spat_covs,
            self._emis_rep_delay,
            self._emis_rep_cost,
            self._next_emission,
            self._prefix,
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
        multi_emissions,
        generated_emissions,
        emis_rate_source,
        emis_prod_rate,
        emis_duration,
        meth_spat_covs,
        emis_rep_delay,
        emis_rep_cost,
        next_emission,
        prefix,
    ):
        # Create a new instance without invoking __init__
        instance = cls.__new__(cls)
        # Restore the instance's attributes
        instance._source_ID = source_ID
        instance._repairable = repairable
        instance._persistent = persistent
        instance._active_duration = active_duration
        instance._inactive_duration = inactive_duration
        instance._multi_emissions = multi_emissions
        instance._generated_emissions = generated_emissions
        instance._emis_rate_source = emis_rate_source
        instance._emis_prod_rate = emis_prod_rate
        instance._emis_duration = emis_duration
        instance._meth_spat_covs = meth_spat_covs
        instance._emis_rep_delay = emis_rep_delay
        instance._emis_rep_cost = emis_rep_cost
        instance._next_emission = next_emission
        instance._prefix = prefix
        return instance

    def _set_source_only_properties(self, info) -> None:
        try:
            self._repairable: bool = info[IC.Sources_File_Constants.REPAIRABLE]
            self._persistent: bool = info[IC.Sources_File_Constants.PERSISTENT]
            self._active_duration: int = info[IC.Sources_File_Constants.ACTIVE_DUR]
            self._inactive_duration: int = info[IC.Sources_File_Constants.INACTIVE_DUR]
        except KeyError as e:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(im.SOURCE_INFO_MISSING_KEY_MSG.format(key=e))
            sys.exit()

    def _set_prefix(self) -> None:
        prefix: Literal["repairable", "non_repairable"] = (
            ec.REP_PREFIX if self._repairable else ec.NON_REP_PREFIX
        )
        self._prefix = prefix

    def _update_prop_params(self, info, prop_params) -> None:
        meth_specific_params = prop_params.pop(pdc.Common_Params.METH_SPECIFIC)

        for param in meth_specific_params.keys():
            for method in meth_specific_params[param].keys():
                src_val = info.get(method + param, None)
                if src_val is not None:
                    meth_specific_params[param][method] = src_val

        prop_params_keys = list(prop_params.keys())
        for param in prop_params_keys:
            if self._prefix in param:
                src_param = re.sub(self._prefix, "", param)
                src_val = info.get(src_param, None)
                if src_val is not None:
                    prop_params[src_param] = src_val
                else:
                    prop_val = prop_params[param]
                    prop_params[src_param] = prop_val

        prop_params[pdc.Common_Params.METH_SPECIFIC] = meth_specific_params

    def _set_propagating_source_properties(self, prop_params) -> None:
        if prop_params[IC.Sources_File_Constants.EMIS_ERS] is None:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                im.POTENTIAL_SOURCE_CREATION_ERROR_MESSAGE.format(
                    rep=self._prefix, const=IC.Sources_File_Constants.EMIS_ERS
                )
            )
            sys.exit()
        elif prop_params[IC.Sources_File_Constants.EMIS_EPR] is None:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                im.POTENTIAL_SOURCE_CREATION_ERROR_MESSAGE.format(
                    rep=self._prefix, const=IC.Sources_File_Constants.EMIS_EPR
                )
            )
            sys.exit()
        self._emis_rate_source = prop_params[IC.Sources_File_Constants.EMIS_ERS]
        self._emis_prod_rate = prop_params[IC.Sources_File_Constants.EMIS_EPR]
        self._emis_duration = prop_params[IC.Sources_File_Constants.EMIS_DUR]
        self._multi_emissions = prop_params[IC.Sources_File_Constants.MULTI_EMISSIONS]

        self._meth_spat_covs = prop_params[pdc.Common_Params.METH_SPECIFIC][
            IC.Sources_File_Constants.SPATIAL_PLACEHOLDER
        ]

        if self._repairable:
            # TODO look at processing for these values
            self._emis_rep_delay = prop_params[IC.Sources_File_Constants.REPAIR_DELAY][
                pdc.Common_Params.VAL
            ]
            self._emis_rep_cost = prop_params[IC.Sources_File_Constants.REPAIR_COST][
                pdc.Common_Params.VAL
            ]

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
                logger: logging.Logger = logging.getLogger(__name__)
                logger.error(im.INVALID_REPAIR_DELAY_COL_MSG.format(key=self._emis_rep_delay))
                sys.exit()
        else:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(im.INVALID_REPAIR_DELAY_ERR_MSG.format(delay=self._emis_rep_delay))
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
    ) -> emission_types.Emission:
        if self._repairable:
            if self._persistent:
                return emission_types.RepairableEmission(
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
                return emission_types.IntermittentRepairableEmission(
                    emission_number=leak_count,
                    emission_rate=self._get_rate(emission_rate_source_dictionary),
                    start_date=start_date,
                    simulation_start_date=sim_start_date,
                    repairable=self._get_repairable(),
                    tech_spatial_coverage_probabilities=self._meth_spat_covs,
                    repair_delay=self._get_rep_delay(repair_delay_dataframe),
                    repair_cost=self._get_rep_cost(),
                    duration=self._get_emis_duration(),
                    active_duration=self._active_duration,
                    inactive_duration=self._inactive_duration,
                )
        else:
            if self._persistent:
                return emission_types.NonRepairableEmission(
                    emission_n=leak_count,
                    rate=self._get_rate(emission_rate_source_dictionary),
                    start_date=start_date,
                    simulation_sd=sim_start_date,
                    repairable=self._get_repairable(),
                    tech_spat_cov_probs=self._meth_spat_covs,
                    duration=self._get_emis_duration(),
                )
            else:
                return emission_types.IntermittentNonRepairableEmission(
                    emission_number=leak_count,
                    emission_rate=self._get_rate(emission_rate_source_dictionary),
                    start_date=start_date,
                    simulation_start_date=sim_start_date,
                    repairable=self._get_repairable(),
                    tech_spatial_coverage_probabilities=self._meth_spat_covs,
                    duration=self._get_emis_duration(),
                    active_duration=self._active_duration,
                    inactive_duration=self._inactive_duration,
                )

    def generate_emissions(
        self,
        sim_start_date: date,
        sim_end_date: date,
        sim_number: int,
        emission_rate_source_dictionary: dict[str, EmissionsSource],
        repair_delay_dataframe: pd.DataFrame,
    ) -> dict[str, list[emission_types.Emission]]:
        # Using a list as a FIFO queue for less overhead and to be able to pickle it
        emissions_fifo: list[emission_types.Emission] = []

        # Initialize a counter to give all emissions for the source a unique "ID"
        leak_count: int = 0
        # Pre-calculate date ranges
        pre_existing_dates = pd.date_range(
            start=sim_start_date - timedelta(days=self._emis_duration),
            periods=self._emis_duration,
            freq="D",
        )

        # Vectorize random number generation
        pre_existing_emissions = np.random.binomial(1, self._emis_prod_rate, self._emis_duration)

        # Filter dates where emissions should be created
        filtered_emission_dates = pre_existing_dates[pre_existing_emissions == 1]

        #  RNG the number of emissions to create and RNG the date for each emission

        # Generate Pre-Existing Emissions to exist at the start of simulation
        # The loop is working backwards in time, starting from 1 day before simulation start

        # This first loop is to generate emissions that are already active
        # at the start of the simulation. If only one emission is allowed
        # for the given source, the loop will break once the first is made,
        # since no other emissions should exist
        last_emis_day: date = sim_start_date
        for day in filtered_emission_dates:
            emis_start_date: date = day.date()
            emission: emission_types.Emission = self._create_emission(
                leak_count=leak_count,
                start_date=emis_start_date,
                sim_start_date=sim_start_date,
                emission_rate_source_dictionary=emission_rate_source_dictionary,
                repair_delay_dataframe=repair_delay_dataframe,
            )
            leak_count += 1
            emissions_fifo.append(emission)
            if not self._multi_emissions:
                last_emis_day = emis_start_date + timedelta(days=int(self._emis_duration))
                # If only one emission is allowed, break the loop
                break

        # Generate Emissions for the course of the simulation
        date_diff: timedelta = sim_end_date - sim_start_date
        sim_dur: int = date_diff.days + 1  # +1 to include the end date
        # Precalculate date
        simulation_dates = pd.date_range(start=sim_start_date, periods=sim_dur, freq="D")
        # Vectorize random number generation
        simulation_emissions = np.random.binomial(1, self._emis_prod_rate, sim_dur)

        # Filter dates where emissions should be created
        emission_dates = simulation_dates[simulation_emissions == 1]

        for day in emission_dates:
            emis_start_date: date = day.date()
            # Skip emission creation if it's too soon after the last one
            if not self._multi_emissions and emis_start_date <= last_emis_day:
                continue

            emission: emission_types.Emission = self._create_emission(
                leak_count=leak_count,
                start_date=emis_start_date,
                sim_start_date=sim_start_date,
                emission_rate_source_dictionary=emission_rate_source_dictionary,
                repair_delay_dataframe=repair_delay_dataframe,
            )
            leak_count += 1
            emissions_fifo.append(emission)
            if not self._multi_emissions:
                # if only a single emission can be made,
                # update the last_emis_day based on the new emission
                last_emis_day = emis_start_date + timedelta(days=int(self._emis_duration))
        emissions_fifo.reverse()
        self._generated_emissions[sim_number] = emissions_fifo
        return {self._source_ID: emissions_fifo}

    def activate_emissions(self, date: date, sim_number: int) -> list[emission_types.Emission]:
        """Activate any emissions produced by the source that are due to begin on the current date
        for the given simulation and return them in a list.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.

        Returns:
            list[Emission]: The list of emissions that are newly active on the current date
        """
        newly_activated_emissions: list[emission_types.Emission] = []
        sim_emissions: list[emission_types.Emission] = self._generated_emissions[sim_number]

        if self._next_emission is None and sim_emissions:
            focus_emission: emission_types.Emission = sim_emissions.pop()
        else:
            focus_emission: emission_types.Emission = self._next_emission

        while focus_emission and focus_emission.activate(date):
            newly_activated_emissions.append(focus_emission)
            if sim_emissions:
                focus_emission = sim_emissions.pop()
            else:
                focus_emission = None

        self._next_emission = focus_emission

        return newly_activated_emissions

    def set_pregen_emissions(self, src_emissions, sim_number) -> None:
        self._generated_emissions.clear()
        self._generated_emissions[sim_number] = src_emissions

    def get_id(self) -> str:
        return self._source_ID
