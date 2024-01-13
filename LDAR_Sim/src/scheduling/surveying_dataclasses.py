"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        schedule_dataclasses
Purpose: Module for holding the different dataclasses used for surveying.
Specifically split out to prevent circular references. 

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
from dataclasses import dataclass

from virtual_world.sites import Site


@dataclass
class DetectionRecord:
    site_id: str
    site: Site
    rate_detected: float
