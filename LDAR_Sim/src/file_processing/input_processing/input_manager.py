# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim input manager
# Purpose:     Interface for managing, validating, and otherwise dealing with parameters
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

import copy
import json
import os
import sys
from pathlib import Path

import yaml

from initialization.versioning import (
    check_major_version,
)
from utils.check_parameter_types import check_types
from constants.general_const import File_Extension_Constants as fc
from constants.file_name_constants import Default_Files as df
from constants.error_messages import Input_Processing_Messages as ipm, Versioning_Messages as vm
from constants.file_processing_const import ParameterProcessingConst
import constants.param_default_const as pc
from constants.output_messages import RuntimeMessages as rm
from constants.general_const import Version_Constants as vc, Placeholder_Constants as phc


class InputManager:

    def __init__(self) -> None:
        """Constructor creates a lookup of method defaults to run validation against"""
        sim_settings_file = "./src/default_parameters/simulation_settings_default.yml"
        with open(sim_settings_file, "r") as f:
            default_sim_setting_parameters = yaml.load(f.read(), Loader=yaml.SafeLoader)
        self.simulation_parameters = copy.deepcopy(default_sim_setting_parameters)

        self.old_params = False
        # Simulation parameter are parameters that are set up for this simulation
        return

    def read_and_validate_parameters(self, parameter_filenames):
        """Method to read and validate parameters
        :param parameter_filenames: a list of paths to parameter files
        :return returns fully validated parameters dictionary for simulation in LDAR-Sim
        """
        raw_parameters = self.read_parameter_files(parameter_filenames)
        self.parse_parameters(raw_parameters)

        # Add extra guards for other parts of the code that concatenate
        # strings to construct file paths, and expect trailing slashes
        self.remove_type_placeholders(self.simulation_parameters)
        self.validate_names()
        return copy.deepcopy(self.simulation_parameters)

    def write_parameters(self, filename):
        """Method to write simulation parameters to the file system
        :param filename: filename to write the parameters to
        """
        with open(filename, "w") as f:
            f.write(yaml.dump(self.simulation_parameters, Dumper=NoAliasDumper))

    def read_parameter_files(self, parameter_filenames):
        """Method to read a collection of parameter files and perform any mapping prior to
        validation.
        :param parameter_filenames: a list of paths to parameter files
        :return returns a list of parameter dictionaries
        """
        # Read in the parameter files
        new_parameters_list = []
        for parameter_filename in parameter_filenames:
            new_parameters_list.append(self.read_parameter_file(parameter_filename))

        # Perform any mapping, optionally accumulating mined global parameters
        for i in range(len(new_parameters_list)):
            new_parameters_list[i] = self.map_parameters(new_parameters_list[i])

        return new_parameters_list

    def read_parameter_file(self, filename):
        """Method to read a single parameter file from a filename. This method can be extended to
        address different file formats or mappings.
        :param filename: the path to the parameter file
        :return: dictionary of parameters read from the parameter file
        """
        # Get File location
        param_file = Path(filename)
        extension = param_file.suffix

        new_parameters = {}

        if not os.path.exists(param_file):
            print(ipm.MISSING_FILE_ERROR.format(file=param_file))
            if not param_file.is_absolute():
                print(ipm.RELATIVE_FILE_PATH_ERROR)
            sys.exit()

        with open(param_file, "r") as f:
            print(rm.READING_FILE.format(file=filename.name))
            if extension == fc.JSON:
                new_parameters = json.loads(f.read())
            elif extension == fc.YML or extension == fc.YAML:
                new_parameters = yaml.load(f.read(), Loader=yaml.SafeLoader)
            else:
                sys.exit(ipm.INVALID_PARAM_FILE_FORMAT.format(filename=filename))

        return new_parameters

    def handle_parameter_versioning(self, parameters) -> None:
        if not self.old_params:
            if pc.Common_Params.VERSION not in parameters:
                print(vm.VERSION_WARNING.format(current_version=vc.CURRENT_FULL_VERSION))
                parameters[pc.Common_Params.VERSION] = vc.CURRENT_FULL_VERSION

            expected_version_string = ".".join([vc.CURRENT_MAJOR_VERSION, vc.CURRENT_MINOR_VERSION])

            if str(parameters[pc.Common_Params.VERSION]) != expected_version_string:
                if str(parameters[pc.Common_Params.VERSION]) == vc.CURRENT_MAJOR_VERSION:
                    print(vm.MAJOR_VERSION_ONLY_WARNING)
                    sys.exit()
                else:
                    major_version_check = check_major_version(
                        str(parameters[pc.Common_Params.VERSION]), vc.CURRENT_MAJOR_VERSION
                    )
                    if major_version_check == 1:
                        print(vm.NEWER_PARAMETER_WARNING)
                        sys.exit()
                    elif major_version_check == -1:
                        print(vm.LEGACY_PARAMETER_WARNING)
                        sys.exit()
                    else:
                        print(vm.MINOR_VERSION_MISMATCH_WARNING)
                        self.old_params = True
        return

    def map_parameters(self, parameters):
        """Function to map parameters from older versions to the present version, all mappings are
        externally specified in the relevant function.
        :param parameters = the input parameter dictionary
        :return returns the compliant parameters dictionary, and optionally mined global parameters
        """
        self.handle_parameter_versioning(parameters)

        return parameters

    def parse_parameters(self, new_parameters_list: list[dict]):
        """Method to parse and validate new parameters, perform type checking, and organize for
        simulation.

        Programs are then addressed, consecutively adding them in, calling in any methods available
        in the method pool.

        :param new_parameters_list: a list of new parameter dictionaries
        """
        programs = {}
        method_pool = {}
        if not any(
            new_parameter.get(pc.Common_Params.PARAM_LEVEL) == pc.Levels.OUTPUTS
            for new_parameter in new_parameters_list
        ):
            new_parameters_list.append({pc.Common_Params.PARAM_LEVEL: pc.Levels.OUTPUTS})

        for new_parameters in new_parameters_list:
            # Address unsupplied parameter level by defaulting it as simulation_settings
            if pc.Common_Params.PARAM_LEVEL not in new_parameters:
                new_parameters[pc.Common_Params.PARAM_LEVEL] = pc.Levels.SIMULATION
                print(ipm.PARAMETER_INTERPRET_WARNING)

            if new_parameters[pc.Common_Params.PARAM_LEVEL] == pc.Levels.SIMULATION:
                # Extract programs supplied in simulation_settings parameter files
                # to build programs list
                if pc.Levels.PROGRAM in new_parameters:
                    if len(new_parameters[pc.Levels.PROGRAM]) > 0:
                        programs = programs + new_parameters.pop(pc.Levels.PROGRAM)

                check_types(
                    self.simulation_parameters, new_parameters, omit_keys=[pc.Levels.PROGRAM]
                )
                self.retain_update(self.simulation_parameters, new_parameters)

            elif new_parameters[pc.Common_Params.PARAM_LEVEL] == pc.Levels.VIRTUAL:
                if ParameterProcessingConst.DEFAULT_PARAM_STRING not in new_parameters:
                    def_file = df.VIRTUAL_DEF_FILE
                else:
                    def_file = new_parameters[ParameterProcessingConst.DEFAULT_PARAM_STRING]
                v_world_param_file = ParameterProcessingConst.DEFAULT_PARAM_PATHWAY.format(def_file)
                with open(v_world_param_file, "r") as f:
                    default_v_world_params = yaml.load(f.read(), Loader=yaml.SafeLoader)
                check_types(default_v_world_params, new_parameters)
                new_v_world = copy.deepcopy(default_v_world_params)
                self.retain_update(new_v_world, new_parameters)
                self.simulation_parameters[pc.Levels.VIRTUAL] = new_v_world

            elif new_parameters[pc.Common_Params.PARAM_LEVEL] == pc.Levels.PROGRAM:
                if ParameterProcessingConst.DEFAULT_PARAM_STRING not in new_parameters:
                    def_file = df.PROG_DEF_FILE
                else:
                    def_file = new_parameters[ParameterProcessingConst.DEFAULT_PARAM_STRING]
                p_param_file = ParameterProcessingConst.DEFAULT_PARAM_PATHWAY.format(def_file)
                with open(p_param_file, "r") as f:
                    default_program_parameters = yaml.load(f.read(), Loader=yaml.SafeLoader)
                check_types(
                    default_program_parameters, new_parameters, omit_keys=[pc.Levels.METHOD]
                )
                # Copy all default program parameters to build upon by calling update, then append
                new_program = copy.deepcopy(default_program_parameters)
                # HBD - Should be able to change single item in a dict and not the entire dict
                self.retain_update(new_program, new_parameters)
                programs.update({new_program[pc.Program_Params.NAME]: new_program})

            elif new_parameters[pc.Common_Params.PARAM_LEVEL] == pc.Levels.METHOD:
                # Create method pool entry that is referenced by the label
                method_label = new_parameters[pc.Method_Params.NAME]
                # self.retain_update(method_pool[method_label], new_parameters)
                method_pool.update({method_label: new_parameters})
            elif new_parameters[pc.Common_Params.PARAM_LEVEL] == pc.Levels.OUTPUTS:
                if ParameterProcessingConst.DEFAULT_PARAM_STRING not in new_parameters:
                    def_file = df.OUTPUT_DEF_FILE
                else:
                    def_file = new_parameters[ParameterProcessingConst.DEFAULT_PARAM_STRING]
                output_param_file = ParameterProcessingConst.DEFAULT_PARAM_PATHWAY.format(def_file)
                with open(output_param_file, "r") as f:
                    default_output_params = yaml.load(f.read(), Loader=yaml.SafeLoader)
                check_types(default_output_params, new_parameters)
                new_outputs = copy.deepcopy(default_output_params)
                self.retain_update(new_outputs, new_parameters)
                self.simulation_parameters[pc.Levels.OUTPUTS] = new_outputs
            else:
                sys.exit(
                    ipm.PARAMETER_PARSING_ERROR.format(
                        level=new_parameters[pc.Common_Params.PARAM_LEVEL]
                    )
                )

        # Double check there is at least 1 program
        if len(programs) == 0:
            sys.exit(ipm.NO_PROGRAMS_WARNING)

        # Second, install the programs, checking for specified children methods
        for p_idx, program in programs.items():
            programs[p_idx][pc.Levels.METHOD] = {}
            # Install methods from the method labels into the program
            if (
                pc.Program_Params.METHODS in program
                and program[pc.Program_Params.METHODS] is not None
            ):
                for method_label in program[pc.Program_Params.METHODS]:
                    method_found = False
                    for i in method_pool:
                        if method_label == i:
                            programs[p_idx][pc.Levels.METHOD].update(
                                {i: copy.deepcopy(method_pool[i])}
                            )
                            method_found = True

                    if not method_found:
                        print(ipm.MISSING_METHOD_ERROR.format(method=method_label))

            # Next, perform type checking and updating from default module parameters, even for
            # methods pre-specified
            for midx, method in program[pc.Levels.METHOD].items():
                if ParameterProcessingConst.DEFAULT_PARAM_STRING not in method:
                    def_file = df.METH_DEF_FILE
                else:
                    def_file = new_parameters[ParameterProcessingConst.DEFAULT_PARAM_STRING]
                m_param_file = ParameterProcessingConst.DEFAULT_PARAM_PATHWAY.format(def_file)
                with open(m_param_file, "r") as f:
                    default_module = yaml.load(f.read(), Loader=yaml.SafeLoader)
                check_types(
                    default_module,
                    method,
                    omit_keys=[ParameterProcessingConst.DEFAULT_PARAM_STRING],
                )
                self.retain_update(default_module, method)
                programs[p_idx][pc.Levels.METHOD][midx] = default_module

        # Third, install the programs into the simulation parameters
        self.simulation_parameters[pc.Levels.PROGRAM] = programs

    def retain_update(self, obj, new_parameters):
        for idx, param in new_parameters.items():
            if isinstance(param, dict):
                self.retain_update(obj[idx], param)
            else:
                obj.update({idx: param})
        return

    def remove_type_placeholders(self, obj):
        placeholders = [phc.PLACEHOLDER_INT, phc.PLACEHOLDER_FLOAT, phc.PLACEHOLDER_STR]
        if isinstance(obj, list):
            iterator = enumerate(obj)
        elif isinstance(obj, dict):
            iterator = obj.items()
        for idx, param in iterator:
            if param in placeholders:
                obj[idx] = None
            # special case, empty list
            elif (
                isinstance(param, (list, tuple)) and len(param) == 1 and (param[0] in placeholders)
            ):
                obj[idx] = []
            elif isinstance(param, (dict, list)):
                self.remove_type_placeholders(obj[idx])
        return

    def validate_names(self):
        invalid_names = {"none", "null", "nan"}
        for name in self.simulation_parameters["programs"].keys():
            if name.lower() in invalid_names:
                sys.exit(ipm.INVALID_NAME_ERROR.format(level=pc.Levels.PROGRAM, name=name))
            for method in self.simulation_parameters["programs"][name][pc.Program_Params.METHODS]:
                if method.lower() in invalid_names:
                    sys.exit(ipm.INVALID_NAME_ERROR.format(level=pc.Levels.METHOD, name=method))


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True
