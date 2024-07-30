"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        remove_generator.py
Purpose: Contains function for removing all the non-preseed generator files

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

import os


def remove_non_preseed_files(directory):
    """
    Remove all files in the given directory except for 'preseed.p'.

    :param directory: Path to the directory to clean up.
    """
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) and "preseed" not in filename:
                os.remove(file_path)
                print(f"Removed: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
