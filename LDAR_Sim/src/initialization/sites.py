# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.sites
# Purpose:     Pregenerate sites and regenerate sites
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

import copy
from datetime import datetime
import math


import pandas as pd
from initialization.equipment_groups import Equipment_Group

from initialization.infrastructure_const import (
    Infrastructure_Constants,
)

PLACEHOLDER_EQUIPMENT = "Placeholder_Equipment"
PLACEHOLDER_EQUIPMENT_COUNT = 10


class Site:
    def __init__(
        self,
        id: str,
        lat: float,
        long: float,
        equipment_groups: list,
        propagating_params: dict,
        infrastructure_inputs: dict,
        site_type: str = None,
    ) -> None:
        self._site_ID: str = id
        self._lat: float = lat
        self._long: float = long

        self._site_type: str = site_type
        self._survey_frequencies: dict = propagating_params["Method_Specific_Params"].pop(
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER
        )
        self.create_equipment_groups(equipment_groups, infrastructure_inputs, propagating_params)

    def create_equipment_groups(
        self, equipment_groups, infrastructure_inputs, propagating_params
    ) -> None:
        self._equipment_groups: list[Equipment_Group] = []
        if isinstance(equipment_groups, list) and len(equipment_groups) > 0:
            equip_groups_in: pd.DataFrame = infrastructure_inputs["equipment_groups"]
            for equipment_group in equipment_groups:
                site_equipment_group = equip_groups_in.loc[
                    equip_groups_in[
                        Infrastructure_Constants.Equipment_Group_File_Constants.EQUIPMENT_GROUP
                    ]
                    == equipment_group
                ].iloc[0]
                prop_params = copy.deepcopy(propagating_params)
                self._equipment_groups.append(
                    Equipment_Group(
                        site_equipment_group[
                            Infrastructure_Constants.Equipment_Group_File_Constants.EQUIPMENT_GROUP
                        ],
                        infrastructure_inputs,
                        prop_params,
                        site_equipment_group,
                    )
                )
        elif isinstance(equipment_groups, (int, float)):
            for i in range(0, equipment_groups):
                equip_group_info = pd.Series(
                    {
                        PLACEHOLDER_EQUIPMENT: math.ceil(
                            PLACEHOLDER_EQUIPMENT_COUNT / equipment_groups
                        )
                    }
                )
                prop_params = copy.deepcopy(propagating_params)
                self._equipment_groups.append(
                    Equipment_Group(i, infrastructure_inputs, prop_params, equip_group_info)
                )
        else:
            equip_group_info = pd.Series(
                {PLACEHOLDER_EQUIPMENT: math.ceil(PLACEHOLDER_EQUIPMENT_COUNT)}
            )
            prop_params = copy.deepcopy(propagating_params)
            self._equipment_groups.append(
                Equipment_Group(i, infrastructure_inputs, prop_params, equip_group_info)
            )

    def generate_emissions(self, sim_start_date, sim_end_date, sim_number) -> dict:
        site_emissions: dict = {}
        for eqg in self._equipment_groups:
            eqg: Equipment_Group
            site_emissions.update(eqg.generate_emissions(sim_start_date, sim_end_date, sim_number))

        return {self._site_ID: site_emissions}

    def activate_emissions(self, date: datetime, sim_number: int) -> None:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the equipment at which they occur.

        Args:
            date (datetime): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        for eqg in self._equipment_groups:
            eqg.activate_emissions(date, sim_number)

    def set_pregen_emissions(self, site_emissions, sim_number) -> None:
        for eqg in self._equipment_groups:
            eqg.set_pregen_emissions(site_emissions[eqg.get_id()], sim_number)

    def get_required_surveys(self, method_name) -> int:
        return self._survey_frequencies[method_name]

    def get_method_survey_time(self, method_name) -> float:
        survey_time: float = 0
        for eqg in self._equipment_groups:
            survey_time += eqg.get_survey_time(method_name=method_name)
        return survey_time

    def get_id(self) -> str:
        return self._site_ID

    def _get_days_since_last_survey(self, method_name: str, current_date: datetime) -> int:
        return (self._last_survey_dates[method_name] - current_date).days

    def _get_current_yearly_surveys(self, method_name: str) -> int:
        return self._surveys_this_year[method_name]
