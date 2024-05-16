# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        benchmarking_parser.py
# Purpose:     Parser for benchmarking results
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
# ------------------------------------------------------------------------------
import pstats
import sys
import os

benchmark_res_path = "Benchmarking"

file_list = os.listdir(benchmark_res_path)
FILE_NAME = "benchmark1_results"


for filename in file_list:
    if filename == FILE_NAME:
        with open(benchmark_res_path + "/" + filename + ".txt", "w") as file:
            old_stdout = sys.stdout
            sys.stdout = file
            pstats.Stats(benchmark_res_path + "/" + filename).strip_dirs().sort_stats(
                "cumulative"
            ).print_stats()
            sys.stdout = old_stdout
