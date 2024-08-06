import gc
import os
import shutil
from pathlib import Path

import sensitivity_analysis.parameter_variator
from constants import param_default_const as pdc
from constants.sensitivity_analysis_constants import SensitivityAnalysisMapping as sens_map
from file_processing.input_processing.input_manager import InputManager
from initialization.args import get_abs_path
from parameters.parameters_holder import ParametersHolder
from sensitivity_analysis.sensitivity_analysis_results_manager import (
    SensitivityAnalysisResultsManager,
)
from simulation.simulation_manager import SimulationManager


class SensitivitySimulationManager(SimulationManager):
    def __init__(self, input_manager: InputManager, parameter_filenames: list[str]):
        self._read_in_original_parameters(input_manager, parameter_filenames)
        self.setup_sensitivity_properties()
        self.generate_parameters_holder()

    def _read_in_original_parameters(
        self,
        input_manager: InputManager,
        parameter_filenames: list[str],
    ):
        if "out_dir" in parameter_filenames:
            self.original_sim_params: dict = input_manager.read_and_validate_parameters(
                parameter_filenames["parameter_files"]
            )
            self.original_out_dir = get_abs_path(parameter_filenames[pdc.Sim_Setting_Params.OUTPUT])
        else:
            self.original_sim_params: dict = input_manager.read_and_validate_parameters(
                parameter_filenames
            )
            self.original_out_dir = get_abs_path(
                self.original_sim_params[pdc.Sim_Setting_Params.OUTPUT]
            )

        self._set_original_parameters()

    def _set_original_parameters(self):
        self.original_programs = self.original_sim_params.pop(pdc.Levels.PROGRAM)
        self.original_virtual_world = self.original_sim_params.pop(pdc.Levels.VIRTUAL)
        self.original_output_params = self.original_sim_params.pop(pdc.Levels.OUTPUTS)
        self.original_base_program = self.original_sim_params[pdc.Sim_Setting_Params.BASELINE]

    def setup_sensitivity_properties(self):
        self.sensitivity_results_manager: SensitivityAnalysisResultsManager = None
        self.sensitivity_simulation_parameters: list[ParametersHolder] = None
        self.number_of_sens_variations: int = None
        self.sensitivity_program: str = None

    def generate_parameters_holder(self):
        self.parameters_holder = ParametersHolder(
            self.original_sim_params,
            self.original_programs,
            self.original_virtual_world,
            self.original_output_params,
            self.original_base_program,
        )

    def setup_for_sensitivity_analysis(self, sensitivity_info: dict):
        self.number_of_sens_variations = sensitivity_info[
            sens_map.SENS_PARAM_MAPPING[sens_map.SENS_SET_COUNT]
        ]
        self.sensitivity_program = self.parameters_holder.get_non_baseline_program()

        sensitivity_summary_outputs_info: dict = sensitivity_info.pop(sens_map.SENS_SUMMARY_INFO)

        self.sensitivity_simulation_parameters: list[ParametersHolder] = (
            sensitivity_analysis.parameter_variator.vary_parameter_values(
                self.parameters_holder,
                self.sensitivity_program,
                **sensitivity_info,
            )
        )

        self.sensitivity_results_manager = SensitivityAnalysisResultsManager(
            out_dir=self.original_out_dir,
            parameter_variations=sensitivity_info[sens_map.PARAM_VARIATIONS],
            sens_level=sensitivity_info[sens_map.PARAM_LEVEL],
            sens_summary_info=sensitivity_summary_outputs_info,
        )

        self.initialize_original_outputs()

    def initialize_original_outputs(self):
        if os.path.exists(self.original_out_dir):
            shutil.rmtree(self.original_out_dir)
        os.makedirs(self.original_out_dir)

    def run_sensitivity_analysis(self):
        for sim_params in self.sensitivity_simulation_parameters:
            gc.collect()
            self.set_simulation_parameters(sim_params)
            self.setup_properties()
            self.check_inputs()
            self.initialize_outputs(None, False)
            self.check_generator_files()
            self.setup_virtual_world()
            self.setup_emissions()
            self.setup_weather()
            self.setup_daylight()
            self.initialize_summary_managers()
            self.run_simulations(DEBUG=False)
            self.generate_summary_results()
        self.generate_sensitive_analysis_results()

    def set_simulation_parameters(self, sim_params: ParametersHolder):
        self.sim_params: dict = sim_params.get_simulation_settings()
        self.out_dir: Path = get_abs_path(self.sim_params[pdc.Sim_Setting_Params.OUTPUT])
        self.base_program: str = self.sim_params[pdc.Sim_Setting_Params.BASELINE]
        self.in_dir: Path = get_abs_path(self.sim_params[pdc.Sim_Setting_Params.INPUT])
        self.programs: dict = sim_params.get_programs()
        self.virtual_world: dict = sim_params.get_virtual_world()
        self.output_params: dict = sim_params.get_output()
        self.preseed_random: bool = self.sim_params[pdc.Sim_Setting_Params.PRESEED]

        self._set_methods()

    def generate_sensitive_analysis_results(self):
        self.sensitivity_results_manager.gen_sensitivity_results(self.sensitivity_program)
        self.sensitivity_results_manager.gen_sensitivity_visualizations(self.sensitivity_program)
        self.sensitivity_results_manager.save_sensitivity_variations_mapping(
            self.number_of_sens_variations
        )
        self.sensitivity_results_manager.gen_sensitivity_summary_results()
