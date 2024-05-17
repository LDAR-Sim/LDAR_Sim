# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        profiling_tools.py
# Purpose:     Methods to wrap LDAR-Sim methods in order to profile their runtime


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

from contextlib import contextmanager
import cProfile
import pstats


# HOW TO USE:
# 1. Import the profile_function method from this file
#    into the file with the method you want to profile
# 2. Wrap the method you want to profile in a with statement
#    using the profile_function method
#    Example: with profile_function(<filename>):
#                <method to profile>
#    The easiest way to do this is replace calls to the method
#    with calls to a wrapper method that calls the method
# 3. Run LDAR-SIm as you normally would
# 4. The profile results will be saved to the Benchmarking folder


@contextmanager
def profile_function(filename: str = "Benchmarking/test_results"):
    pr = cProfile.Profile()
    pr.enable()
    yield
    pr.disable()
    with open("../Benchmarking/" + filename + ".txt", "w") as f:
        ps = pstats.Stats(pr, stream=f)
        ps.strip_dirs().sort_stats("cumulative").print_stats()
