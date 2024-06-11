# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        utils.check_parameter_types
# Purpose:     Check input parameter types
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

import sys
from constants.general_const import Placeholder_Constants as pc
from constants.error_messages import Initialization_Messages as im


def check_types(default, test, name, omit_keys=None, fatal=False):
    """Helper function to recursively check the type of parameter dictionaries
    :param default: default element to test
    :param test: test element to test
    :param file_name: name of the file being tested
    :param omit_keys: a list of dictionary keys to omit from further recursive testing
    :param fatal: boolean to control whether sys.exit() is called upon an error
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
    elif default == pc.PLACEHOLDER_INT and (type(test) is int):
        type_ok = True
    elif default == pc.PLACEHOLDER_FLOAT and (type(test) is int or type(test) is float):
        type_ok = True
    elif default == pc.PLACEHOLDER_STR and type(test) is str:
        type_ok = True
    else:
        type_ok = False

    if type_ok:
        # Proceed to test for dict or list types to recursively examine
        if isinstance(test, dict):
            for i in test:
                if i not in omit_keys:
                    if i not in default:
                        print(im.PARAMETER_CREATION_ERROR_MESSAGE.format(key=i, name=name))
                        fatal = True
                        if fatal:
                            sys.exit()

                    else:
                        check_types(default[i], test[i], name, omit_keys=omit_keys, fatal=fatal)

        elif isinstance(test, list):
            if len(default) > 0 and len(test) > 0:
                for i in range(len(test)):
                    check_types(default[0], test[i], name, omit_keys=omit_keys, fatal=fatal)

    else:
        print(
            im.PARAMETER_TYPE_MISMATCH_ERROR_MESSAGE.format(
                default=str(default),
                def_type=str(type(default)),
                test=str(test),
                test_type=str(type(test)),
                name=name,
            )
        )
        fatal = True
        if fatal:
            sys.exit()
