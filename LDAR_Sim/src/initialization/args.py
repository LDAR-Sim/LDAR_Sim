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

from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
import sys
import os


def get_abs_path(path, ref_folder=None):
    """ Get the absolute path of a file from the reference folder
        If none is specified, use the current working directory

    Args:
        path (string): relative (or absolute) path to a file
        ref_folder (Path, optional): reference folder. Defaults to None.
    """
    def sel_parent(p_folder):
        return p_folder.parent
    if ref_folder is None:
        ref_folder = Path(os.getcwd())
    n_pars = len(path) - len(path.lstrip('.'))
    if n_pars > 0:
        n_pars -= 1
        mod_rel_path = path[n_pars:]
        out_dir = ref_folder
        for par in range(n_pars):
            out_dir = sel_parent(out_dir)
        return out_dir / mod_rel_path
    else:
        return Path(path)


def files_from_args(ref_path):
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
        parameter_files = [
            get_abs_path(args.in_dir, ref_path) / "{}".format(f)
            for f in os.listdir(get_abs_path(args.in_dir, ref_path))
            if ".yaml" in f or ".yml" in f or ".json" in f]
    else:
        parameter_files = [
            get_abs_path(f, ref_path)
            for f in args.in_files
            if ".yaml" in f or ".yml" in f or ".json" in f]

    if len(parameter_files) < 1:
        print('Please provide at least one input argument')
        sys.exit()
    return parameter_files
