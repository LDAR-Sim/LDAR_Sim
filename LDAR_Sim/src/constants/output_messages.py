"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        output_messages.py
Purpose:     Holds messages used throughout the program


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

SUMMARY_PLOT_GENERATION_MESSAGE = "Generating cross-program summary plots"


class RuntimeMessages:

    OPENING_MSG = """
        You are running LDAR-Sim version 4.0.0 an open sourced software (MIT) license.
        Provide any issues, comments, questions, or recommendations by
        adding an issue to https://github.com/LDAR-Sim/LDAR_Sim.git
        """

    GEN_WARNING_MSG = """\
        !!!Pre-generated initialization files exist!!!
        LDAR-Sim may not create new emissions to model with
        """

    INIT_WEATHER = "...Initializing weather"
    INIT_INFRA = "...Initializing infrastructure"
    INIT_EMISS = "...Initializing emissions"
    INIT_DAYLIGHT = "...Initializing daylight"

    SIM_SET = "......Simulating set {simulation_number}"
    SIM_PROG = ".........Simulating program: {prog_name}"
    FIN_PROG = "......... Finished simulating program: {prog_name}"
    FIN_SIM_SET = "...Finished simulating set {simulation_number}"
    BATCH_CLEAN = "...Cleaning up batch {batch_count} data"

    READING_FILE = "Reading in {file}"

    HASHING = "Hashing files"
    HASHING_COMPLETE = "Done hashing files"

    GEN_INFRA = "Generating infrastructure"

    CHECK_WEATHER = "Weather data checked. Continuing simulation."
    ATTEMPT_AWS_WEATHER_DOWNLOAD = "Weather data not found. Attempting to download from AWS now ..."
    COMPLETE_WEATHER_DOWNLOAD = "Weather data download complete"

    GEN_EMISS = "Generating emissions for Set_{i} simulations"


class InputHelpText:
    INPUT_FILE_HELP_TEXT = (
        "Input files, separate with space, can be absolute path or relative to"
        "root directory (LDAR_Sim). All files should have yaml, yml, or json extensions \n"
        "ie. python ldar_sim_main.py ./file1.json c:/path/to/file/file2.json"
    )
    INPUT_DIR_HELP_TEXT = (
        "Input Directory, folder containing input files, will input all files within"
        "folder that have yaml, yml or json extensions \n"
        "ie. python ldar_sim_main.py --in_dir ./folder_with_infiles",
    )
    OUTPUT_DIR_HELP_TEXT = (
        "Output Directory, folder containing output files, will save all output files \n"
        "ie. python ldar_sim_main.py --out_dir ./folder_for_save_outputs"
    )
