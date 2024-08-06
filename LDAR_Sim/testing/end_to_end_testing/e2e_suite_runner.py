# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        End-to-End Test Suite Runner
# Purpose:     Interface for running LDAR-Sim End-to-End test.
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
from testing_utils.result_verification import compare_outputs

# Get directories and set up root
e2e_test_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir: Path = e2e_test_dir.parent.parent
src_dir: Path = root_dir / "src"
tests_dir: Path = e2e_test_dir / "test_suite"
os.chdir(root_dir)
# Add the source directory to the import file path to import all LDAR-Sim modules
sys.path.insert(1, str(src_dir))

if __name__ == "__main__":

    from file_processing.input_processing.input_manager import InputManager
    from initialization.args import files_from_path
    from simulation.end_to_end_test_simulation_manager import EndToEndTestSimulationManager

    for test in os.scandir(tests_dir):

        if test.is_dir():
            print(f"Running test: {test.name}")
            test_dir: Path = Path(os.path.normpath(test))
            params_dir = test_dir / "params"
            parameter_filenames = files_from_path(params_dir)
            input_manager = InputManager()

            simulation_manager: EndToEndTestSimulationManager = EndToEndTestSimulationManager(
                input_manager=input_manager,
                parameter_filenames=parameter_filenames,
                test_dir=test_dir,
            )

            simulation_manager.check_inputs()

            simulation_manager.initialize_outputs(input_manager)

            simulation_manager.check_generator_files()

            simulation_manager.setup_virtual_world()

            simulation_manager.setup_emissions()

            simulation_manager.setup_weather()

            simulation_manager.setup_daylight()

            simulation_manager.run_simulations(DEBUG=False)

            simulation_manager.generate_summary_results()

            simulation_manager.validate_outputs(test=test, comparison_function=compare_outputs)
