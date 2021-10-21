# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.args
# Purpose:     Handle program input arguments
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
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

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter


def files_from_args():
    '''
    Look for parameter files supplied as arguments - if parameter files are supplied as
    arguments, proceed to parse and type check input parameter type with the input manager.
    The program will will also accept flagged input directory , (-P or --in_dir)
    '''
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    # ---Declare input arguments---
    parser.add_argument(
        'in_files', type=str, nargs='*',
        help='Input files, seperate with space, can be absolute path or relative to' +
        'root directory (LDAR_Sim). All files should have yaml, yml, or json extensions \n' +
        'ie. python ldar_sim_main.py ./file1.json c:/path/to/file/file2.json')
    parser.add_argument(
        "-P", "--in_dir",
        help='Input Directory, folder containing input files, will input all files within' +
        'folder that have yaml, yml or json extensions \n' +
        'ie. python ldar_sim_main.py --in_dir ./folder_with_infiles')
    args = parser.parse_args()

    if args.in_dir is not None:
        # if an input directory is specified, get all files within that are in the directory
        # Get all yaml or json files in specified folder
        parameter_filenames = [
            "{}/{}".format(args.in_dir, f) for f in os.listdir(args.in_dir)
            if ".yaml" in f or ".yml" in f or ".json" in f]
    else:
        parameter_filenames = args.in_files

    if len(parameter_filenames) < 1:
        print('Please provide at least one input argument')
        sys.exit ()
        
    return parameter_filenames
