"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        queue
Purpose: Module for extending the python queue module

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
import queue
import itertools


class PriorityQueueWithFIFO(queue.PriorityQueue):
    def __init__(self):
        super().__init__()
        self.counter = itertools.count()

    def put(self, priority, item):
        # Add a tie-breaker using a secondary counter
        entry = (priority, next(self.counter), item)
        super().put(entry)
