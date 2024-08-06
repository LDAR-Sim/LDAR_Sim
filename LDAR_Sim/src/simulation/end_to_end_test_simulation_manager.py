import os
from pathlib import Path
from typing import Any, override

from constants import param_default_const as pdc
from constants.output_messages import RuntimeMessages as rm
from file_processing.input_processing.input_manager import InputManager
from file_processing.output_processing.summary_output_helpers import get_non_baseline_prog_names
from initialization.args import get_abs_path
from initialization.preseed import gen_seed_emis
from simulation.simulation_helpers import remove_non_preseed_files
from simulation.simulation_manager import SimulationManager


class EndToEndTestSimulationManager(SimulationManager):
    def __init__(self, input_manager: InputManager, parameter_filenames: list[str], test_dir: Path):
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
        self.test_dir: Path = test_dir

        super().__init__(input_manager=input_manager, parameter_filenames=parameter_filenames)
        self.overwrite_test_params()
        self.expected_results: Path = test_dir / "expected_outputs"

    def overwrite_test_params(self):
        for key, value in self.GLOBAL_PARAMS_TO_REP.items():
            self.sim_params[key] = value

        for key, value in self.GLOBAL_OUTPUT_PARAMS.items():
            self.output_params[key] = value

    @override
    def _read_in_parameters(
        self, input_manager: InputManager, parameter_filenames: list[str]
    ) -> None:
        self.sim_params: dict = input_manager.read_and_validate_parameters(parameter_filenames)
        self.out_dir: Path = get_abs_path(
            self.sim_params[pdc.Sim_Setting_Params.OUTPUT], self.test_dir
        )

        self._set_parameters(self.test_dir)

    @override
    def _set_parameters(self, test_dir: Path) -> None:
        super()._set_parameters()

        self.in_dir = get_abs_path(self.sim_params[pdc.Sim_Setting_Params.INPUT], test_dir)

    @override
    def check_generator_files(self) -> bool:
        remove_non_preseed_files(self.generator_dir)

        print(rm.INIT_INFRA)

        if self.preseed_random:
            self.emis_preseed_val, self.force_remake_gen = gen_seed_emis(
                self.simulation_count, self.generator_dir
            )

    @override
    def run_simulations(self, DEBUG) -> None:
        self._run_simulation_multiprocessing(sim_counts=[self.simulation_count])

    @override
    def generate_summary_results(self) -> None:
        non_baseline_progs = get_non_baseline_prog_names(self.programs, self.base_program)
        self.summary_stats_manager.gen_cost_summary_outputs(non_baseline_progs)

    def validate_outputs(self, test: os.DirEntry, comparison_function: callable) -> None:
        comparison_function(test.name, self.out_dir, self.expected_results)
