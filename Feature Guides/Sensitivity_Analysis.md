# LDAR-Sim Sensitivity Analysis Guide

## Introduction

The purpose of this guide is to provide users with instructions and examples on how to run the LDAR-Sim Sensitivity Analysis module. Sensitivity Analysis with the LDAR-Sim.

## Key Sensitivity Analysis Information

Sensitivity Analysis module is performed based on the parameter level. This means that either virtual world parameters, program parameters for one or programs or method parameters for one or more methods can be varied for Sensitivity Analysis, but not at the same time.

Multiple parameters can be varied at once for sensitivity analysis, however it is important to properly understand how this works. Variations for parameters in the Sensitivity Analysis module are provided as lists, for example, performing Sensitivity Analysis on virtual world parameters:

```yml
emissions:
  repairable_emissions:
    production_rate: [0.0065, 0.013]
    duration: [365, 730]
```

is a potential input to the Sensitivity Analysis file, which will generate two sets of simulations. The first set will have:

```yml
emissions:
  repairable_emissions:
    production_rate: 0.0065
    duration: 365
```

and the second set will have:

```yml
emissions:
  repairable_emissions:
    production_rate: 0.013
    duration: 730
```

### On Having Multiple Program

One key intricacy of LDAR-Sim Sensitivity Analysis functionality is that it is intended to support only a single program at time. If the simulation parameters include more than one program, one will be chosen at random for sensitivity analysis.

Specifically, outputs for virtual world level sensitivity analysis will compare the performance of a single program on different virtual worlds.

Program level sensitivity analysis will compare the performance of variations of a base program against each other.

Method level sensitivity analysis will compare the performance of variations of a program varied by generating variations of one or more of it's methods.

## Setup

The LDAR-Sim sensitivity analysis module runs using standard LDAR-Sim parameter files with one new addition: the new sensitivity info parameter file.
It is recommend to change the output directory in the simulation settings parameters as so not to overwrite existing outputs.

```yml
output_directory: {new output location}
```

### Creating the Sensitivity Analysis Information File

The Sensitivity Analysis Information File must be a .yaml or .yml file that follows a specific format.

```yml
Sensitivity Parameter Level: # The level of parameters on which to perform sensitivity analysis. Options are: "virtual_world", "programs" or "methods".
Sensitivity Analysis Permutations: # How many different sensitivity analysis permutations are described (The length of the list of values to evaluate for each parameters). For example: if we have Parameter: [Value 1, Value 2] that would be a value of 2.
Sensitivity Parameter Variations: 
  # Parameters and Lists of values to set for those parameters that fall under the specified parameter level.
  # Looks like:
  # Parameter: [Value 1, Value 2, Value 3]
Sensitivity Summary Outputs Information: 
  Confidence Interval: # Can be either 1 number or a list of two numbers.
    # One number, for example 95, will result in sensitivity analysis outputs reporting the 100-(CI/2)th and (CI/2)th percentile (2.5th and 97.5th percentiles). Two numbers, for example 5 and 90 will results in sensitivity analysis outputs reporting those percentiles (5th and 90th percentiles)
```

This format varies slightly based on the parameter level on which Sensitivity Analysis is being performed. See the following examples below for different parameter levels.

#### Virtual World Level Sensitivity Analysis

```yml
Sensitivity Parameter Level: "virtual_world"
Sensitivity Analysis Permutations: 3
Sensitivity Parameter Variations:
  emissions:
    repairable_emissions:
      emissions_production_rate: [0.00325, 0.0065, 0.013]
      duration: [182, 365, 730]
Sensitivity Summary Outputs Information:
  Confidence Interval: [85]
```

#### Program Level Sensitivity Analysis

```yml
Sensitivity Parameter Level: "programs"
Sensitivity Analysis Permutations: 3
Sensitivity Parameter Variations:
  - Program Name: "Example_Program"
    Program Sensitivity Parameters:
      economics: 
        verification_cost: [100, 200, 300]
Sensitivity Summary Outputs Information:
  Confidence Interval: [85]
```

#### Method Level Sensitivity Analysis

##### One Method

```yml
Sensitivity Parameter Level: "methods"
Sensitivity Analysis Permutations: 3
Sensitivity Parameter Variations:
  - Method Name: "Example_Method"
    Method Sensitivity Parameters:
      surveys_per_year: [1,2,3]
Sensitivity Summary Outputs Information:
  Confidence Interval: [85]
```

##### Two Methods

```yml
Sensitivity Parameter Level: "methods"
Sensitivity Analysis Permutations: 3
Sensitivity Parameter Variations:
  - Method Name: "Example_Method"
    Method Sensitivity Parameters:
      surveys_per_year: [1,2,3]
  - Method Name: "Example_Method_2"
    Method Sensitivity Parameters:
      surveys_per_year: [2,4,6]
Sensitivity Summary Outputs Information:
  Confidence Interval: [85]
```

## Running LDAR-Sim Sensitivity Analysis

LDAR-Sim sensitivity analysis is run through the command line, similar to LDAR-Sim. The command takes the form:

```cmd
-p <path to your LDAR-Sim parameters> --sensitivity_info <path to sensitivity info file>
```

or

```cmd
--in_dir <path to your LDAR-Sim parameters> --sensitivity_info <path to sensitivity info file>
```

Where the first argument (-P or --in_dir) indicates that the following argument will be the path to the input directory where the simulation parameter files are contained.

The second argument must be the path to the input directory, for example:

```cmd
./simulations
```

For parameter files inside the simulations folder in the inner LDAR-Sim file folder.

The third argument (--sensitivity_info) indicates that the following argument will be the path to the new sensitivity information file.

The fourth argument must be the path to the sensitivity info file, for example:

```cmd
./simulations/sens_info.yml
```

For sensitivity information file named sens_info located in the simulations folder in the inner LDAR-SIm folder.
**Note: Remember to include the file extension in the file path for the sensitivity info file (.yml)**

### Example Command

```cmd
-p simulations/example_sensitivity_analysis --sensitivity_info simulations/example_sensitivity_analysis/sensitivity_info.yml
```
