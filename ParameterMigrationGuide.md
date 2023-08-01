# LDAR-Sim V3.0 Parameter Migration Guide

## Purpose

This guide is intended to assist users users who are updating to LDAR-Sim V3.0 by providing instructions on how to update their parameter files to the supported V3.0 format.

## What changed between V2 and V3.0?

The majority of the LDAR_Sim parameters from V2 still exist in V3.0, but some of them have moved parameter files. In LDAR-Sim V3.0, global parameters has been renamed to Simulation_setting. A new parameters file: the "virtual_world" parameters has been introduced to contain parameters that inform the LDAR-Sim virtual world.

### Details

Many of the parameter you would find in programs in V2 you will now find in the Virtual World parameters file. Do note that there can only be 1 Virtual World parameters file per simulation set. This has been done to avoid confusion on the construction of the LDAR-Sim virtual world. The LDAR-Sim virtual world informs properties such as leak rate, leak frequency, etc. and is shared between all programs in simulation.

Parameters that would previously be found in the LDAR-Sim global parameters can now be found in the Simulation_settings parameter file. Other than the file level renaming completed for clarity, the parameters situated in this file are largely unchanged.

## New Parameter files

### Simulation Settings

Contains parameters used to inform properties of the LDAR-Sim simulation, such as input and output folders, years to simulate, simulation set name, etc. These parameters are largely unchanged from what used to be the global parameters.

### Virtual World

Contains parameters used to inform the LDAR-Sim virtual world. These parameters will typically be a direct match for parameters previously found at the program level in V2. There can only be one Virtual World parameter file per simulation set.

## Moving from V2 parameters to V3.0 Parameters

### 1. Creating the Simulation Settings parameter file

1. Locate the global parameters file for the version 2 of the parameters you are looking to convert. Typically this will be named something like G_.yml. Global parameters can be identified by locating the parameter file with the contents:

    ```yaml
    parameter_level: global
    ```

2. Rename the global parameters files to:

    ```shell
    Simulation_settings.yml
    ```

3. Open up the newly named Simulation_settings.yml. Find the following values:

    ```yaml
    parameter_level:
    version:
    ```

4. Change those values to match what is shown below:

     ```yaml
    parameter_level: "simulation_settings"
    version: 3.0
    ```

    **Caution:** This step is case sensitive. Spelling must match.

### 2. Creating the Virtual World parameter file

1. Locate the program parameter file associate with the baseline program for your simulation. It's name will match the value set for the baseline_program parameter in the Simulation_settings (Your transformed global parameters file). This will often be set to P_none.

    For Example:

    ```yaml
    baseline_program: P_none
    ```

    You are looking for a file with the property:

    ```yaml
    program_name: P_none
    ```

    Ideally the name of the should also be P_none.yaml, but this is not required.

2. Copy the key value pairs of the following parameters from the baseline program if they exist:

    ```yaml
    weather_file:
    weather_is_hourly:
    infrastructure_file:
    site_samples:
    subtype_times_file:
    subtype_file:
    consider_weather:
    repair_delay:
        type:
        val:
    emissions:
        consider_venting:
        leak_dist_params:
        leak_dist_type:
        leak_file:
        leak_file_use:
        LPR:
        max_leak_rate:
        units:
    NRd:
    economics:
        carbon_price_tonnesCO2e:
        cost_CCUS:
        GWP_CH4:
        sale_price_natgas:
        repair_costs:
            vals:
            file:
        verification_cost:
    ```

    ***Note:*** If some of the parameters listed above do not exist in the baseline program, this is perfectly fine, these missing values will be inherited from the default values.

3. Created a new yaml file. Name it:

    ```shell
    virtual_world.yml.
    ``````

4. Paste the contents copied from the baseline program into this new file

5. Add the following parameters and values. They can go anywhere, but the top of the file recommended.

    ```yaml
    version: "3.0"
    parameter_level: "virtual_world"
    ```

### 3. Necessary Program parameter file changes

**Important:** You must repeat this step for each program file in the parameter files

Program files can be identified by the property:

```yaml
parameter_level: "program"
```

1. Ensure each program file contains ***only*** the following parameters:

    ```yaml
    version:
    parameter_level:
    method_labels:
    program_name:
    ```

2. The values for "method_labels" and "program_name" should remain unchanged.

3. Set the values for the version and parameter_level as indicated

    ```yaml
    version: "3.0"
    parameter_level: "program"
    ```

### 4. Necessary Method parameter file changes

**Important:** You must repeat this step for each method file in the parameter files

Method files can be identified by the property:

```yaml
parameter_level: "method"
```

1. Find the version property in the method file

    ```yaml
    version:
    ```

2. Set the version to 3.0

    ```yaml
    version: 3.0
    ```

### Congratulations: The move from parameter files version 2 to version 3.0 is complete
