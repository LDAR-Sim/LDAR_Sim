
# Unit Testing Info

Before running Pytest coverage, install

```cmd
    pip install pytest-cov
```

## Code Coverage Gude

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
