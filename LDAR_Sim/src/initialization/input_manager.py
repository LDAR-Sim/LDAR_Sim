# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim input manager
# Purpose:     Interface for managing, validating, and otherwise dealing with parameters
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
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
import yaml
import json
import sys
from pathlib import Path

from utils.check_parameter_types import check_types


class InputManager:
    def __init__(self, root_dir):
        """ Constructor creates a lookup of method defaults to run validation against
        """
        self.root_dir = root_dir
        g_param_file = self.root_dir / 'src/default_parameters/g_default.yml'
        with open(g_param_file, 'r') as f:
            default_global_parameters = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.simulation_parameters = copy.deepcopy(default_global_parameters)
        # Simulation parameter are parameters that are set up for this simulation
        return

    def read_and_validate_parameters(self, parameter_filenames):
        """Method to read and validate parameters
        :param parameter_filenames: a list of paths to parameter files
        :return returns fully validated parameters dictionary for simulation in LDAR-Sim
        """
        raw_parameters = self.read_parameter_files(parameter_filenames)
        self.parse_parameters(raw_parameters)

        # Coerce all paths to absolute paths prior to release, add extra guards for other parts of
        # the code that concatenate strings to construct file paths, and expect trailing slashes
        self.simulation_parameters['input_directory'] = self.root_dir \
            / self.simulation_parameters['input_directory']
        self.simulation_parameters['output_directory'] = self.root_dir \
            / self.simulation_parameters['output_directory']
        self.remove_type_placeholders(self.simulation_parameters)
        return(copy.deepcopy(self.simulation_parameters))

    def write_parameters(self, filename):
        """Method to write simulation parameters to the file system
        :param filename: filename to write the parameters to
        """
        with open(filename, 'w') as f:
            f.write(yaml.dump(self.simulation_parameters))

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
        global_parameters = {}
        for i in range(len(new_parameters_list)):
            new_parameters_list[i], mined_global_parameters = \
                self.map_parameters(new_parameters_list[i])
            global_parameters.update(mined_global_parameters)

        # Append the mined global parameters for installation after all other parameter updates
        if len(global_parameters) > 0:
            global_parameters['parameter_level'] = 'global'
            new_parameters_list.append(global_parameters)

        return(new_parameters_list)

    def read_parameter_file(self, filename):
        """Method to read a single parameter file from a filename. This method can be extended to
        address different file formats or mappings.
        :param filename: the path to the parameter file
        :return: dictionary of parameters read from the parameter file
        """
        # Get File location
        file_path = Path(filename)
        _, extension = file_path.stem, file_path.suffix
        if filename[0] == ".":
            # All relative need to be in reference to root folder
            fn_abspart = filename.split("./")[-1]
            temp_dir = self.root_dir
            # if parent folder is required, move to parent directory number
            # of times in relative path (.../ will backup 2 directories)
            n_parents = filename.count("..")
            for pcnt in range(n_parents):
                temp_dir = temp_dir.parent
            param_file = temp_dir / fn_abspart
        else:
            param_file = Path(filename)

        new_parameters = {}

        with open(param_file, 'r') as f:
            print('Reading ' + filename)
            if extension == '.json':
                new_parameters = json.loads(f.read())
            elif extension == '.yaml' or extension == '.yml':
                new_parameters = yaml.load(f.read(), Loader=yaml.FullLoader)
            else:
                sys.exit('Invalid parameter file format: ' + filename)

        return(new_parameters)

    def map_parameters(self, parameters):
        """Function to map parameters from older versions to the present version, all mappings are
        externally specified in the relevant function.
        :param parameters = the input parameter dictionary
        :return returns the compliant parameters dictionary, and optionally mined global parameters
        """
        if 'version' not in parameters:
            print('Warning: interpreting parameters as version 2.0 because version key was missing')
            parameters['version'] = '2.0'

        # address all parameter mapping, the input_mapper_v1 is available as a template
        mined_global_parameters = {}
        # if parameters['version'] == '1.0':
        #     parameters, mined_global_parameters = input_mapper_v1(parameters)
        return(parameters, mined_global_parameters)

    def parse_parameters(self, new_parameters_list):
        """Method to parse and validate new parameters, perform type checking, and organize for
        simulation.

        Programs are then addressed, consecutively adding them in, calling in any methods available
        in the method pool.

        :param new_parameters_list: a list of new parameter dictionaries
        """
        programs = []
        method_pool = {}
        for new_parameters in new_parameters_list:
            # Address unsupplied parameter level by defaulting it as global
            if 'parameter_level' not in new_parameters:
                new_parameters['parameter_level'] = 'global'
                print('Warning: parameter_level should be supplied to parameter files, LDAR-Sim '
                      'interprets parameter files as global if unspecified')

            if new_parameters['parameter_level'] == 'global':
                # Extract programs supplied in global parameter files to build programs list
                if 'programs' in new_parameters:
                    if len(new_parameters['programs']) > 0:
                        programs = programs + new_parameters.pop('programs')

                check_types(self.simulation_parameters, new_parameters, omit_keys=['programs'])
                self.simulation_parameters.update(new_parameters)

            elif new_parameters['parameter_level'] == 'program':
                if 'default_parameters' not in new_parameters:
                    def_file = 'p_default.yml'
                else:
                    def_file = new_parameters['default_parameters']
                g_param_file = self.root_dir / 'src/default_parameters/{}'.format(def_file)
                with open(g_param_file, 'r') as f:
                    default_program_parameters = yaml.load(f.read(), Loader=yaml.FullLoader)
                check_types(default_program_parameters, new_parameters, omit_keys=['methods'])
                # Copy all default program parameters to build upon by calling update, then append
                new_program = copy.deepcopy(default_program_parameters)
                # HBD - Should be able to change single item in a dict and not he entire dict
                self.retain_update(new_program, new_parameters)
                programs.append(new_program)

            elif new_parameters['parameter_level'] == 'method':
                # Create method pool entry that is referenced by the label
                method_label = new_parameters['label']
                # self.retain_update(method_pool[method_label], new_parameters)
                method_pool.update({method_label: new_parameters})

            else:
                sys.exit('Parameter_level of ' + str(new_parameters['parameter_level']) +
                         ' is not possible to parse')

        # Second, install the programs, checking for specified children methods
        for program in programs:
            # Find any orphaned methods that can be installed in this program
            if 'method_labels' in program and program['method_labels'] is not None:
                for method_label in program['method_labels']:
                    method_found = False
                    for i in method_pool:
                        if method_label == i:
                            program['methods'].update({i: copy.deepcopy(method_pool[i])})
                            method_found = True

                    if not method_found:
                        print('Warning, the following method was specified by not supplied ' +
                              method_label)

            # Next, perform type checking and updating from default module parameters, even for
            # methods pre-specified
            for midx, method in program['methods'].items():
                if 'default_parameters' not in method:
                    def_file = 'm_default.yml'
                else:
                    def_file = new_parameters['default_parameters']
                m_param_file = self.root_dir / 'src/default_parameters/{}'.format(def_file)
                with open(m_param_file, 'r') as f:
                    default_module = yaml.load(f.read(), Loader=yaml.FullLoader)
                check_types(
                    default_module,
                    method,
                    omit_keys=['default_parameters'])
                self.retain_update(default_module, method)
                program['methods'][midx] = default_module

            # Finally, manually append some keys from globals that are required to be in the program
            # parameters
            program['start_date'] = self.simulation_parameters['start_date']
            program['end_date'] = self.simulation_parameters['end_date']

        # Third, install the programs into the simulation parameters
        self.simulation_parameters['programs'] = programs

    def retain_update(self, obj, new_parameters):
        for idx, param in new_parameters.items():
            if isinstance(param, dict):
                self.retain_update(obj[idx], param)
            else:
                obj.update({idx: param})
        return

    def remove_type_placeholders(self, obj):
        placeholders = ['_placeholder_int_', '_placeholder_float_', '_placeholder_str_']
        if isinstance(obj, list):
            iterator = enumerate(obj)
        elif isinstance(obj, dict):
            iterator = obj.items()
        for idx, param in iterator:
            if param in placeholders:
                obj[idx] = None
            # special case, empty list
            elif isinstance(param, (list, tuple)) \
                    and len(param) == 1 and (param[0] in placeholders):
                obj[idx] = []
            elif isinstance(param, (dict, list)):
                self.remove_type_placeholders(obj[idx])
        return
