"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        intermittent_repairable_emission.py
Purpose: Defines the IntermittentRepairableEmission class.

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

from virtual_world.emission_types.intermittency_mixin import IntermittencyMixin
from virtual_world.emission_types.repairable_emission import RepairableEmission


class IntermittentRepairableEmission(IntermittencyMixin, RepairableEmission):
    def __init__(
        self,
        emission_number: int,
        emission_rate: float,
        start_date: date,
        simulation_start_date: date,
        repairable: bool,
        tech_spatial_coverage_probabilities: dict[str, float],
        repair_delay: int,
        repair_cost: float,
        duration: int,
        active_duration: int,
        inactive_duration: int,
    ):
        super().__init__(
            active_duration,
            inactive_duration,
            emission_number,
            emission_rate,
            start_date,
            simulation_start_date,
            repairable,
            tech_spatial_coverage_probabilities,
            repair_delay,
            repair_cost,
            duration,
        )

    def __reduce__(self):
        return self._reconstruct_intermittent_repairable_emission, (self.__dict__,)

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def _reconstruct_intermittent_repairable_emission(cls, state):
        instance = cls.__new__(cls)
        instance.__setstate__(state)
        return instance
