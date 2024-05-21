# LDAR-Sim Documentation for Input Parameters and Data

Github Repository: LDAR-Sim

Version: 4.0

Branch: Master

Document Custodian: Sally Jang

Email: <sally@highwoodemissions.com>

--------------------------------------------------------------------------------

## Table of Contents

- [LDAR-Sim Documentation for Input Parameters and Data](#ldar-sim-documentation-for-input-parameters-and-data)
  - [Table of Contents](#table-of-contents)
  - [1. Read this first](#1-read-this-first)
    - [Notes for Developers](#notes-for-developers)
  - [2. Introduction](#2-introduction)
  - [3. File Structure](#3-file-structure)
  - [4. Introducing Parameter Files](#4-introducing-parameter-files)
    - [Parameter file usage](#parameter-file-usage)
    - [Parameter Hierarchy](#parameter-hierarchy)
    - [Versioning of Parameter Files](#versioning-of-parameter-files)
    - [Parameter File Formats](#parameter-file-formats)
  - [5. Simulation Settings](#5-simulation-settings)
    - [\<parameter\_level\> (simulation\_settings)](#parameter_level-simulation_settings)
    - [\<version\> (simulation\_settings)](#version-simulation_settings)
    - [\<input\_directory\>](#input_directory)
    - [\<output\_directory\>](#output_directory)
    - [\<baseline\_program\>](#baseline_program)
    - [\<reference\_program\> WIP](#reference_program-wip)
    - [\<processes\_count\>](#processes_count)
    - [\<simulation\_count\>](#simulation_count)
    - [\<preseed\_random\>](#preseed_random)
  - [6. Output Settings](#6-output-settings)
    - [\<parameter\_level\> (outputs)](#parameter_level-outputs)
    - [\<version\> (outputs)](#version-outputs)
  - [7. Virtual World Setting](#7-virtual-world-setting)
  - [8. Program Inputs](#8-program-inputs)
  - [9. Method Inputs](#9-method-inputs)
  - [10. Virtual World Defining Files](#10-virtual-world-defining-files)
  - [11. Legacy Inputs](#11-legacy-inputs)
    - [Simulation Settings Parameters](#simulation-settings-parameters)
      - [\<pregenerate\_leaks\>](#pregenerate_leaks)
      - [\<print\_from\_simulation\>](#print_from_simulation)
      - [\<outputs\>](#outputs)
      - [\<site\_visits\>](#site_visits)
      - [\<leaks\>](#leaks)
      - [\<sites\>](#sites)
      - [\<timeseries\>](#timeseries)
      - [\<plots\>](#plots)
      - [\<batch\_reporting\>](#batch_reporting)
      - [\<make\_plots\>](#make_plots)
    - [Virtual World Settings Parameters](#virtual-world-settings-parameters)
      - [\<consider\_venting\>](#consider_venting)
      - [\<weather\_is\_hourly\>](#weather_is_hourly)
      - [\<infrastructure\_file\>](#infrastructure_file)
      - [\<subtype\_file\>](#subtype_file)
      - [\<leak\_dist\_params\>](#leak_dist_params)
      - [\<leak\_dist\_type\>](#leak_dist_type)
      - [\<leak\_file\>](#leak_file)
      - [\<leak\_file\_use\>](#leak_file_use)
      - [\<max\_leak\_rate\>](#max_leak_rate)
      - [\<units\>](#units)
      - [\<n\_init\_leaks\_prob\>](#n_init_leaks_prob)
      - [\<n\_init\_days\>](#n_init_days)
      - [\<subtype\_leak\_dist\_file\>](#subtype_leak_dist_file)
      - [\<subtype\_times\_file\>](#subtype_times_file)
      - [\<vent\_file\>](#vent_file)
  - [12. Data sources, modelling confidence and model sensitivity](#12-data-sources-modelling-confidence-and-model-sensitivity)
    - [Duty Holder / Operator (historical LDAR data)](#duty-holder--operator-historical-ldar-data)
    - [Duty Holder / Operator (organizational data)](#duty-holder--operator-organizational-data)
    - [Technology / Solution Provider / Operator (if self-performing LDAR)](#technology--solution-provider--operator-if-self-performing-ldar)
    - [Modeling Expert](#modeling-expert)
  - [13. References](#13-references)

--------------------------------------------------------------------------------

## 1\. Read this first

Please note the following before reading, using, or modifying this document:

- The purpose of this document is to introduce LDAR-Sim, provide guidance for use, and catalogue input parameters, files, data, and arguments required to run the LDAR-Sim model.
- The document you are now reading will _always_ be associated with a specific version or branch of LDAR-Sim. Multiple versions of this document therefore exist, as multiple versions and sub-versions of LDAR-Sim exist.
- **If you are submitting a pull request to the public LDAR-Sim repo**, please update this documentation alongside modifications to code. Your pull request will not be approved without updating this document with relevant changes to inputs, how they work, and their implications for outputs.
- For more information on LDAR-Sim, including code, instructions, and additional resources, please visit the Github page by [clicking this link](https://github.com/LDAR-Sim/LDAR_Sim).
- If you find any errors or inaccuracies in this documentation or in LDAR-Sim, please contact the document custodian (email included above) or leave a ticket in the Git Issues [link](https://github.com/LDAR-Sim/LDAR_Sim/issues).
- The parameter descriptions in this document are provided in an order matching that of parameters in the default parameter files. When updating this document to add new parameters descriptions, ensure the ordering is correct.
- _**Useful tip for searching the document:**_ If searching for the entry describing as specific parameter as opposed to to searching for mentions of that parameter, search for <parameter_name> to uniquely match the entry describing the parameter, instead of any mention of it.

--------------------------------------------------------------------------------

### Notes for Developers

If you are developing in LDAR-Sim, please adhere to the following rules:

1. All parameters must be documented, refer to the examples below on the precise format.

2. All parameters must sit in a key-value hierarchy that semantically makes sense and can be understood by the diversity of users that use LDAR-Sim.

3. All parameter files require `parameter_level` to define the position within the hierarchy.

4. If adding new functionality - The version change associated with the change in functionality must be a Major or Minor version change, accompanied by a software release. This allows for users to download and run the version compatible with legacy parameters if required in the future. Any parameters changed or removed must be documented in Legacy Parameters in the user manual. Developers should aim to support backwards compatibility wherever reasonable.

5. Please do not modify parameters in the program during simulation - consider parameters as 'read only' throughout the simulation.

--------------------------------------------------------------------------------

## 2\. Introduction

To reduce fugitive methane emissions from the oil and gas (O&G) industry, companies implement leak detection and repair (LDAR) programs across their asset base. Traditionally, regulators have specified the use of close-range methods such as the U.S. Environmental Protection Agency's (EPA) Method 21 or Optical Gas Imaging (OGI) cameras for component-level surveys in LDAR programs. These methods remain widely approved by regulators and are effective, however, they are also time consuming and labor intensive. New methane detection and measurement technologies that incorporate satellites, aircraft, drones, fixed sensors, and vehicle-based systems have emerged that promise to deliver faster and more cost-effective LDAR. Before applying these technologies and their work practices in LDAR programs, operators and regulators may wish to estimate anticipated emissions reductions and costs. Regulators often require demonstration of equivalence – that the proposed alternative will achieve at least the same emissions reductions as incumbent regulatory methods. To support this process, the Leak Detection and Repair Simulator (LDAR-Sim) was developed at the University of Calgary to evaluate the emissions reduction potential of alternative LDAR programs.

LDAR-Sim is a computer model that simulates an asset base of oil and gas facilities, the emissions they produce, and the work crews that use different technologies and methods to find and repair leaks. LDAR-Sim replicates the complex reality of LDAR in a virtual world and allows users to test how changes to facilities or the applications of different technologies and methods might affect emissions reductions and LDAR program costs.

To support wider use of LDAR-Sim, the University of Calgary and Highwood Emissions Management have partnered to expand the model's capabilities and stakeholder accessibility through the IM3S Project. This document describes how to use LDAR-Sim and details the model's input data definitions, requirements, and formats. For each input parameter, the data type, defaults, and a detailed description are provided, as well as additional information about data acquisition and limitations. The parameter list comprises general inputs such as weather, leak rates, and facility coordinates, as well as those specific to individual close-range and screening methods like cost-per-day and follow-up thresholds. All inputs, whether empirical distributions or Boolean logic, are customizable. Recommended defaults are described.

By detailing the model inputs, this report creates the technical foundation for adding new functionality and enabling wider use of the model. This document will be revised continuously as modules, inputs, and functionality are added to or removed from LDAR-Sim.

--------------------------------------------------------------------------------

## 3\. File Structure

_TODO_ update when structure is finalized

The LDAR-Sim software is organized using the following structure:

- Root(LDAR_Sim)
  - inputs
  - install
  - outputs
  - src
  - simulations
  - external_sensors

- CHANGELOG.md
- ParameterMigrationGuide.md
- LICENSE.txt
- README.md
- USER_MANUAL.md
- INSTALL_GUIDE.md

The **Root** folder includes all code, inputs, and outputs necessary to run LDAR-Sim. From a software perspective, the root folder is the parent to the src folder (folder containing LDAR_sim_main). This folder will be always be the root folder when making relative references in LDAR-Sim. For example, if input_directory is specified as _./inputs_ from anywhere in the code, the targeted folder will be _{absolute_path_to} / Root / inputs_.

The **inputs** folder contains input files required to run LDAR-Sim. These include weather files, empirical leak and vent data, facility lists, and other inputs.

The **outputs** folder stores all output data files produced by LDAR-Sim. The folder is cleaned, and added if required each time ldar_sim_main is run.

The **src** folder stores the python source code. The main code of LDAR-Sim, LDAR_sim_main.py is stored in the base folder of src.

The **external_sensors** folder contains python source code for alternative technology sensors that users are free to use and add to.

The **simulations** stores sample V4.0 input parameter files.

--------------------------------------------------------------------------------

To set up the model, follow the [installation guide](INSTALL_GUIDE.md) provided.

--------------------------------------------------------------------------------

To run the model, supply one or more input parameter files as arguments to the program. The main function is called `ldar_sim_run.py` and is the main entrypoint to the model. File paths can be relative to the root directory (e.g., `./parameter_file1.yaml`) or absolute (e.g., `D://parameter_files//parameter_file1.yaml`). File paths are positional arguments and should be separated by a single space.

```buildoutcfg
python ldar_sim_run.py parameter_file1.yaml parameter_file2.yaml
```

Alternatively, a single folder name (absolute or relative to root) can be passed by flagged argument _-P_ or _--in_dir_. All json or yaml files within that folder will be added as parameter_files. For example, the following will use all parameter files within the sample simulation folder:

```buildoutcfg
python ldar_sim_run.py --in_dir ./simulations
```

We recommend running the model with a working directory set to /LDAR_Sim/src.

Optionally, a single folder name (absolute or relative to root) can be passed by flagged argument _-X_ or _--out_dir_. All output files will be added as outputs in that directory. For example, the following will save all output files within the "out" folder:

```buildoutcfg
python ldar_sim_run.py --in_dir ./simulations --out_dir ./out
```

--------------------------------------------------------------------------------

## 4\. Introducing Parameter Files

Parameter files are all key-value pairs (i.e., Python dictionary), with multiple levels of nesting. The model runs with 4 main levels in a hierarchy:

- `simulation setting`: global simulation setting parameters that are common across all programs in a simulation or set of simulations such as system parameters, etc.
- `virtual world`: virtual world parameters that are used to create the virtual world which the different emissions reduction programs are applied to.
- `program`: program parameters that are used to define a specific emissions reduction program (or lack thereof). Commonly, an 'alternative' custom program is compared to a defined regulatory program. Many programs can be compared at once.
- `method`: emissions reduction methods (e.g., specific LDAR technologies and work practices and/or LDAR service provider companies) that are deployed within a program. Methods are specified in a given program for deployment and multiple methods may be used at once (e.g., satellite + aircraft + OGI follow-up + routine AVO)

A typical simulation would compare at least two programs: a reference program and one or more test programs. Including a baseline program is also necessary.

- `baseline program`: The program against which mitigation is estimated for reference and test programs (mitigation = baseline emissions - LDAR emissions). Typically involves running LDAR-Sim in the absence of a formal LDAR program (commonly denoted as 'P_none'). Even without a formal LDAR program, leaks are eventually removed from the simulation due to operator rounds (e.g., AVO), routine maintenance, refits and retrofits, or other factors.
- `reference program`: The program against which test programs are compared (e.g., to establish equivalency). The reference program is often defined by regulations that require the use of OGI (commonly denoted 'P_OGI').
- `test programs`: A custom alternative program that the user wants to evaluate. Commonly denoted using 'P_' + program name (e.g., 'P_aircraft', 'P_GasCompanyX', 'P_drone', etc.).

A simulation can consist of any number of programs and each program can consist of any number of methods. For example, the reference program could deploy one method (OGI). The test program could deploy two new LDAR methods (magical helicopter and un-magical binoculars). Each program would be run on the asset base multiple times through time to create a statistical representation of the emissions and cost data. Finally, the statistical emissions and cost distributions of the reference program can be compared to those of the test program. It is often the differences between the programs that represents the important information that is of interest to users of LDAR-Sim.

In this example, the hierarchy looks like:

```yaml
Simulation setting parameters
Virtual world parameters
Programs:
    Baseline program
    Reference program:
        Reference LDAR method (OGI)
    Test program:
        New LDAR method 1 (Magical Helicopter)
        New LDAR method 2 (Un-magical Binoculars)
```

--------------------------------------------------------------------------------

### Parameter file usage

We recommend supplying LDAR-Sim with a full set of parameters, copied from the default parameters in the `default_parameters` folder and modified for your purposes. This will ensure you are familiar with the parameters you have chosen to run the model.

However, it may be more convenient once you are familiar with how parameter files update each other to use multiple parameter files to create your simulations and rely upon the default parameters.

All simulations using multiple parameter files are created the following way:

_TODO_ Possibly insert the data flow chart here?

--------------------------------------------------------------------------------

### Parameter Hierarchy

As noted previously, LDAR-Sim usues a 4 level hierarchy of simulations, virtual world, programs and methods parameters. To tell LDAR_Sim what level in the hierarchy your parameter file is destined for, you must specify a `parameter\_level` parameter that will specify what level your paremeter file is aimed at.

The `parameter_level` parameter can be one of three values:

- `simulation_settings`: parameters are aimed at the simulation setting level.
- `virtual_world`: parameters are used to define the virtual world.
- `program`: parameters are used to define a program.
- `method`: parameters are used to define a method and update a given method by name.

--------------------------------------------------------------------------------

### Versioning of Parameter Files

All parameter files must specify a version to enable mapping. This versioning is used to allow code to verify that a compatible version of the parameters is being used. If the parameter version is incompatible, the software will output an error message with further instructions on where to find guidance on input parameter mapping to the latest version.

Refer to `input_mapper_v1.py` for a template file and discussion document on input parameter mapping from V1.0 to V2.0.

Refer to [ParameterMigrationGuide](ParameterMigrationGuide.md) for instructions on how to migrate parameters from v2.x.x to V3.0 and from V3.0 to V4.0. Reverse compatibility mapping only exists for minor parameter versions within the same major LDAR-Sim version (For example LDAR_Sim version 3.0 is not compatible with version 2.x.x parameters).

--------------------------------------------------------------------------------

### Parameter File Formats

LDAR-Sim includes a flexible input parameter mapper that accepts a variety of input parameter formats. Choose the one that you like the best. [YAML](https://en.wikipedia.org/wiki/YAML) is the easiest to read for humans, allows inline comments, and is recommended.

The following formats are accepted:

- yaml files (extension = '.yaml' or '.yml')
- json files (extension = '.json')

For example, here is a program definition in yaml:

```buildoutcfg
version: '4.0'
parameter_level: program
name: awesome_program
```

Here is the same program definition in json:

```buildoutcfg
{
    "version": "4.0",
    "parameter_level": "program",
    "name": "awesome_program"
}
```

Note that programs are interpreted as a flat list of parameters that are incorporated into a list where methods have one parameter (the method name), and other method parameters nested below.

--------------------------------------------------------------------------------

## 5\. Simulation Settings

### &lt;parameter_level&gt; (simulation_settings)

**Data Type:** String

**Default input:** 'simulation_settings'

**Description:** A string indicating the parameters in file are at the simulation settings level

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be set to ```parameter_level: simulation_settings``` for a simulation setting parameter file.

### &lt;version&gt; (simulation_settings)

**Data type:** String

**Default input:** 4.0

**Description:** Specify version of LDAR-Sim. See section _[Versioning of Parameter Files](#versioning-of-parameter-files)_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** Improper versioning will prevent simulator from executing.

### &lt;input_directory&gt;

**Data type:** String

**Default input:** "./inputs"

**Description:** Specifies the folder/directory containing virtual world defining files like the[emissions_file](#emissions_file), [sites_file](#sites_file), etc. Accepts either an absolute path or a relative path from the root folder.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### &lt;output_directory&gt;

**Data type:** String

**Default input:** './outputs'

**Description:** Specifies the folder/directory to generate output files into. Accepts either an absolute path or a relative path from the root folder.

**Notes on acquisition:** It is recommended for the `output_directoy` be specified for each simulation that is ran.

**Notes of caution:** The contents of the existing folder is **removed** and **overwritten**. Rename folders to ensure that old output files are not lost.

### &lt;baseline_program&gt;

**Data type:** String

**Default input:** 'P_none'

**Description:** Refers to a [name of a program](#program_name) that is a part of the simulation. Results requiring a reference point for comparison, such as mitigation efforts, will be derived by comparing the output values from this program.

**Notes on acquisition:** Typically a program that represents a scenario where there is no formal LDAR or that has no LDAR method is recommended as the baseline program. Simply put, create a program with no methods.

**Notes of caution:** A baseline program is required to successfully run the simulation.

### &lt;reference_program&gt; WIP

**Data type:** String

**Default input:** 'P_OGI'

**Description:** Refers to a [name of a program](#program_name), against which alternative programs are compared.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### &lt;processes_count&gt;

**Data type:** Integer (Numeric)

**Default input:** 6

**Description:** The maximum number of parallel tasks or processes that the simulator can use simultaneously. To simplify, this is the limit of how many different tasks the simulator can handle at a given time.

**Notes on acquisition:** In general, many modern computers can effectively handle around 6 concurrent processes without significant performance issues. This number is influenced by factors such as the computer's hardware specifications, operating system efficiency, and the resource demands of the individual processes.

**Notes of caution:** Python is limited and cannot achieve true simultaneous execution of Python code. Therefore, generating too many processes may cause slower performance due to excessive context switching between the different processes.

A minimum of a single process is required for the simulation to run.

### &lt;simulation_count&gt;

**Data type:** Integer (Numeric)

**Default input:** 2

**Description:** The number of simulation rounds to execute for the given programs.

**Notes on acquisition:** Increasing the number of simulations improves result accuracy but extends the runtime.

**Notes of caution:** For critical scenarios that are intended to guide decision-making, we recommend running a significant number of simulations for each modeled scenario. A minimum of 50 simulations is advised to ensure a robust comparison of different LDAR programs.

To generate meaningful and reliable data output from the simulator, it's important to aim for a substantial number of annual data points. We recommend aiming for at least 400 annual data points. This can be achieved by adjusting the number of simulation iterations and the duration of the simulations. For instance, you could run 100 iterations of a 4-year-long simulation. Alternatively, you can employ any combination that suits your specific needs, as long as it results in a sufficient number of data points.

### &lt;preseed_random&gt;

**Data type:** Boolean

**Default input:** False

**Description:** If enabled, a series of random integers, acting as the 'seed', will be generated. These integers guarantee the reproducibility of all randomly generated values. For instance, future simulations utilizing the same virtual world parameters alongside the specified 'seed' will produce identical emission sets.

**Notes on acquisition:** N/A

**Notes of caution:** It is advisable to set `preseed_random: True` for any simulation results that will require referencing and duplication in the future.

--------------------------------------------------------------------------------

## 6\. Output Settings

### &lt;parameter_level&gt; (outputs)

**Data Type:** String

**Default input:** 'outputs'

**Description:** A string indicating the parameters in file are at the output settings level

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be set to ```parameter_level: outputs``` for an output setting parameter file.

### &lt;version&gt; (outputs)

**Data type:** String

**Default input:** 4.0

**Description:** Specify version of LDAR-Sim. See section _[Versioning of Parameter Files](#versioning-of-parameter-files)_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** Improper versioning will prevent simulator from executing.

_TODO_

--------------------------------------------------------------------------------

## 7\. Virtual World Setting

--------------------------------------------------------------------------------

## 8\. Program Inputs

Content for the "Program Inputs" section goes here.

--------------------------------------------------------------------------------

## 9\. Method Inputs

Content for the "Method Inputs" section goes here.

--------------------------------------------------------------------------------

## 10\. Virtual World Defining Files

Content for the "Virtual World Defining Files" section goes here.

--------------------------------------------------------------------------------

## 11\. Legacy Inputs

As LDAR-Sim continues to advance, certain parameters may become obsolete and consequently removed from the current version. This section will comprehensively list such parameters, along with the version in which they were removed and, if applicable, their replacements.

--------------------------------------------------------------------------------

### Simulation Settings Parameters

#### &lt;pregenerate_leaks&gt;

- Removed as of version 4.0.0

As of v4.0 to ensure a fair comparison of programs, the functionality to compare programs with differing emission levels has been omitted, ensuring a standardized evaluation across all programs.

#### &lt;print_from_simulation&gt;

- Removed as of version 4.0.0

#### &lt;outputs&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;site_visits&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;leaks&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;sites&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;timeseries&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;plots&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;batch_reporting&gt;

- Removed as of version 4.0.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

#### &lt;make_plots&gt;

- Removed as of version 3.2.0

Version 4.0.0 introduces the new [Output Parameter defaults](#6-output-settings), offering a more detailed version of this feature.

--------------------------------------------------------------------------------

### Virtual World Settings Parameters

#### &lt;consider_venting&gt;

- Removed as of version 4.0.0

This feature has been removed due to the implementation of non-repairable emissions.

#### &lt;weather_is_hourly&gt;

- Removed as of version 4.0.0

This feature may be re-implemented in the future, however with the initial update, all weather is averaged per day.

#### &lt;infrastructure_file&gt;

- Removed as of version 4.0.0

This parameter has been replaced with [sites_file](#sites_file).

#### &lt;subtype_file&gt;

- Removed as of version 4.0.0

This parameter has been replaced with [site_type_file](#site_type_file).

#### &lt;leak_dist_params&gt;

- Removed as of version 4.0.0

As of version 4.0.0, this parameter has been moved into the [emissions_file](#emissions_file).

#### &lt;leak_dist_type&gt;

- Removed as of version 4.0.0

As of version 4.0.0, this parameter has been moved into the [emissions_file](#emissions_file).

#### &lt;leak_file&gt;

- Removed as of version 4.0.0

As of version 4.0.0, the function of this file has been replaced by the [emissions_file](#emissions_file).

#### &lt;leak_file_use&gt;

- Removed as of version 4.0.0

As of version 4.0.0, this parameter has been moved into the [emissions_file](#emissions_file).

#### &lt;max_leak_rate&gt;

- Removed as of version 4.0.0

As of version 4.0.0, this parameter has been moved into the [emissions_file](#emissions_file).

#### &lt;units&gt;

- Removed as of version 4.0.0

As of version 4.0.0, this parameter has been moved into the [emissions_file](#emissions_file).

#### &lt;n_init_leaks_prob&gt;

- Removed as of version 4.0.0

#### &lt;n_init_days&gt;

- Removed as of version 4.0.0

#### &lt;subtype_leak_dist_file&gt;

- Removed as of version 3.0.0

Version 4.0.0 revamped the organization of all emissions-related values, consolidating them within the [emissions_file](#emissions_file).

#### &lt;subtype_times_file&gt;

- Removed as of version 2.4.0

#### &lt;vent_file&gt;

- Removed as of Version 2.1.2

--------------------------------------------------------------------------------

## 12\. Data sources, modelling confidence and model sensitivity

There are a broad range of inputs used in LDAR-Sim that must be derived from various sources. Each of these parameters should be carefully considered and understood before using LDAR-Sim to inform decision making. Like other models, the quality of simulation results will depend on the quality and representativeness of the inputs used.

The sensitivity of modeling results to inputs will vary on a case-by-case basis. In general, it is best to assume that all parameters in LDAR-Sim are important before modeling begins. It is strongly recommended to perform sensitivity analyses each time LDAR-Sim is used in order to understand the impact that uncertainty in inputs might have on results. Each LDAR program is unique in many ways. Therefore, there is no universal set of rules or guidelines to indicate _a priori_ which parameters will have the greatest impact on results.

In the same way, the confidence in the accuracy of input data can only be determined by the user who provides the data. For example, if provided an empirical leak-size distribution consisting of only 5 measurements, LDAR-Sim will run and generate results without generating warnings. It is the responsibility of the user to have sufficient experience to understand how LDAR-Sim processes different types of data so that they can confidently provide high quality inputs.

In terms of data source, inputs can come from oil and gas companies, technology providers, or solution providers. Some parameters and inputs can also be sourced from peer reviewed literature or can be used simply as experimental levers to explore different scenarios within LDAR-Sim. The lists below provide a general overview of what stakeholders will _generally_ be responsible for different parameters and inputs. Exceptions will always exist, and may vary according to the purpose of modeling, the jurisdiction, and the scope of the modeling exercise. In general, we strongly suggest deriving method performance metrics from single-blind controlled release testing experiments.

Below are some examples of common sources of LDAR-Sim data. Not all parameters are covered. In the absence of operator-specific data, published estimates can be used.

### Duty Holder / Operator (historical LDAR data)

- [emissions_file](#emissions_file)*
- [LPR](#lpr)*

### Duty Holder / Operator (organizational data)

- [sites_file](#sites_file) (ID, lat, long)
- [repair_cost](#repairs)*
- [repair_delay](#repairs)*

### Technology / Solution Provider / Operator (if self-performing LDAR)

_TODO_ fill out later

- OGI – n_crews, min_temp_, max_wind_, max_precip_, min_interval, max_workday, cost_per_day_, reporting_delay, MDL* , consider_daylight
- Screening Methods – n_crews, [various weather and operational envelopes]_, min_interval, max_workday, cost_per_day_, reporting_delay, MDL_, consider_daylight, follow_up_thresh, follow_up_ratio, QE_
- Fixed sensor – same as screening methods & up_front_cost, time to detection

### Modeling Expert

- [weather_file](#weather_file)

--------------------------------------------------------------------------------

## 13\. References

Fox, Thomas A., Mozhou Gao, Thomas E. Barchyn, Yorwearth L. Jamin, and Chris H. Hugenholtz. 2021\. "An Agent-Based Model for Estimating Emissions Reduction Equivalence among Leak Detection and Repair Programs." _Journal of Cleaner Production_, 125237\. <https://doi.org/10.1016/j.jclepro.2020.125237>.

Ravikumar, Arvind P., Sindhu Sreedhara, Jingfan Wang, Jacob Englander, Daniel Roda-Stuart, Clay Bell, Daniel Zimmerle, David Lyon, Isabel Mogstad, and Ben Ratner. 2019\. "Single-Blind Inter-Comparison of Methane Detection Technologies–Results from the Stanford/EDF Mobile Monitoring Challenge." _Elem Sci Anth_ 7 (1).

Ravikumar, Arvind P., Jingfan Wang, Mike McGuire, Clay S. Bell, Daniel Zimmerle, and Adam R. Brandt. 2018\. "Good versus Good Enough? Empirical Tests of Methane Leak Detection Sensitivity of a Commercial Infrared Camera." _Environmental Science & Technology_.

Zimmerle, Daniel, Timothy Vaughn, Clay Bell, Kristine Bennett, Parik Deshmukh, and Eben Thoma. 2020\. "Detection Limits of Optical Gas Imaging for Natural Gas Leak Detection in Realistic Controlled Conditions." _Environmental Science & Technology_ 54 (18): 11506–14.

