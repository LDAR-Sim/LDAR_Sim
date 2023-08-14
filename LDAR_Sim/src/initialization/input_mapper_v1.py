# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim input mapper sample
# Purpose:     Example input mapper
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

def input_mapper_v1(parameters):
    """Function to perform all input mapping from version 1.0 parameter files to presently compliant
    parameter files. This is necessary to ensure reverse compatibility - to allow older parameter
    files to run properly.

    **** THIS IS AN EXAMPLE FILE THAT IS PROVIDED AS A TEMPLATE ****

    This function is a series of hooks that fall into several categories:
    1) Construction hooks: these hooks construct newer parameters from older parameters. This is
    necessary if parameters were deprecated in the newest version of the model, but relied upon in
    older versions. For example, newer versions of the program may simply allow specification of a
    start and end date, but not include specification of the number of timesteps. To allow this, a
    construction hook could create start and end date from the number of timesteps using any
    necessary rules to maintain compatibility.

    2) Destruction hooks: these hooks destruct parameters that are no longer in the default set of
    parameters in the model. To continue the above example, if the present version of the model
    does not use number of timesteps, and the number of timesteps is no longer specified in the
    default parameter file - that key should be removed. The issue here is without destruction of
    deprecated parameters - this parameter file will fail validation. Of course, destruction must
    be called AFTER construction so the information in the deprecated parameters is used to map
    to the new parameters before being deleted!

    3) Recalculation hooks: these hooks recalculate variables or map the values. For example, if
    the units have changed, but the key has not - these hooks are necessary to recalculate the new
    units to be compliant with the present version of the model. If the older version of the model
    had a spelling mistake in a string specification, this type of hook would map the parameters.
    Several examples:

    # map an old spelling mistake properly - the present version of LDAR Sim has corrected the
    # spelling mistake but old parameter files continue to use the misspelled value
    if parameters['calculation_method'] == 'categoricle':
        parameters['calculation_method'] = 'categorical'

    # map the leak rate parameter from one unit to another, the newest version uses a different
    # unit, where 0.003332 is the conversion factor
    parameters['leak_rate] = parameters['leak_rate'] * 0.003332

    4) Key-change hooks: these hooks change the key name to a new key name to map the old name to
    the new name.

    :param parameters = a dictionary of parameters that must be mapped to a compliant version
    :return returns a model compliant parameter file dictionary and global parameter file (see notes
     in code).

    In cases where the global parameters are not returned, the global parameters are returned as an
    empty dictionary
    """
    # ----------------------------------------------------------------------------------------------
    # 1. Construction hooks
    # NOTES: Version 1.0 parameter files used to create global parameters by pulling some parameters
    #        from the P_ref program. Thus, this function returns global parameters as well as the
    #        parameters dictionary under analysis. There were no global parameters in v1.0. They
    #        were defined inline in the code.

    # Version 1.0 files are all program files
    # if 'parameter_level' not in parameters:
    #    parameters['parameter_level'] = 'program'

    # Set version
    # if 'version' not in parameters:
    #     parameters['version'] = '1.0'

    # Check if this is P_ref, if so, mine the global parameters
    mined_global_parameters = {}
    # parameters_to_make_global = ['n_simulations', 'timesteps', 'start_year', 'weather_file',
    #                              'print_from_simulations', 'write_data']
    # if parameters['program_name'] == 'P_ref':
    #     for i in parameters_to_make_global:
    #         mined_global_parameters[i] = parameters[i]

    # Construct a programs key
    #     mined_global_parameters['programs'] = []

    # ----------------------------------------------------------------------------------------------
    # 2. Destruction hooks
    # Delete the parameters that are now globals from this program definition - these do nothing
    # for i in parameters_to_make_global:
    #     _ = parameters.pop(i)

    # ----------------------------------------------------------------------------------------------
    # 3. Recalculation hooks
    pass

    # ----------------------------------------------------------------------------------------------
    # 4. Key-change hooks
    pass

    return (parameters, mined_global_parameters)
