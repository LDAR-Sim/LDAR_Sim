import copy
from typing import Any
from parameters.parameters_holder import ParametersHolder
from constants import param_default_const, error_messages
from parameters.genric_parameters import GenericParameters


def vary_parameter_values(
    simulation_parameters: ParametersHolder,
    sensitivity_program: str,
    parameter_level: str,
    number_of_variations: int,
    parameter_variations: dict[str, Any] | list[dict[str, Any]],
) -> list[ParametersHolder]:
    """
    Varies the parameter values as specified for sensitivity analysis.

    Args:
        simulation_parameters (ParametersHolder): The original simulation parameters.
        parameter_level (str): The parameter level at which the sensitivity analysis is performed.
        number_of_variations (int): The number of variations of parameters supplied.
        parameter_variations (dict[str, Any]): The parameter variations to apply.
        method_name (str, optional): The name of the method to vary parameters for
        (only applicable if parameter_level is 'METHOD'). Defaults to None.

    Returns:
        list[ParametersHolder]: A list of new simulation parameters with varied parameter values.

    Raises:
        ValueError: If the parameter level is not recognized or valid for the sensitivity analysis.
    """
    # Function implementation...
    # Initialize the list of new simulation parameters
    new_simulation_parameters: list[ParametersHolder] = []
    # If the sensitivity analysis is at the virtual world level
    if parameter_level == param_default_const.Levels.VIRTUAL:
        # Loop through the number of variations
        for i in range(number_of_variations):
            # Create a deep copy of the simulation parameters
            parameters: ParametersHolder = copy.deepcopy(simulation_parameters)
            # Vary all the specified parameters
            for key, value in parameter_variations.items():
                for index in range(i, len(value), number_of_variations):
                    parameters.alter_parameter(
                        param_default_const.Levels.VIRTUAL, key, value[index]
                    )
            # Append the new parameters to the list
            new_simulation_parameters.append(parameters)
    # If the sensitivity analysis is at the program level
    elif parameter_level == param_default_const.Levels.PROGRAM:
        # Create a deep copy of the simulation parameters
        parameters: ParametersHolder = copy.deepcopy(simulation_parameters)
        # Remove the original programs
        for program in simulation_parameters.get_programs():
            parameters.remove_program(program)
        parameters.add_program(
            simulation_parameters.baseline_program_name,
            simulation_parameters.get_baseline_program(),
        )
        # Loop through the number of variations
        for i in range(number_of_variations):
            for program_name, program_variations in parameter_variations.items():
                # Create a deep copy of the non-baseline program (will return the first if multiple)
                program_parameters: GenericParameters = copy.deepcopy(
                    simulation_parameters.get_program(program_name)
                )
                # Alter the name of the program
                program_parameters.alter_parameter(
                    param_default_const.Program_Params.NAME, f"{program_name}_{i}"
                )
                # Vary all the specified parameters
                for key, value in program_variations.items():
                    program_parameters.alter_parameter(key, value[i])
                # Add the new program to the parameters
                parameters.add_program(f"{program_name}_{i}", program_parameters)
        # Append the new parameters to the list
        new_simulation_parameters.append(parameters)
    # If the sensitivity analysis is at the method level
    elif parameter_level == param_default_const.Levels.METHOD:
        # Create a deep copy of the simulation parameters
        parameters: ParametersHolder = copy.deepcopy(simulation_parameters)
        # Loop through the number of variations
        for i in range(number_of_variations):
            # Create a deep copy of the non-baseline program (will return the first if multiple)
            program_parameters: GenericParameters = copy.deepcopy(
                simulation_parameters.get_program(sensitivity_program)
            )
            # Alter the name of the program
            program_parameters.alter_parameter(
                param_default_const.Program_Params.NAME, f"{sensitivity_program}_{i}"
            )

            method_names: list[str] = program_parameters.get_parameter(
                param_default_const.Program_Params.METHODS
            )

            for method_name, variations in parameter_variations.items():
                # Replace the method to vary with a copy with a different name
                prog_methods: GenericParameters = program_parameters.get_parameter(
                    param_default_const.Levels.METHOD
                )
                target_method: GenericParameters = prog_methods.get_parameter(method_name)

                prog_methods.delete_parameter(method_name)

                prog_methods.add_parameter(f"{method_name}_{i}", target_method)

                program_parameters.override_parameter(
                    param_default_const.Levels.METHOD, prog_methods
                )

                method_names.remove(method_name)

                method_names.append(f"{method_name}_{i}")

                # Create a new dictionary with the method name and the parameter variations
                alter_dict = {param_default_const.Levels.METHOD: {f"{method_name}_{i}": {}}}

                for key, value in variations.items():
                    key_vals: dict | Any = {}
                    for index in range(i, len(value), number_of_variations):
                        if isinstance(value[index], dict):
                            key_vals.update(value[index])
                        else:
                            key_vals = value[index]
                    alter_dict[param_default_const.Levels.METHOD][f"{method_name}_{i}"][
                        key
                    ] = key_vals

                # Alter the name of the method
                alter_dict[param_default_const.Levels.METHOD][f"{method_name}_{i}"][
                    param_default_const.Method_Params.NAME
                ] = f"{method_name}_{i}"
                # Alter the parameters of the method
                program_parameters.alter_parameters(alter_dict)
                # Add the new program to the parameters
                parameters.add_program(f"{sensitivity_program}_{i}", program_parameters)
            # Update the method names in the program
            program_parameters.alter_parameter(
                param_default_const.Program_Params.METHODS, method_names
            )
        # Remove the original programs
        for program in simulation_parameters.get_programs():
            parameters.remove_program(program)
        parameters.add_program(
            simulation_parameters.baseline_program_name,
            simulation_parameters.get_baseline_program(),
        )
        # Edit the base program
        parameters.alter_parameter(
            param_default_const.Levels.SIMULATION,
            param_default_const.Sim_Setting_Params.REFERENCE,
            f"{sensitivity_program}_{0}",
        )
        # Append the new parameters to the list
        new_simulation_parameters.append(parameters)
    # If the parameter level is not recognized or valid for the sensitivity analysis
    else:
        # Raise a value error
        raise ValueError(
            error_messages.SensitivityAnalysisMessages.INVALID_PARAMETER_LEVEL_ERROR.format(
                parameter_level=parameter_level
            )
        )
    for i, new_params in enumerate(new_simulation_parameters):
        new_params.alter_simulation_info(i)
    # Return the new simulation parameters
    return new_simulation_parameters
