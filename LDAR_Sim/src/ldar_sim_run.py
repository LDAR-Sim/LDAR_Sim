# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim run
# Purpose:     Main simulation sequence
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
import cProfile
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from constants.file_processing_const import IOLocationConstants as io_loc
from constants.output_messages import RuntimeMessages as rm
from file_processing.input_processing.input_manager import InputManager
from initialization.args import files_from_args
from log_utils.logging_config import setup_error_logging
from simulation.simulation_manager import SimulationManager


def run_ldar_sim(parameter_filenames, DEBUG=False):
    try:

        input_manager = InputManager()

        simulation_manager: SimulationManager = SimulationManager(
            input_manager=input_manager, parameter_filenames=parameter_filenames
        )

        simulation_manager.check_inputs()

        simulation_manager.initialize_outputs(input_manager, setup_output_logging=True)

        simulation_manager.check_generator_files()

        simulation_manager.setup_infrastructure()

        simulation_manager.setup_emissions()

        simulation_manager.setup_weather()

        simulation_manager.setup_daylight()

        simulation_manager.run_simulations(DEBUG=DEBUG)

        simulation_manager.generate_summary_results()

    except Exception as e:
        logger: logging.Logger = logging.getLogger(__name__)
        logger.exception(rm.SIMULATION_ERROR)
        raise e


def setup_logging(root_dir: Path) -> None:
    # Setup log folder
    log_folder: Path = root_dir / io_loc.LOG_FOLDER
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M")

    setup_error_logging(
        log_folder=log_folder,
        timestamp=timestamp,
        log_to_file=True,
        log_to_console=True,
    )


if __name__ == "__main__":

    print(rm.OPENING_MSG)

    root_dir: Path = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    setup_logging(root_dir)

    src_dir: Path = root_dir / "src"
    sys.path.insert(1, str(src_dir))

    # -- Retrieve input parameters from commandline argument and parse --
    parameter_filenames, _DEBUG = files_from_args(root_dir)

    if _DEBUG:
        print(rm.DEBUG_MODE_ON)
        cProfile.run(
            "run_ldar_sim(parameter_filenames, _DEBUG)",
            "../Benchmarking/benchmark1_results",
            "cumulative",
        )
    else:
        run_ldar_sim(parameter_filenames, _DEBUG)
