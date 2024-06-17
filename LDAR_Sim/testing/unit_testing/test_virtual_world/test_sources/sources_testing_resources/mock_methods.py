"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        mock_methods.py
Purpose: Contains mock methods for testing sources.

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


def mock_source_initialization_for_intermittent_source(
    self,
    repairable: bool = True,
    persistent: bool = False,
    emis_rate_source: str = "test",
    emis_duration: int = 365,
    **kwargs,
):
    if kwargs:
        self._active_duration = kwargs["active_duration"]
        self._inactive_duration = kwargs["inactive_duration"]
    self._repairable = repairable
    self._persistent = persistent
    self._emis_rate_source = emis_rate_source
    self._emis_duration = emis_duration
    self._meth_spat_covs = {}
    self._emis_rep_delay = 0
    self._emis_rep_cost = 0
