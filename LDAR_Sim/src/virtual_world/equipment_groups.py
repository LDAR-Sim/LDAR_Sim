"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        equipment_groups
Purpose: The equipment group module.

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

import pandas as pd
from file_processing.output_processing.output_utils import EMIS_SUMMARY_DATA_COLS, TsEmisData
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
)
from scheduling.schedule_dataclasses import TaggingInfo
from virtual_world.emissions import Emission
from virtual_world.infrastructure_const import Infrastructure_Constants
from virtual_world.equipment import Equipment


class Equipment_Group:
    def __init__(self, id, infrastructure_inputs, prop_params, info) -> None:
        self._id: str = id
        self._update_prop_params(info, prop_params)
        self._set_method_specific_params(prop_params)
        self._create_equipment(
            infrastructure_inputs=infrastructure_inputs,
            prop_params=prop_params,
            info=info,
        )

    def _update_prop_params(self, info: dict, prop_params: dict) -> None:
        meth_specific_params: dict = prop_params.pop("Method_Specific_Params")

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

    def _create_equipment(self, infrastructure_inputs, prop_params, info) -> None:
        self._equipment: list[Equipment] = []
        for col, val in info.items():
            if "equipment" in col.lower():
                for count in range(0, val):
                    self._equipment.append(
                        Equipment(col, count, infrastructure_inputs, prop_params)
                    )

    def _set_method_specific_params(self, prop_params):
        self._meth_survey_times = prop_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER
        )
        self._meth_survey_costs = prop_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER
        )

    def generate_emissions(
        self,
        sim_start_date,
        sim_end_date,
        sim_number,
        emission_rate_source_dictionary: dict[str, EmissionsSource],
        repair_delay_dataframe: pd.DataFrame,
    ) -> dict:
        eqg_emissions = {}
        for eqmt in self._equipment:
            eqg_emissions.update(
                eqmt.generate_emissions(
                    sim_start_date,
                    sim_end_date,
                    sim_number,
                    emission_rate_source_dictionary,
                    repair_delay_dataframe,
                )
            )

        return {self._id: eqg_emissions}

    def activate_emissions(self, date: date, sim_number: int) -> int:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (date): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        new_emissions: int = 0
        for equipment in self._equipment:
            new_emissions += equipment.activate_emissions(date, sim_number)
        return new_emissions

    def update_emissions_state(self) -> TsEmisData:
        emis_data = TsEmisData()
        for equip in self._equipment:
            emis_data += equip.update_emissions_state()
        return emis_data

    def tag_emissions_at_equipment(self, equipment: str, tagging_info: TaggingInfo) -> None:
        target_equip: Equipment | None = next(
            (equip for equip in self._equipment if equip.get_id() == equipment),
            None,
        )
        target_equip.tag_emissions(tagging_info)

    def get_detectable_emissions(self, method_name: str) -> dict[str, list[Emission]]:
        detectable_emissions: dict[str, Emission] = {}
        for equip in self._equipment:
            detectable_emissions[equip.get_id()] = equip.get_detectable_emissions(method_name)

        return detectable_emissions

    def set_pregen_emissions(self, eqg_emissions, sim_number) -> None:
        for equipment in self._equipment:
            equipment.set_pregen_emissions(eqg_emissions[equipment.get_id()], sim_number)

    def get_survey_time(self, method_name) -> float:
        survey_time: float = self._meth_survey_times[method_name]
        return survey_time

    def report_func(self):
        # TODO: some reporting agregate function?
        return

    def get_id(self) -> str:
        return self._id

    def get_emis_data(self) -> pd.DataFrame:
        equip_emis_dataframes: list[pd.DataFrame] = [
            equip.get_emis_data() for equip in self._equipment
        ]
        equip_emis_dataframes = [df for df in equip_emis_dataframes if not df.empty]

        if equip_emis_dataframes:
            emis_data: pd.DataFrame = pd.concat(equip_emis_dataframes)
        else:
            emis_data: pd.DataFrame = pd.DataFrame(columns=EMIS_SUMMARY_DATA_COLS)
        emis_data["Equipment Group"] = self._id
        return emis_data

    def get_survey_cost(self, method_name) -> float:
        return self._meth_survey_costs[method_name]