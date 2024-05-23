# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.args
# Purpose:     Handle program input arguments
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
#
# ------------------------------------------------------------------------------

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from constants.error_messages import Input_Processing_Messages as ipm
from constants.general_const import File_Extension_Constants as fc
from constants.output_messages import InputHelpText as iht


def get_abs_path(path, ref_folder=None):
    """Get the absolute path of a file from the reference folder
        If none is specified, use the current working directory

    Args:
        path (string): relative (or absolute) path to a file
        ref_folder (Path, optional): reference folder. Defaults to None.
    """

    def sel_parent(p_folder):
        return p_folder.parent

    if ref_folder is None:
        ref_folder = Path(os.getcwd())
    n_pars = len(path) - len(path.lstrip("."))
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
    """
    Look for parameter files supplied as arguments - if parameter files are supplied as
    arguments, proceed to parse and type check input parameter type with the input manager.
    The program will also accept flagged input directory , (-P or --in_dir)
    """
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    # ---Declare input arguments---
    parser.add_argument(
        "in_files",
        type=str,
        nargs="*",
        help=iht.INPUT_FILE_HELP_TEXT,
    )
    parser.add_argument(
        "-P",
        "--in_dir",
        help=iht.INPUT_DIR_HELP_TEXT,
    )
    parser.add_argument(
        "-X",
        "--out_dir",
        help=iht.OUTPUT_DIR_HELP_TEXT,
    )
    parser.add_argument(
        "-D", "--debug", action="store_true", help=iht.DEBUG_HELP_TEXT, default=False
    )

    args = parser.parse_args()
    if args.in_dir is not None:
        # if an input directory is specified, get all files within that are in the directory
        # Get all yaml or json files in specified folder
        parameter_files = [
            get_abs_path(args.in_dir, ref_path) / "{}".format(f)
            for f in os.listdir(get_abs_path(args.in_dir, ref_path))
            if fc.YML in f or fc.YAML in f or fc.JSON in f
        ]
    else:
        parameter_files = [
            get_abs_path(f, ref_path)
            for f in args.in_files
            if fc.YAML in f or fc.YML in f or fc.JSON in f
        ]

    if len(parameter_files) < 1:
        print(ipm.MISSING_ARGUMENT_ERROR)
        sys.exit()
    if args.out_dir is not None:
        out_dir = get_abs_path(args.out_dir, ref_path)
        return {"parameter_files": parameter_files, "out_dir": str(out_dir)}

    return parameter_files, args.debug


def files_from_path(in_path):
    if in_path is not None:
        # if an input directory is specified, get all files within that are in the directory
        # Get all yaml or json files in specified folder
        parameter_files = [
            in_path / "{}".format(f)
            for f in os.listdir(in_path)
            if fc.YAML in f or fc.YML in f or fc.JSON in f
        ]

    if len(parameter_files) < 1:
        print(ipm.MISSING_ARGUMENT_ERROR)
        sys.exit()

    return parameter_files
