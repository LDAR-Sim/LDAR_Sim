import os
import shutil
from pathlib import Path
from typing import Any, override

import yaml
from constants import param_default_const as pdc
from constants.output_messages import RuntimeMessages as rm
from file_processing.input_processing.input_manager import InputManager
from file_processing.output_processing.summary_output_helpers import get_non_baseline_prog_names
from initialization.args import files_from_path, get_abs_path
from simulation.simulation_helpers import remove_non_preseed_files
from simulation.simulation_manager import SimulationManager


class EndToEndCreationSimulationManager(SimulationManager):
    def __init__(
        self,
        input_manager: InputManager,
        test_creator_dir: Path,
        root_dir: Path,
        script_arguments: list[str],
    ):
        self.GLOBAL_PARAMS_TO_REP: "dict[str, Any]" = {
            pdc.Sim_Setting_Params.SIMS: 2,
            pdc.Sim_Setting_Params.PRESEED: True,
            pdc.Sim_Setting_Params.INPUT: "./inputs",
            pdc.Sim_Setting_Params.OUTPUT: "./outputs",
        }
        self.GLOBAL_OUTPUT_PARAMS: "dict[str, Any]" = {
            pdc.Output_Params.PROGRAM_VISUALIZATIONS: {
                pdc.Output_Params.SINGLE_PROGRAM_TIMESERIES: False
            }
        }
        self.test_creator_dir: Path = test_creator_dir
        self.root_dir: Path = root_dir
        self.parse_script_arguments(script_arguments)
        self.clean_test_creator_dir()
        self.retrieve_test_parameters()
        self.fix_simulation_settings()
        parameter_filenames: list[str] = files_from_path(self.params_dir)
        super().__init__(input_manager=input_manager, parameter_filenames=parameter_filenames)

    def parse_script_arguments(self, script_arguments: list[str]) -> None:
        self.original_input_folder: str = script_arguments[1]
        self.original_param_folder: str = script_arguments[2]
        self.test_name: str = script_arguments[3]
        self.sim_settings_file: str = script_arguments[4]

    def clean_test_creator_dir(self) -> None:
        for item in os.listdir(self.test_creator_dir):
            item_path = os.path.join(self.test_creator_dir, item)
            if item != ".gitignore":
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

    def retrieve_test_parameters(self) -> None:
        self.original_inputs_dir: Path = self.root_dir / self.original_input_folder
        self.original_params_dir: Path = self.root_dir / self.original_param_folder
        self.params_dir: Path = self.test_creator_dir / "params"
        if self.original_params_dir != self.params_dir:
            shutil.copytree(self.original_params_dir, self.params_dir)
        self.test_case_dir: Path = self.test_creator_dir / self.test_name
        if os.path.exists(self.test_case_dir):
            shutil.rmtree(self.test_case_dir)
        os.mkdir(self.test_case_dir)

    def fix_simulation_settings(self) -> None:
        sim_settings_file_path: Path = self.params_dir / self.sim_settings_file
        with open(sim_settings_file_path, "r") as file:
            sim_settings = yaml.safe_load(file)

        for key, value in self.GLOBAL_PARAMS_TO_REP.items():
            sim_settings[key] = value
        with open(sim_settings_file_path, "w") as file:
            yaml.safe_dump(sim_settings, file)

    @override
    def _read_in_parameters(
        self,
        input_manager: InputManager,
        parameter_filenames: list[str],
    ) -> None:
        self.sim_params: dict = input_manager.read_and_validate_parameters(parameter_filenames)
        self.out_dir: Path = get_abs_path("./expected_outputs", self.test_case_dir)
        self._set_parameters()

    @override
    def _set_parameters(self) -> None:
        self.base_program: str = self.sim_params[pdc.Sim_Setting_Params.BASELINE]
        self.in_dir = get_abs_path("./inputs", self.test_creator_dir)
        shutil.copytree(self.original_inputs_dir, self.in_dir)
        if os.path.exists(self.in_dir / "generator"):
            shutil.rmtree(self.in_dir / "generator")
        self.programs = self.sim_params.pop(pdc.Levels.PROGRAM)
        self.virtual_world = self.sim_params.pop(pdc.Levels.VIRTUAL)
        self.output_params = self.sim_params.pop(pdc.Levels.OUTPUTS)
        self.preseed_random = True

        self._set_methods()
        self.overwrite_simulation_settings()

    def overwrite_simulation_settings(self) -> None:
        for key, value in self.GLOBAL_OUTPUT_PARAMS.items():
            self.output_params[key] = value

    @override
    def generate_summary_results(self) -> None:

        print(rm.BATCH_CLEAN.format(batch_count=0))
        self.summary_stats_manager.gen_summary_outputs(False)
        non_baseline_progs = get_non_baseline_prog_names(self.programs, self.base_program)
        self.summary_stats_manager.gen_cost_summary_outputs(non_baseline_progs)

    def format_test_results_location(self, tests_dir: Path) -> None:
        os.chdir(self.root_dir)
        shutil.move(self.params_dir, self.test_case_dir)
        shutil.move(self.in_dir, self.test_case_dir)
        shutil.move(self.test_case_dir, tests_dir / self.test_name)

        test_generator = tests_dir / self.test_name / "inputs" / "generator"
        remove_non_preseed_files(test_generator)
