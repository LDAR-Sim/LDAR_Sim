
# Unit Testing Info

## Unit testing file format guide

Inside of the unit_testing folder, tests should be grouped into sub-folders based on the module that is being tested, with folders matching LDAR-SIm module hierarchy. The folder should be named test_\<module name> For example: testing the method detect_emissions in crews.py should results a file named test_detect_emissions inside a folder structure of test_methods -> test_crews -> test_detect_emissions.py. Each python file containing tests should correspond to a specific method.

## Test naming guide

Tests should be named descriptively, as the test names will not need to be called. Tests must start with test_\<xxx>_ where xxx is a unique number corresponding to all tests in the given testing folder, where the first two numbers are used to indicate the higher level module path, and the final number is used to indicate each test file corresponding to a method within the module. For example: a test testing the method detect_emissions in crews.py should start with test_05x where x is the number corresponding to methods in crews.py

Module Unique Identifiers have been outlined below:

- Files directly under src: 00
- campaigns: 01
- economics: 02
- geography: 03
- initialization: 04
- methods: 05
  - deployment: 11
  - init_func: 12
  - reporting: 13
  - sensors: 14
- out_processing: 06
- utils: 07
- weather: 08
- external_sensors: 09

## Required installation

Before running Pytest coverage, install

```cmd
    pip install pytest-cov
```

## Code Coverage Guide

Pytest-cov allows for generation coverage reports for LDAR-Sim

The recommended command to generate a code coverage report is:

``` cmd
    pytest --cov=src --cov-report=html:LDAR_Sim/LDAR_Sim/testing/coverage/complete --cov-branch  
```

The code coverage report can be found in html format inside the testing/coverage/complete folder

Listed below are some other options for users:

1. For Line/Statement coverage in a HTML report run the following:

    ``` cmd
    pytest --cov=src --cov-report=html:LDAR_Sim/LDAR_Sim/testing/coverage/line
    ```

    The line coverage report can be found in html format inside the testing/coverage/line folder

2. For Line/Statement coverage with results printed to the terminal as well run the following:

    ``` cmd
    pytest --cov=src --cov-report=html:LDAR_Sim/LDAR_Sim/testing/coverage/line --cov-report=term-missing line
    ```

    The line coverage report can be found in html format inside the testing/coverage/line folder
3. For Branch/Condition coverage run the following:

    ``` cmd
    pytest --cov=src --cov-report=html:LDAR_Sim/LDAR_Sim/testing/coverage/branch --cov-branch  
    ```

    The Branch coverage report can be found in html format inside the testing/coverage/branch folder
4. For a % Line coverage pass condition run the following, where x is the desired percentage (for example: for 80% coverage use 80):

    ``` cmd
    pytest --cov=src --cov-report=html:LDAR_Sim/LDAR_Sim/testing/coverage/line --cov-fail-under=<x>
    ```

    The line coverage report can be found in html format inside the testing/coverage/line folder

For more details on pytest code coverage options, reference the documentation for pytest-cov at: <https://pytest-cov.readthedocs.io/en/latest/index.html>

## Pytest configuration

LDAR-Sim is structured in such a away that it uses relative pathways for module imports. This can cause troubles with unit tests, where it expects the full pathways for imports. A solution to this problem is to create a pytest.ini file, that dictates the relative python paths, based on the root folder.

For more details, reference the documentation for pytest configuration at: <https://docs.pytest.org/en/7.1.x/reference/reference.html#configuration-options>
