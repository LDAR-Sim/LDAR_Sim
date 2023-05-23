
# Instructions for adding End-to-End tests

## Steps

1. Using LDAR-Sim as normal, setup the parameters and inputs for the scenario you would like to add as a test case in the test suite

2. Change the global_parameter "preseed_random" to True

    ```yaml
    preseed_random: True
    ```

3. Change the global parameter "pregenerate_leaks" to True

    ```yaml
    pregenerate_leaks: True
    ```

4. Change the global parameter "n_simulations" to 1

    ```yaml
    n_simulations: 1
    ```

5. Delete the generator folder from the inputs folder if it exists

6. Copy the inputs folder and the folder containing the simulation parameters inside the test_case_creator folder

7. Run the test suite creator using the command:

    ```cmd
    python LDAR_Sim/LDAR_Sim/testing/end_to_end_testing/e2e_test_case_creator.py <test_name>
    ```

    from a conda terminal inside the LDAR-Sim repository at the highest level directory, where <test_name> is a user input indicating what the end to end test cse folder should be named.

8. Verify that the test has been correctly created in the end to end testing directory.

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
