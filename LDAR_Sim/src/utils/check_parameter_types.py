# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        check_parameter_types
# Purpose:     Check input parameter types
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

import sys


def check_types(default, test, omit_keys=None, fatal=False):
    """Helper function to recursively check the type of parameter dictionaries
    :param default: default element to test
    :param test: test element to test
    :param omit_keys: a list of dictionary keys to omit from further recursive testing
    :param fatal: boolean to control whether sys.exit() is called upon a error
    """
    # Infer 'None' to an empty list
    if omit_keys is None:
        omit_keys = []

    # Perform type checking, allow integer inputs to be passed through as floats (but not reverse)
    # Also allow placeholder values
    if type(default) is type(test):
        type_ok = True
    elif type(default) is float and type(test) is int:
        type_ok = True
    elif default == '_placeholder_int_' and (type(test) is int):
        type_ok = True
    elif default == '_placeholder_float_' and (type(test) is int or type(test) is float):
        type_ok = True
    elif default == '_placeholder_str_' and type(test) is str:
        type_ok = True
    else:
        type_ok = False

    if type_ok:
        # Proceed to test for dict or list types to recursively examine
        if isinstance(test, dict):
            for i in test:
                if i not in omit_keys:
                    if i not in default:
                        print(
                            'Key ' + i +
                            ' present in test parameters, but not in default parameters')
                        if fatal:
                            sys.exit()

                    else:
                        check_types(default[i], test[i], omit_keys=omit_keys, fatal=fatal)

        elif isinstance(test, list):
            if len(default) > 0 and len(test) > 0:
                for i in range(len(test)):
                    check_types(default[0], test[i], omit_keys=omit_keys, fatal=fatal)

    else:
        print('Parameter type mismatch')
        print('Default parameter: ' + str(default) + ' is ' + str(type(default)))
        print('Test parameter: ' + str(test) + ' is ' + str(type(test)))
        if fatal:
            sys.exit()
