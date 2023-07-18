# External Sensor Coding Practices

This document provides coding guidelines and best practices for developing external sensors/plugins for use with LDAR-Sim. Following these practices will ensure consistency, readability, and maintainability of the codebase.

## Table of Contents

- [External Sensor Coding Practices](#external-sensor-coding-practices)
  - [Table of Contents](#table-of-contents)
  - [General Guidelines](#general-guidelines)
  - [File Structure](#file-structure)
  - [Naming Conventions](#naming-conventions)
  - [Code Formatting](#code-formatting)
  - [Documentation](#documentation)
  - [Error Handling](#error-handling)
  - [Testing](#testing)
  - [Detect Emissions Function Requirement](#detect-emissions-function-requirement)

## General Guidelines

- Keep the code modular, well-organized, and maintainable.
- Follow the [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) for code style and formatting.
  - If possible use the autopep8 auto formatting
- Write code that is concise, readable, and self-explanatory.
- Avoid unnecessary code duplication; favor code reuse.

## File Structure

- Organize your plugin files such that they are located in the `external_sensors` folder
- Each sensor should be one file
- Consider using a package structure for larger plugins.

## Naming Conventions

- Use descriptive and meaningful names for variables, functions, classes, and modules.
- Follow the Python naming conventions: use lowercase with underscores for variables and functions (`my_variable`, `my_function`), and use CamelCase for classes (`MyClass`).
- Avoid single-character variable names except for simple loop counters.

## Code Formatting

- Use consistent and readable code formatting.
- Keep lines within a reasonable length (80-120 characters).
- Use blank lines and proper spacing to enhance readability.
- Follow appropriate naming conventions for constants and global variables.
- If possible use Black as a formatter.

## Documentation

- Provide clear and concise comments and docstrings. See [Detect Emissions Function Requirement](#detect-emissions-function-requirement) for more details.
- Include a high-level overview of the plugin's purpose and functionality.
- Document public interfaces, classes, and functions.
- Add inline comments where necessary to explain complex code logic.
- Include code examples or usage instructions when necessary.

- Within the docstring, be sure to include the probability of detection curve that the sensor should be replicating. Additionally, add in additional values that the function requires as inputs. For example:

```python

def detect_emissions(self, site, covered_leaks, covered_equipment_rates, covered_site_rate,
                     site_rate, venting, equipment_rates):
    """
    An alternative sensor

    Utilizes 3 values set as the MDL:
        mdl = [a, b, c]
        where 
        a and b are utilize for the POD curve variables 
        c represents the floor/minimum cutoff value of the leak rates
    """
```

## Error Handling

- Use proper error handling techniques to handle exceptions.
- Catch specific exceptions instead of using broad `except` clauses.
- Log or report errors appropriately to aid troubleshooting and debugging.
- Handle exceptions gracefully to avoid crashes or unexpected behavior.

## Testing

- Write unit tests to verify the correctness of your plugin.
- Test all major functionalities and edge cases.
- Use test frameworks like `unittest` or `pytest`.
- Ensure the tests are easily runnable and provide clear output.

## Detect Emissions Function Requirement

The external sensor function should have the following signature and functionality:

```python
def detect_emissions(site, covered_leaks, covered_equipment_rates, covered_site_rate,
                    site_rate, venting, equipment_rates):
    """
    Perform sensor measurements and generate a site report.

    Args:
        site (site obj): Site in which crew is working at
        covered_leaks (list): List of leak objects that can be detected by the crew
        covered_equipment_rates (list): List of equipment leak rates that can be
                                        detected by the crew
        covered_site_rate (float): Total site emissions from leaks that are observable
                                    from a crew
        site_rate (float): Total site emissions from all leaks at the site 
        venting (float): Total site emissions from venting
        equipment_rates (list): List of equipment leak rates for each equipment group

    Returns:
        site_report (dict):
            'site' (site obj): Same as input
            'leaks_present' (list): Same as covered_leaks input
            'site_true_rate' (float): Same as site_rate
            'site_measured_rate' (float): Total emissions from all leaks measured
            'equip_measured_rates' (list): Total emissions from all leaks measured for each equipment group
            'venting' (float): Same as input
            'found_leak' (boolean): Indicates if the crew found at least one leak at the site
    """
    # Implement the sensor function logic here
    # ...
    # Return the site report
```

**Note:** Rates provided by LDAR-Sim are in g/s, however resulting rate should be in kg/hr. 