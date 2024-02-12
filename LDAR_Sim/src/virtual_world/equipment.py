"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        equipment
Purpose: The equipment module.

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

from copy import deepcopy
from datetime import date
import re

import pandas as pd
from file_processing.output_processing.output_utils import (
    EMIS_DATA_COLS,
    EmisRepairInfo,
    TsEmisData,
)
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
)
from scheduling.schedule_dataclasses import TaggingInfo

from virtual_world.emissions import Emission
from virtual_world.fugitive_emission import FugitiveEmission
from virtual_world.infrastructure_const import Infrastructure_Constants

from virtual_world.sources import Source


SOURCE_CREATION_ERROR_MESSAGE = (
    "Invalid LDAR-Sim infrastructure inputs: Failure to read in sources infrastructure input"
)


class Equipment:
    def __init__(self, equip_type, equip_id, infrastructure_inputs, prop_params) -> None:
        STR_FILTER = r"_equipment"
        pattern: re.Pattern[str] = re.compile(re.escape(STR_FILTER), re.IGNORECASE)
        self._equip_type: str = re.sub(pattern, "", equip_type)
        self._equipment_ID: str = self._equip_type + "_" + str(equip_id)
        self._create_sources(infrastructure_inputs=infrastructure_inputs, prop_params=prop_params)
        self._active_emissions: list[Emission] = []
        self._inactive_emissions: list[Emission] = []

    def _create_sources(self, infrastructure_inputs, prop_params) -> None:
        self._sources: list[Source] = []
        if self._equip_type != "Placeholder" and "sources" in infrastructure_inputs:
            sources_info = infrastructure_inputs["sources"]
            sources = sources_info.loc[
                sources_info[Infrastructure_Constants.Sources_File_Constants.EQUIPMENT]
                == self._equip_type
            ]
            for source in sources:
                src_prop_params = deepcopy(prop_params)
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

    def generate_emissions(
        self,
        sim_start_date,
        sim_end_date,
        sim_number,
        emission_rate_source_dictionary: dict[str, EmissionsSource],
        repair_delay_dataframe: pd.DataFrame,
    ) -> dict:
        equip_emissions = {}
        for src in self._sources:
            equip_emissions.update(
                src.generate_emissions(
                    sim_start_date,
                    sim_end_date,
                    sim_number,
                    emission_rate_source_dictionary,
                    repair_delay_dataframe,
                )
            )

        return {self._equipment_ID: equip_emissions}

    def activate_emissions(self, date: date, sim_number: int) -> int:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (date): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        new_emissions_count: int = 0
        for source in self._sources:
            new_emissions: list[Emission] = source.activate_emissions(date, sim_number)
            self._active_emissions.extend(new_emissions)
            new_emissions_count += len(new_emissions)
        return new_emissions_count

    def update_emissions_state(self, emis_rep_info: EmisRepairInfo) -> TsEmisData:
        updated_active_emissions: list[Emission] = []
        emis_data: TsEmisData = TsEmisData()
        for emission in self._active_emissions:
            if emission.update(emis_rep_info):
                updated_active_emissions.append(emission)
                emis_data.daily_emis += emission.get_daily_emis()
            else:
                self._inactive_emissions.append(emission)
        self._active_emissions = updated_active_emissions
        emis_data.active_leaks += len(self._active_emissions)
        return emis_data

    def tag_emissions(self, tagging_info: TaggingInfo) -> None:
        for emission in self._active_emissions:
            if isinstance(emission, FugitiveEmission):
                emission.tag_leak(
                    measured_rate=tagging_info.measured_rate,
                    cur_date=tagging_info.curr_date,
                    t_since_ldar=tagging_info.t_since_LDAR,
                    company=tagging_info.company,
                    crew_id=tagging_info.crew,
                    tagging_rep_delay=tagging_info.report_delay,
                )
                emission.update_detection_records(
                    company=tagging_info.company, detect_date=tagging_info.curr_date
                )

    def get_detectable_emissions(self, method_name: str) -> Emission:
        detectable_emissions: list[Emission] = []
        for emis in self._active_emissions:
            if emis.check_spatial_cov(method_name):
                detectable_emissions.append(emis)

        return detectable_emissions

    def set_pregen_emissions(self, equipment_emissions, sim_number) -> None:
        for src in self._sources:
            src.set_pregen_emissions(equipment_emissions[src.get_id()], sim_number)

    def get_id(self) -> str:
        return self._equipment_ID

    def get_emis_data(self) -> pd.DataFrame:
        emis_data_active: pd.DataFrame = pd.DataFrame(
            [emission.get_summary_dict() for emission in self._active_emissions]
        )

        emis_data_inactive: pd.DataFrame = pd.DataFrame(
            [emission.get_summary_dict() for emission in self._inactive_emissions]
        )

        # Handle empty dataframe cases
        if emis_data_active.empty and emis_data_inactive.empty:
            columns = EMIS_DATA_COLS
            return pd.DataFrame(columns=columns)
        elif emis_data_inactive.empty:
            emis_data = emis_data_active
        elif emis_data_active.empty:
            emis_data = emis_data_inactive
        else:
            # Exclude empty or all-NA columns from both DataFrames
            # Specifically the spatial coverage column that may be empty for emis_data_active
            emis_data_active = emis_data_active.dropna(axis=1, how="all")
            emis_data_inactive = emis_data_inactive.dropna(axis=1, how="all")
            emis_data = pd.concat([emis_data_active, emis_data_inactive], ignore_index=True)

        emis_data["Equipment"] = self._equipment_ID

        return emis_data
