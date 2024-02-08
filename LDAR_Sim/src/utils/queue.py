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

from multiprocessing import Queue
import itertools


class PriorityQueueWithFIFO:
    def __init__(self, num_priorities=3):
        self.queues = [Queue() for _ in range(num_priorities)]
        self.counters = [itertools.count() for _ in range(num_priorities)]

    def put(self, priority, item):
        entry = (next(self.counters[priority]), item)
        self.queues[priority].put(entry)

    def get(self):
        for queue in self.queues:
            if not queue.empty():
                _, item = queue.get()
                return item
        raise IndexError("Queue is empty")

    def empty(self):
        return all(queue.empty() for queue in self.queues)


class PriorityQueue:
    def __init__(self, num_priorities=3):
        self.queues = [Queue() for _ in range(num_priorities)]

    def put(self, priority, item):
        self.queues[priority].put(item)

    def get(self):
        for queue in self.queues:
            if not queue.empty():
                return queue.get()
        raise IndexError("Queue is empty")

    def empty(self):
        return all(queue.empty() for queue in self.queues)
