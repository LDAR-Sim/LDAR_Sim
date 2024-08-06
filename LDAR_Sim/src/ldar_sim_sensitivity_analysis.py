# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        ldar_sim_sensitivity_analysis.py
# Purpose:     Script to run LDAR-Sim sensitivity analysis.
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
from pathlib import Path

import sensitivity_analysis.parameter_variator
import sensitivity_analysis.sensitivity_processing
from constants.output_messages import RuntimeMessages as rm
from file_processing.input_processing.input_manager import InputManager
from initialization.args import files_from_args_sens  # TODO: move this over to input_processing?
from simulation.sensitivity_simulation_manager import SensitivitySimulationManager


def run_ldar_sim_sensitivity(parameter_filenames: list[str], sens_info: dict):

    input_manager = InputManager()

    simulation_manager: SensitivitySimulationManager = SensitivitySimulationManager(
        input_manager=input_manager, parameter_filenames=parameter_filenames
    )

    simulation_manager.generate_parameters_holder()

    simulation_manager.setup_for_sensitivity_analysis(sens_info)

    simulation_manager.run_sensitivity_analysis()

    simulation_manager.generate_sensitive_analysis_results()


if __name__ == "__main__":
    print(rm.OPENING_MSG)

    root_dir: Path = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    src_dir: Path = root_dir / "src"
    sys.path.insert(1, str(src_dir))

    # -- Retrieve input parameters from commandline argument and parse --
    parameter_filenames, sens_info_file_path = files_from_args_sens(root_dir)

    sensitivity_info: dict = sensitivity_analysis.sensitivity_processing.get_sensitivity_info(
        root_dir, sens_info_file_path, parameter_filenames
    )

    run_ldar_sim_sensitivity(parameter_filenames, sensitivity_info)
