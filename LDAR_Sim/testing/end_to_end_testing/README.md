
# Instructions for adding End-to-End tests

## Steps

1. Using LDAR-Sim as normal, setup the parameters and inputs for the scenario you would like to add as a test case in the test suite. It is recommended for creating end-to-end tests that only necessary inputs are included in the inputs folder.

2. Run the test suite creator using the command:

    ```cmd
    python LDAR_Sim/LDAR_Sim/testing/end_to_end_testing/e2e_test_case_creator.py <inputs folder> <parameters folder> <test_name> <Global parameter file name>
    ```

    from a conda terminal inside the LDAR-Sim repository at the highest level directory, where "inputs folder" and "parameters folder" are paths to the inputs and parameters folders from base LDAR-Sim (the LDAR_Sim folder containing code) respectively. An example of this would be "inputs" and "simulations" respectively. <test_name> is a user input indicating what the end to end test case folder should be named. "Global parameter file is name of the global parameters file, for example: "G_.yaml".

3. Verify that the test has been correctly created in the end to end testing directory.

# Instructions for Running End-to-End tests

## Option 1

Run the End-To-End suite runner by running the command:

```cmd
python LDAR_Sim/LDAR_Sim/testing/end_to_end_testing/e2e_suite_runner.py
```

from a conda terminal inside the LDAR-Sim repository at the highest level directory.

## Option 2

Create a Visual Studio Code run configuration matching the following configuration:

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run LDAR-sim end-to-end tests",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/LDAR_Sim/LDAR_Sim/testing/end_to_end_testing/e2e_suite_runner.py",
      "console": "integratedTerminal",
      "args": []
    }
  ]
}
```
