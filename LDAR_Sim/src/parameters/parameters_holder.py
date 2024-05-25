import copy
from typing import Any

from parameters.genric_parameters import GenericParameters
from parameters.high_level_parameters import HighLevelParameters


from constants import param_default_const, error_messages


class ParametersHolder:

    VIRTUAL_WORLD_SUB_PARAMETER_MAPPING = {
        param_default_const.Virtual_World_Params.INFRA: None,
        param_default_const.Virtual_World_Params.REPAIR: None,
        param_default_const.Virtual_World_Params.EMIS: {
            param_default_const.Virtual_World_Params.REPAIRABLE: None,
            param_default_const.Virtual_World_Params.NON_REPAIRABLE: None,
        },
    }

    OUTPUTS_SUB_PARAMETER_MAPPING = {
        param_default_const.Output_Params.PROGRAM_OUTPUTS: None,
        param_default_const.Output_Params.SUMMARY_OUTPUTS: {
            param_default_const.Output_Params.SUMMARY_FILES: None,
            param_default_const.Output_Params.SUMMARY_STATS: {
                param_default_const.Output_Params.TIMESERIES_SUMMARY: None,
                param_default_const.Output_Params.EMISSIONS_SUMMARY: None,
            },
        },
        param_default_const.Output_Params.SUMMARY_VISUALIZATIONS: None,
    }

    METHOD_SUB_PARAMETER_MAPPING = {
        param_default_const.Method_Params.SENSOR: None,
        param_default_const.Method_Params.COVERAGE: None,
        param_default_const.Method_Params.COST: None,
        param_default_const.Method_Params.T_BW_SITES: None,
        param_default_const.Method_Params.SCHEDULING: None,
        param_default_const.Method_Params.WEATHER_ENVS: None,
        param_default_const.Method_Params.FOLLOW_UP: None,
    }

    PROGRAM_SUB_PARAMETER_MAPPING = {
        param_default_const.Levels.METHOD: {},
        param_default_const.Program_Params.ECONOMICS: None,
    }

    def __init__(
        self,
        simulation_settings: dict[str, Any],
        programs: dict[dict[str, Any]],
        virtual_world: dict[str, dict[str, Any]],
        outputs: dict[str, Any],
        baseline_program: str,
    ) -> None:
        self._baseline = baseline_program
        self._simulation_settings: GenericParameters = GenericParameters(simulation_settings)
        self._virtual_world: HighLevelParameters = HighLevelParameters(
            virtual_world, self.VIRTUAL_WORLD_SUB_PARAMETER_MAPPING
        )
        self._output: HighLevelParameters = HighLevelParameters(
            outputs, self.OUTPUTS_SUB_PARAMETER_MAPPING
        )
        self._programs: dict[str, HighLevelParameters] = {}
        for name, program in programs.items():
            prog_param_mapping: dict = copy.deepcopy(self.PROGRAM_SUB_PARAMETER_MAPPING)
            for method in program[param_default_const.Program_Params.METHODS]:
                prog_param_mapping[param_default_const.Levels.METHOD][method] = copy.deepcopy(
                    self.METHOD_SUB_PARAMETER_MAPPING
                )
            self._programs[name] = HighLevelParameters(program, prog_param_mapping)

    def alter_parameter(self, level: str, key: str, value: Any) -> None:
        if level == param_default_const.Levels.SIMULATION:
            self._simulation_settings.alter_parameter(key, value)
        elif level == param_default_const.Levels.VIRTUAL:
            self._virtual_world.alter_parameter(key, value)
        elif level == param_default_const.Levels.OUTPUTS:
            self._output.alter_parameter(key, value)
        else:
            raise ValueError(
                error_messages.ParameterInteractionMessages.INVALID_PARAMETER_LEVEL_ERROR.format(
                    level=level
                )
            )

    def get_non_baseline_program(self) -> HighLevelParameters:
        for name, program in self._programs.items():
            if not self._baseline == program.get_parameter_value(
                param_default_const.Program_Params.NAME
            ):
                return name

    def get_baseline_program(self) -> HighLevelParameters:
        return self._programs[self._baseline]

    @property
    def baseline_program_name(self) -> str:
        return self._baseline

    def get_program(self, program_name: str) -> HighLevelParameters:
        return self._programs[program_name]

    def add_program(self, program_name: str, program: HighLevelParameters) -> None:
        self._programs[program_name] = program

    def remove_program(self, program_name: str) -> None:
        self._programs.pop(program_name)

    def get_simulation_settings(self) -> GenericParameters:
        return self._simulation_settings.to_dict()

    def get_virtual_world(self) -> HighLevelParameters:
        return self._virtual_world.to_dict()

    def get_output(self) -> HighLevelParameters:
        return self._output.to_dict()

    def get_programs(self) -> list[dict[str:dict]]:
        return {name: program.to_dict() for name, program in self._programs.items()}

    def alter_simulation_info(self, variation_number: int) -> None:
        outputs_dir: str = self._simulation_settings.get_parameter_value(
            param_default_const.Sim_Setting_Params.OUTPUT
        )
        self._simulation_settings.alter_parameter(
            param_default_const.Sim_Setting_Params.OUTPUT, f"{outputs_dir}/{variation_number}"
        )
