"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        equipment_groups.py
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
from file_processing.output_processing.output_utils import (
    EmisInfo,
    TsEmisData,
)
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
)
from scheduling.schedule_dataclasses import TaggingInfo
from virtual_world.emissions import Emission
from constants.infrastructure_const import Infrastructure_Constants as IC
from virtual_world.component import Component
from constants.param_default_const import Common_Params as cp


class Equipment_Group:
    def __init__(self, id, infrastructure_inputs, prop_params, info) -> None:
        self._id: str = id
        self._meth_survey_times = None
        self._meth_survey_costs = None
        self._component: list[Component] = []
        self._update_prop_params(info, prop_params)
        self._set_method_specific_params(prop_params)
        self._create_equipment(
            infrastructure_inputs=infrastructure_inputs,
            prop_params=prop_params,
            info=info,
        )

    def __reduce__(self):
        args = (
            self._id,
            self._meth_survey_times,
            self._meth_survey_costs,
            self._component,
        )
        return (self.__class__._reconstruct, args)

    @classmethod
    def _reconstruct(cls, id, meth_survey_times, meth_survey_costs, component):
        instance = cls.__new__(cls)
        instance._id = id
        instance._meth_survey_times = meth_survey_times
        instance._meth_survey_costs = meth_survey_costs
        instance._component = component
        return instance

    def _update_prop_params(self, info: dict, prop_params: dict) -> None:
        meth_specific_params: dict = prop_params.pop(cp.METH_SPECIFIC)

        for param in meth_specific_params.keys():
            for method in meth_specific_params[param].keys():
                eqg_val = info.get(method + param, None)
                if eqg_val is not None:
                    meth_specific_params[param][method] = eqg_val

        for param in prop_params.keys():
            eqg_val = info.get(param, None)
            if eqg_val is not None:
                prop_params[param] = eqg_val

        prop_params[cp.METH_SPECIFIC] = meth_specific_params

    def _create_equipment(self, infrastructure_inputs, prop_params, info) -> None:
        tot_equip = info.sum()
        nonrep_epr = prop_params[IC.Equipment_Group_File_Constants.NON_REP_EMIS_EPR]
        rep_epr = prop_params[IC.Equipment_Group_File_Constants.REP_EMIS_EPR]
        if nonrep_epr is not None and nonrep_epr > 0:
            prop_params[IC.Equipment_Group_File_Constants.NON_REP_EMIS_EPR] = nonrep_epr / tot_equip
        if rep_epr is not None and rep_epr > 0:
            prop_params[IC.Equipment_Group_File_Constants.REP_EMIS_EPR] = rep_epr / tot_equip
        for col, val in info.items():
            for count in range(0, val):
                self._component.append(Component(col, count, infrastructure_inputs, prop_params))

    def _set_method_specific_params(self, prop_params):
        self._meth_survey_times = prop_params[cp.METH_SPECIFIC].pop(
            IC.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER
        )
        self._meth_survey_costs = prop_params[cp.METH_SPECIFIC].pop(
            IC.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER
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
        for eqmt in self._component:
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
        for component in self._component:
            new_emissions += component.activate_emissions(date, sim_number)
        return new_emissions

    def update_emissions_state(self, emis_rep_info: EmisInfo, emis_data: TsEmisData) -> None:
        for comp in self._component:
            comp.update_emissions_state(emis_rep_info, emis_data)

    def tag_emissions_at_component(self, component: str, tagging_info: TaggingInfo) -> None:
        target_comp: Component | None = next(
            (comp for comp in self._component if comp.get_id() == component),
            None,
        )
        target_comp.tag_emissions(tagging_info)

    def get_detectable_emissions(self, method_name: str) -> dict[str, list[Emission]]:
        detectable_emissions: dict[str, Emission] = {}
        for equip in self._component:
            detectable_emissions[equip.get_id()] = equip.get_detectable_emissions(method_name)

        return detectable_emissions

    def set_pregen_emissions(self, eqg_emissions, sim_number) -> None:
        for component in self._component:
            component.set_pregen_emissions(eqg_emissions[component.get_id()], sim_number)

    def get_survey_time(self, method_name) -> float:
        survey_time: float = self._meth_survey_times[method_name]
        return survey_time

    def report_func(self):
        # TODO: some reporting agregate function?
        return

    def get_id(self) -> str:
        return self._id

    def gen_emis_data(self, emis_df: pd.DataFrame, site_id: str, row_index: int, end_date: date):
        upd_row_index = row_index
        for equip in self._component:
            upd_row_index = equip.gen_emis_data(emis_df, site_id, self._id, upd_row_index, end_date)
        return upd_row_index

    def get_survey_cost(self, method_name) -> float:
        return self._meth_survey_costs[method_name]

    def setup(self, methods: list[str]):
        for component in self._component:
            component.set_emis_sum_dtypes(methods)

    @property
    def component(self):
        return self._component
