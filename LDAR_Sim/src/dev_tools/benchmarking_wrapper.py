# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        benchmarking_wrapper.py
# Purpose:     Wrapper to run ldar-sim with benchmarking


# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.
# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.

# ------------------------------------------------------------------------------

import cProfile
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ldar_sim_run import run_ldar_sim  # noqa: E402, F401


if __name__ == "__main__":
    cProfile.run(
        "run_ldar_sim()",
        "../Benchmarking/benchmark1_results",
        "cumulative",
    )
