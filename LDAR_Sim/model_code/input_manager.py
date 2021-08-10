# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim input manager
# Purpose:     Interface for managing, validating, and otherwise dealing with parameters
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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
import os
import yaml
import json
import sys

from utils.check_parameter_types import check_types
from default_parameters.default_global_parameters import default_global_parameters
from default_parameters.default_program_parameters import default_program_parameters
from default_parameters.default_aircraft_parameters import default_aircraft_parameters
from default_parameters.default_OGI_parameters import default_OGI_parameters
from default_parameters.default_OGI_FU_parameters import default_OGI_FU_parameters
from default_parameters.default_satellite_parameters import default_satellite_parameters
from default_parameters.default_truck_parameters import default_truck_parameters
from default_parameters.default_continuous_parameters import default_continuous_parameters


class InputManager:
    def __init__(self):
        """ Constructor creates a lookup of method defaults to run validation against
        """
        # Simulation parameter are parameters that are set up for this simulation
        self.simulation_parameters = copy.deepcopy(default_global_parameters)

        # Construct a lookup of default method parameters
        self.method_defaults = {
            'aircraft': copy.deepcopy(default_aircraft_parameters),
            'OGI': copy.deepcopy(default_OGI_parameters),
            'OGI_FU': copy.deepcopy(default_OGI_FU_parameters),
            'satellite': copy.deepcopy(default_satellite_parameters),
            'truck': copy.deepcopy(default_truck_parameters),
            'continuous': copy.deepcopy(default_continuous_parameters),
        }
        return

    def read_and_validate_parameters(self, parameter_filenames):
        """Method to read and validate parameters
        :param parameter_filenames: a list of paths to parameter files
        :return returns fully validated parameters dictionary for simulation in LDAR-Sim
        """
        raw_parameters = self.read_parameter_files(parameter_filenames)
        self.parse_parameters(raw_parameters)

        # Coerce all paths to absolute paths prior to release, add extra guards for other parts of the code
        # that concatenate strings to construct file paths, and expect trailing slashes
        self.simulation_parameters['wd'] = os.path.abspath(self.simulation_parameters['wd']) + '//'
        self.simulation_parameters['output_directory'] = \
            os.path.abspath(self.simulation_parameters['output_directory']) + '//'
        return(copy.deepcopy(self.simulation_parameters))

    def write_parameters(self, filename):
        """Method to write simulation parameters to the file system
        :param filename: filename to write the parameters to
        """
        with open(filename, 'w') as f:
            f.write(yaml.dump(self.simulation_parameters))

    def read_parameter_files(self, parameter_filenames):
        """Method to read a collection of parameter files and perform any mapping prior to validation.
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
            new_parameters_list[i], mined_global_parameters = self.map_parameters(new_parameters_list[i])
            global_parameters.update(mined_global_parameters)

        # Append the mined global parameters for installation after all other parameter updates
        if len(global_parameters) > 0:
            global_parameters['parameter_level'] = 'global'
            new_parameters_list.append(global_parameters)

        return(new_parameters_list)

    def read_parameter_file(self, filename):
        """Method to read a single parameter file from a filename. This method can be extended to address different
        file formats or mappings.
        :param filename: the path to the parameter file
        :return: dictionary of parameters read from the parameter file
        """
        parameter_set_name, extension = os.path.splitext(os.path.basename(filename))
        new_parameters = {}
        with open(filename, 'r') as f:
            print('Reading ' + filename)
            if extension == '.txt':
                print('Warning: txt file inputs will be depreciated')
                exec(f.read())
                new_parameters.update(eval(parameter_set_name))
            elif extension == '.json':
                new_parameters = json.loads(f.read())
            elif extension == '.yaml' or extension == '.yml':
                new_parameters = yaml.load(f.read(), Loader = yaml.FullLoader)
            else:
                sys.exit('Invalid parameter file format: ' + filename)

        return(new_parameters)

    def map_parameters(self, parameters):
        """Function to map parameters from older versions to the present version, all mappings are externally specified
        in the relevant function.
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
        """Method to parse and validate new parameters, perform type checking, and organize for simulation.

        Programs are then addressed, consecutively adding them in, calling in any methods available in the method
        pool.

        :param new_parameters_list: a list of new parameter dictionaries
        """
        self.simulation_parameters = copy.deepcopy(default_global_parameters)
        programs = []
        method_pool = {}
        for new_parameters in new_parameters_list:
            # Address unsupplied parameter level by defaulting it as global
            if 'parameter_level' not in new_parameters:
                new_parameters['parameter_level'] = 'global'
                print('Warning: parameter_level should be supplied to parameter files, LDAR-Sim interprets parameter'
                      'files as global if unspecified')

            if new_parameters['parameter_level'] == 'global':
                # Extract programs supplied in global parameter files to build programs list
                if 'programs' in new_parameters:
                    if len(new_parameters['programs']) > 0:
                        programs = programs + new_parameters.pop('programs')

                check_types(default_global_parameters, new_parameters, omit_keys = ['programs'])
                self.simulation_parameters.update(new_parameters)

            elif new_parameters['parameter_level'] == 'program':
                check_types(default_program_parameters, new_parameters, omit_keys = ['methods'])

                # Copy all default program parameters to build upon by calling update, then append
                new_program = copy.deepcopy(default_program_parameters)
                new_program.update(new_parameters)
                programs.append(new_program)

            elif new_parameters['parameter_level'] == 'method':
                # Create method pool entry that is referenced by the label
                method_label = new_parameters['label']
                method_pool.update({method_label: new_parameters})

            else:
                sys.exit('Parameter_level of ' + str(new_parameters['parameter_level']) + ' is not possible to parse')

        # Second, install the programs, checking for specified children methods
        for program in programs:
            # Find any orphaned methods that can be installed in this program
            if 'method_labels' in program:
                for method_label in program['method_labels']:
                    method_found = False
                    for i in method_pool:
                        if method_label == i:
                            program['methods'].update({i: copy.deepcopy(method_pool[i])})
                            method_found = True

                    if not method_found:
                        print('Warning, the following method was specified by not supplied ' + method_label)

            # Next, perform type checking and updating from default module parameters, even for methods pre-specified
            for i in program['methods']:
                module = program['methods'][i]['module']

                # Perform type checking from known default methods
                if module in self.method_defaults:
                    check_types(self.method_defaults[module], program['methods'][i])
                    method = copy.deepcopy(self.method_defaults[module])
                    method.update(program['methods'][i])
                    program['methods'][i] = method
                else:
                    print('Warning: no default parameters supplied for supplied method module: ' + module)

            # Finally, manually append some keys from globals that are required to be in the program parameters
            program['start_year'] = self.simulation_parameters['start_year']
            program['timesteps'] = self.simulation_parameters['timesteps']

        # Third, install the programs into the simulation parameters
        self.simulation_parameters['programs'] = programs
