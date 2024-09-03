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
  - [5. Simulation Settings](#5-simulation-settings)
  - [6. Output Settings](#6-output-settings)
  - [7. Virtual World Setting](#7-virtual-world-setting)
  - [8. Program Inputs](#8-program-inputs)
  - [9. Method Inputs](#9-method-inputs)
  - [10. Virtual World Defining Files](#10-virtual-world-defining-files)
    - [Sites File](#sites-file)
    - [Site Type File](#site-type-file)
    - [Equipment File](#equipment-file)
    - [Source File](#source-file)
    - [Emissions File](#emissions-file)
  - [11. Legacy Inputs](#11-legacy-inputs)
    - [Legacy Simulation Settings Parameters](#legacy-simulation-settings-parameters)
    - [Legacy Virtual World Settings Parameters](#legacy-virtual-world-settings-parameters)
  - [12. Data sources, modelling confidence and model sensitivity](#12-data-sources-modelling-confidence-and-model-sensitivity)
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

The LDAR-Sim software is organized using the following structure:

- Root
  - Benchmarking
  - doc-images
  - Guides
    - Feature Guides
    - Version Migration Guides
  - install
  - LDAR_Sim
    - inputs
    - outputs
    - simulations
    - src
      - default_parameters
      - ldar_sim_run.py
      - ldar_sim_sensitivity_analysis.py
    - testing

  - CHANGELOG.md
  - INSTALL_GUIDE.md
  - LICENSE.txt
  - ParameterMigrationGuide.md
  - README.md
  - USER_MANUAL.md

The **Root** folder includes all LDAR-Sim related content.

The **Benchmarking** folder is a dev specific folder for benchmarking results.

The **doc-images** folder contains all images used in the different documents and guides for LDAR-Sim.

The **Guides** folder contains all other guides and documents and guides for LDAR-Sim.

The **Feature Guides** folder contains guides and documentation on specific features.

The **Version Migration Guides** folder contains guides for version migrations.

The **install**  folder contains the YAML files necessary for setting up the Conda environment required to run LDAR-Sim.

The **LDAR-Sim** folder contains all the files related to the simulation, including the actual source code and various parameter/input files.

The **inputs** folder is the default folder that contains virtual world defining files required to run LDAR-Sim. These include weather files, empirical emission data, facility lists, and more.

The **outputs** folder is the default folder that stores all output data files produced by LDAR-Sim. The folder is cleaned, and added if required each time the ldar_sim_run script is executed. Users can set the [outputs](#output_directory) to change the location.

The **simulations** stores sample input parameter files.

The **src** folder stores the python source code. The main script to run LDAR-Sim, ldar_sim_run.py is stored in the base folder of src, in addition to the script to run the sensitivity analysis, ldar_sim_sensitivity_analysis.py.

The **default_paramters** file contained within the _src_ folder contains all the default parameters utilized by LDAR-Sim.

The **testing** folder is a development-specific directory that contains resources for end-to-end testing as well as all unit tests.

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

A typical simulation would compare at least two programs: a baseline program and one or more test programs.

- `baseline program`: The program against which mitigation is estimated for test programs (mitigation = baseline emissions - LDAR emissions). Typically involves running LDAR-Sim in the absence of a formal LDAR program (commonly denoted as 'P_none'). Even without a formal LDAR program, emissions are eventually removed from the simulation due to operator rounds (e.g., AVO), routine maintenance, refits and retrofits, or other factors.
- `test programs`: A custom alternative program that the user wants to evaluate. Commonly denoted using 'P_' + program name (e.g., 'P_aircraft', 'P_GasCompanyX', 'P_drone', etc.).

A simulation can consist of any number of programs and each program can consist of any number of methods. For example, the test program 1 could deploy one method (OGI). The test program 2 could deploy two new LDAR methods (magical helicopter and un-magical binoculars). Each program would be run on the asset base multiple times through time to create a statistical representation of the emissions and cost data. Finally, the statistical emissions and cost distributions of the baseline program can be compared to those of the test program. It is often the differences between the programs that represents the important information that is of interest to users of LDAR-Sim.

In this example, the hierarchy looks like:

```yaml
Simulation setting parameters
Virtual world parameters
Programs:
    Baseline program
    Test program:
        New LDAR method 1 (Magical Helicopter)
        New LDAR method 2 (Un-magical Binoculars)
```

--------------------------------------------------------------------------------

### Parameter file usage

We recommend supplying LDAR-Sim with a full set of parameters, copied from the default parameters in the `default_parameters` folder and modified for your purposes. This will ensure you are familiar with the parameters you have chosen to run the model.

--------------------------------------------------------------------------------

### Parameter Hierarchy

As noted previously, LDAR-Sim uses a 4 level hierarchy of simulations, virtual world, programs and methods parameters. To tell LDAR_Sim what level in the hierarchy your parameter file is destined for, you must specify a `parameter\_level` parameter that will specify what level your parameter file is aimed at.

The `parameter_level` parameter can be one of three values:

- `simulation_settings`: parameters are aimed at the simulation setting level.
- `virtual_world`: parameters are used to define the virtual world.
- `program`: parameters are used to define a program.
- `method`: parameters are used to define a method and update a given method by name.

In addition to the parameter hierarchy, LDAR-Sim requires several csv files to provide the properties of the virtual world, such as the individual site's ID, latitude, and longitude values. These files will be covered in further detail in the [virtual world defining files](#10-virtual-world-defining-files).

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

**Notes on acquisition:** It is recommended for the `output_directory` be specified for each simulation that is ran.

**Notes of caution:** The contents of the existing folder is **removed** and **overwritten**. Rename folders to ensure that old output files are not lost.

### &lt;baseline_program&gt;

**Data type:** String

**Default input:** 'P_none'

**Description:** Refers to a [name of a program](#program_name) that is a part of the simulation. Results requiring a reference point for comparison, such as mitigation efforts, will be derived by comparing the output values from this program.

**Notes on acquisition:** Typically a program that represents a scenario where there is no formal LDAR or that has no LDAR method is recommended as the baseline program. Simply put, create a program with no methods.

**Notes of caution:** A baseline program is required to successfully run the simulation.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### &lt;processes_count&gt;

**Data type:** Numeric (Integer)

**Default input:** 6

**Description:** The maximum number of parallel tasks or processes that the simulator can use simultaneously. To simplify, this is the limit of how many different tasks the simulator can handle at a given time.

**Notes on acquisition:** In general, many modern computers can effectively handle around 6 concurrent processes without significant performance issues. This number is influenced by factors such as the computer's hardware specifications, operating system efficiency, and the resource demands of the individual processes.

**Notes of caution:** Python is limited and cannot achieve true simultaneous execution of Python code. Therefore, generating too many processes may cause slower performance due to excessive context switching between the different processes.

A minimum of a single process is required for the simulation to run.

### &lt;simulation_count&gt;

**Data type:** Numeric (Integer)

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

The output parameter file is a configuration file used to manage the activation (`true`) or deactivation (`false`) of specific outputs. By modifying this file, users can control which outputs are generated based on their particular needs. This is particularly useful when users only require specific outputs, allowing them to streamline the process and potentially improve performance by disabling unnecessary outputs.

It is strongly recommended to use the default settings provided. These settings are optimized for general use and ensure that all necessary outputs are correctly generated without any issues.

It is important to understand that certain outputs are interdependent. Disabling an output that serves as a dependency for another may cause errors or unexpected behavior. Therefore, users should be cautious and ensure they have a thorough understanding of these dependencies before making changes.

### Output Settings of Note

#### Keep All Program Outputs

By default, LDAR-Sim only keep the results of the first 5 simulations for each program. Changing this setting to true will result in LDAR-Sim keeping program results for all simulations.

**Warning** It is not recommended to run a large number of simulations with this setting set to true as this will result in a significant amount of output files being kept, potentially filling up a users filesystem.

--------------------------------------------------------------------------------

## 7\. Virtual World Setting

### &lt;parameter_level&gt; (virtual_world)

**Data Type:** String

**Default input:** 'virtual_world'

**Description:** A string indicating the parameters in file are at the virtual world level

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be set to ```parameter_level: virtual_world``` for a virtual world parameter file.

### &lt;version&gt; (virtual world)

**Data type:** String

**Default input:** 4.0

**Description:** Specify version of LDAR-Sim. See section _[Versioning of Parameter Files](#versioning-of-parameter-files)_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** Improper versioning will prevent simulator from executing.

### &lt;start_date&gt;

**Data type:** List of integers [year, month, day]

**Default input:** [2023,1,1]

**Description:** The date at which the simulations begins.

**Notes on acquisition:** We recommend running the simulation for several years due to the stochastic nature of LDAR systems and the periods of time over which leaks arise and are repaired.

**Notes of caution:** A start date not on January 1st of a given year may cause error with the calculation of annual summary statistics.

### &lt;end_date&gt;

**Data type:** List of integers [year, month, day]

**Default input:** [2027,12,31]

**Description:** The date at which the simulations ends.

**Notes on acquisition:** We recommend running the simulation for several years due to the stochastic nature of LDAR systems and the periods of time over which leaks arise and are repaired.

**Notes of caution:** An end date not on December 31st of a given year may cause error with the calculation of annual summary statistics.

### &lt;infrastructure&gt;

**Description:** This parameter does not require user input. It serves to provide a more comprehensive categorization for parameters that specify the files used to construct the virtual world.

#### &lt;sites_file&gt;

**Data Type:** String

**Default input:** None

**Description:** This parameter is defined by a string specifying the name of the CSV file containing data on the sites participating in the simulation. It is a **mandatory** file that must, at a minimum, include unique site IDs, latitude and longitude values, along with corresponding site types for each row.

**Notes on acquisition:** Refer to the section [Virtual World Defining Files](#10-virtual-world-defining-files) for comprehensive instructions on setting up this file.

**Notes of caution:** The number of unique sites provided in this file must be equal or greater than the [site_samples](#site_samples) parameter.

#### &lt;site_type_file&gt;

**Data type:** String

**Default input:** None

**Description:** This parameter is defined by a string that specifies the name of the CSV file containing data on the site types involved in the simulator. It's optional and aims to minimize the redundancy of repeatedly defining site types.

**Notes on acquisition:** Refer to the section [Virtual World Defining Files](#10-virtual-world-defining-files) for comprehensive instructions on setting up this file.

**Notes of caution:** The site types defined in this file must correspond to the values in the [sites_file](#sites_file). Refer to the [Virtual World Defining Files](#10-virtual-world-defining-files) for more details.

#### &lt;equipment_group_file&gt;

**Data Type:** String

**Default input:** None

**Description:** This parameter is defined by a string specifying the name of the CSV file containing data on the equipment in the simulation. It's an _optional_ file intended to refine site characteristics and minimize the need for redundant definitions of similar equipment. In simpler terms, the equipment file streamlines the process of defining granular sites by reducing the manual repetition required to define similar equipment multiple times.

**Notes on acquisition:** Refer to the section [Virtual World Defining Files](#10-virtual-world-defining-files) for comprehensive instructions on setting up this file.

**Notes of caution:** The equipment defined in this file must correspond to equipment defined in the [sites_file](#sites_file). Refer to the [Virtual World Defining Files](#10-virtual-world-defining-files) for more details.

#### &lt;sources_file&gt;

**Data Type:** String

**Default input:** None

**Description:** This parameter is determined by a string indicating the name of the CSV file containing information about the components and sources in the simulation. It's an _optional_ file that enables users to provide more detailed data regarding individual components and the types of sources associated with each component.

**Notes on acquisition:** Refer to the section [Virtual World Defining Files](#10-virtual-world-defining-files) for comprehensive instructions on setting up this file.

**Notes of caution:** The component and sources must correspond to the values found in the [equipment_group_file](#equipment_group_file) and [emissions_file](#emissions_file). Refer to the [Virtual World Defining Files](#10-virtual-world-defining-files) for more details.

### &lt;site_samples&gt;

**Data Type:** Numeric (Integer)

**Default input:** None

**Description:** This variable is an integer indicating the number of sites to be selected as a subset. It allows users to specify how many sites they want to include in their analysis or simulation.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** The number of site sampled must be equal to or less than the number of unique sites provided in the [sites_file](#sites_file).

### &lt;consider_weather&gt;

**Data type:** Boolean

**Default input:** False

**Description:** Specify whether weather envelopes will influence the selection of potential deployment sites for each method. If the weather on a given day falls outside the valid [weather envelopes](#weather_envelopes), crews for the respective method will not be deployed to the site on that day.

**Notes on acquisition:** N/A

**Notes of caution:** Even if weather is considered false, [weather_file](#weather_file) must be present and valid.

### &lt;weather_file&gt;

**Data type:** String

**Default input:** None

**Description:** Specifies the name of the ERA5 NetCDF4 file that contains all weather data to be used in the analysis. Generally, at a minimum, OGI requires wind, temperature, and precipitation data. LDAR-Sim reads in temperature data in degrees Celsius at 2 meters above ground, wind in meters per second at 10 meters above ground, and total precipitation in millimeters accumulated per hour. Other weather variables are freely available for download.

**Notes on acquisition:** Raw data are available from the European Centre for Medium-Range Weather Forecasts. Pre-processed and ready to use weather data have been prepared and are available for download on AWS for Alberta, Colorado, and New Mexico. LDAR-Sim will access these files directly if the file names are specified correctly in the program file. Currently available files are:

- Alberta: "ERA5_AB_1x1_hourly_2015_2019.nc"
- Colorado: "ERA5_CO_1x1_hourly_2015_2019.nc"
- New Mexico: "ERA5_NM_1x1_hourly_2015_2019.nc"

_TODO_ check if these work

In addition, the following files are included in the GitHub repository for generic weather data covering Canada or the United States, as well as specific data for Alberta, the Marcellus shale, and the Permian basin:

- "weather_alberta.nc"
- "weather_marcellus.nc"
- "weather_permian.nc"
- "ERA5_2020_2020_Canada_2xRes.nc"
- "ERA5_2020_2020_US_2xRes.nc"

Each of these files provides hourly weather (wind, temp, precipitation) data spanning the years specified at a spatial resolution of 1 degree latitude and 1 degree longitude. If custom configurations are needed for different regions, spatial resolutions, temporal resolutions, dates, or weather variables (e.g., clouds, snow cover, etc.), they must be downloaded manually from the ERA5 database. The 'ERA5_downloader' python file in the model code folder provides code and guidance for accessing custom weather data.

See [weather_readme](LDAR_Sim/src/weather/weather_readme.md) documentation for further details regarding weather in LDAR-Sim.

**Notes of caution:**

Weather file sizes can become quite large, especially when spatial and temporal resolution increase (maximum resolutions of 1.25 degrees and 1 hour, respectively). Modelers must decide how to navigate these tradeoffs, and understand the implications of the resolutions chosen.

### &lt;Repairs&gt;

**Description:** This parameter doesn't necessitate user-defined input. Its purpose is to offer a broader categorization for parameters that define the repair characteristics of the virtual world.

### &lt;cost&gt;(repairs)

**Description:** This parameter doesn't necessitate user-defined input. Its purpose is to offer a broader categorization for parameters that define the repair cost characteristics of the virtual world.

**Note:** The repair cost parameter can be specifically set at a more granular level through the [virtual world defining files](#10-virtual-world-defining-files).

#### &lt;values&gt; (cost) _(propagating parameter)_

**Data Type:** List of floats/numerics

**Default input:** [200]

**Description:** The cost associated with repairing repairable emissions.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#repairable_repair_cost-sites-file)
- [Site type File](#repairable_repair_cost-site-type-file)
- [Equipment File](#repairable_repair_cost-equipment-file)
- [Source File](#repair_cost-source-file)

**Notes on acquisition:** The duty holder should have data on cost of repairs.

**Notes of caution:**
Cost of repair is highly variable and not well characterized by a single value. For example, a percentage of leaks will have near-zero repair costs if it is just a matter of tightening a valve. Other repairs, especially if specialized equipment is involved, could be extremely expensive – especially if a shutdown is required and production declines, leading to indirect costs.

When specified in the virtual world parameter file, repair costs are independent of emission size or infrastructure. Moreover, these costs are still applicable even when emissions are terminated based on their maximum duration([duration](#duration-propagating-parameter)).

#### &lt;file&gt; (cost)

**Data Type:** String

**Default input:** None

**Description:** The string name of the csv file in which the repair cost values are stored, if it exists.

**Notes on acquisition:** N/A

**Notes of caution:**  It is assumed that this file is located in the same folder as the [infrastructure](#infrastructure) files.

### &lt;delay&gt;(repairs)

**Description:** This parameter doesn't necessitate user-defined input. Its purpose is to offer a broader categorization for parameters that define the repair delay characteristics of the virtual world.

**Note:** The repair delay parameter can be specifically set at a more granular level through the [virtual world defining files](#10-virtual-world-defining-files)

#### &lt;values&gt; (delay)_(propagating parameter)_

**Data Type:** List of integers/numerics, or string

**Default input:** [14]

**Description:** The number of days that pass between the end of a survey when a site is tagged for repairs and when the repairable emission(s) are fixed. This value can also be a column header in the [repair delays file](#file-delay) for sampling purposes.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#repairable_repair_delay-sites-file)
- [Site type File](#repairable_repair_delay-site-type-file)
- [Equipment File](#repairable_repair_delay-equipment-file)
- [Source File](#repair_delay-source-file)

**Notes on acquisition:** Get this information from the service provider.

**Notes of caution:**  When specified in the virtual world parameter file, repair delays are independent of emission size or infrastructure.

#### &lt;file&gt; (delay)

**Data Type:** String

**Default input:** None

**Description:** The string name of the file containing sample repair delays, if it exists.

**Notes on acquisition:** N/A

**Notes of caution:** It is assumed that this file is located in the same folder as the [infrastructure](#infrastructure) files.

### &lt;emissions&gt;

**Description:** This parameter doesn't necessitate user-defined input. Its purpose is to offer a broader categorization for parameters that define the emission characteristics of the virtual world.

#### &lt;emissions_file&gt;

**Data Type:** String

**Default input:** None

**Description:** This parameter specifies the name of the CSV file used to describe the emissions rate characteristics, such as the actual emission rates and the units. Please refer to the section [Virtual World Defining Files](#10-virtual-world-defining-files) for comprehensive instructions on setting up this file.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

#### &lt;Pre-Simulation Emissions&gt;

**Data Type:** Boolean

**Default input:** True

**Description:** This parameter specifies if LDAR-Sim should generate emissions existing before the start date of the simulation. When set to 'False,' emissions are not generated before the simulation's start date. By default, emissions are produced leading up to this date, based on their durations, enabling the system to model a state without LDAR.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### repairable_emissions / non_repairable_emissions

**Description:** These parameters do not require user-defined input. Its purpose is to provide a broader categorization for parameters that define the emission characteristics of the virtual world. The following sub-parameters:  `emissions_production_rate`, `emissions_rate_source`, `duration` and `multiple_emissions_per_source`, can be set for either repairable emissions and/or non-repairable emissions.

**Note:** Ensure to use the correct category before defining the emission characteristics.

**Notes of caution:** The following parameters for defining emissions can be specified at multiple levels of granularity. However, the values set will always be overwritten by the most granular level. For further details and a flowchart, please refer to the section[Virtual World Defining Files](#10-virtual-world-defining-files).

#### &lt;emissions_rate_source&gt; _(propagating parameter)_

**Data Type:** String

**Default input:** None

**Description:** The name of a column in the [emissions file](#emissions_file) that is used to define the row that parameterize the emissions characteristics of all the corresponding repairable or non-repairable emissions. This parameter will be overwritten by the equivalent value, when provided at a more granular scale in one of the [Virtual world defining files](#10-virtual-world-defining-files).

See the following files for examples on setting this value at a more granular level:

Repairable emissions:

- [Sites File](#repairable_emissions_rate_source-sites-file)
- [Site type File](#repairable_emissions_rate_source-site-type-file)
- [Equipment File](#repairable_emissions_rate_source-equipment-file)
- [Sources File](#emissions_rate_source-source-file)

Non-Repairable emissions:

- [Sites File](#non_repairable_emissions_rate_source-sites-file)
- [Site type File](#non_repairable_emissions_rate_source-site-type-file)
- [Equipment File](#non_repairable_emissions_rate_source-equipment-file)
- [Sources File](#emissions_rate_source-source-file)

**Notes on acquisition:** N/A

**Notes of caution:** The column headers are case sensitive.

Both [emissions production rate](#emissions_production_rate-propagating-parameter) and [emissions rate source](#emissions_rate_source-propagating-parameter) must be set for a given repairable or non-repairable emission. The simulator will error out if only one of the two values are provided.

#### &lt;emissions_production_rate&gt; _(propagating parameter)_

**Data Type:** Float (Numeric)

**Default input:** None

**Description:**  A numeric scalar representing the emissions production rate, for repairable or non-repairable emissions. New emissions are generated using a site-level empirical production rate if not specified at a more granular level. The emission production rate, if set at the virtual world setting parameter file only, is the probability that a new emission will arise, each day, for each site. The emission production rate encapsulates various factors contributing to emission occurrences, such as facility age, management practices, predictive maintenance, and random chance. By setting the emission production rate in the virtual world parameter file, a uniform production rate is applied across all facility types, production types, facility ages, etc., unless specified otherwise at a more detailed level. This parameter replaces the old leak production rate (LPR) from previous versions of LDAR-Sim, and for an extended discussion on this topic, see Fox et al. (2021).

See the following files for examples on setting this value at a more granular level:

Repairable emissions:

- [Sites File](#repairable_emissions_production_rate-sites-file)
- [Site type File](#repairable_emissions_production_rate-site-type-file)
- [Equipment File](#repairable_emissions_production_rate-equipment-file)
- [Sources File](#emissions_production_rate-source-file)

Non-Repairable emissions:

- [Sites File](#non_repairable_emissions_production_rate-sites-file)
- [Site type File](#non_repairable_emissions_production_rate-site-type-file)
- [Equipment File](#non_repairable_emissions_production_rate-equipment-file)
- [Sources File](#emissions_production_rate-source-file)

**Notes on acquisition:** While the "true" emissions production rate is elusive, it can be estimated by dividing the number of emissions found during an LDAR survey at a facility by the number of days that have passed since the previous LDAR survey at the same facility. If this is done for a large number of survey intervals at a large number of facilities, one should eventually converge on a representative estimate. When LDAR-Sim is used, operator-specific emissions production rate values should be estimated if sufficient data exist to do so.

**Notes of caution:**  Available techniques for estimating emissions production rate make a number of problematic assumptions. Ultimately, we have relatively poor data on the emissions production rate and the relationship between the _emission production rate_ and the [maximum duration](#duration-propagating-parameter) of emissions. Modeling results are extremely sensitive to the production rate. Given that the emissions production rate is elusive, we strongly recommend that a broad range of the emissions production rate value is evaluated in LDAR-Sim before any decisions are made. For more information, refer to discussions in the main text and supplementary information of Fox et al. (2021).

When the parameter [multiple emissions per source](#multiple_emissions_per_source-propagating-parameter) is set to False, it will affect the emission production rate observed in the simulation. In this scenario, new emissions won't be generated if there's already an existing emission for the specified [emission source](#emissions_rate_source-propagating-parameter).

Both [emissions production rate](#emissions_production_rate-propagating-parameter) and [emissions rate source](#emissions_rate_source-propagating-parameter) must be set for a given repairable or non-repairable emission. The simulator will error out if only one of the two values are provided.

#### &lt;duration&gt; _(propagating parameter)_

**Data Type:** Integer (Numeric)

**Default input:** 365

**Description:** The maximum duration of each emission in number of days. Represents emission removal from the emission pool due to routine maintenance, refits, retrofits, and other reasons.

See the following files for examples on setting this value at a more granular level:

Repairable emissions:

- [Sites File](#repairable_duration-sites-file)
- [Site type File](#repairable_duration-site-type-file)
- [Equipment File](#repairable_duration-equipment-file)
- [Sources File](#duration-source-file)

Non-Repairable emissions:

- [Sites File](#non_repairable_duration-sites-file)
- [Site type File](#non_repairable_duration-site-type-file)
- [Equipment File](#non_repairable_duration-equipment-file)
- [Sources File](#duration-source-file)

**Notes on acquisition:** Estimate from empirical data or use previously published value.

**Notes of caution:** This value is highly uncertain and likely depends on context. Sensitivity analyses should be used to explore the impact of different _duration_ values.

#### &lt;multiple_emissions_per_source&gt; _(propagating parameter)_

**Data Type:** Boolean

**Default input:** True

**Description:** Specifies whether an emission source can generate multiple emissions simultaneously. For instance, a flare that's unlit can't produce additional unlit emissions simultaneously.

See the following files for examples on setting this value at a more granular level:

Repairable emissions:

- [Sites File](#repairable_multiple_emissions_per_source-sites-file)
- [Site type File](#repairable_multiple_emissions_per_source-site-type-file)
- [Equipment File](#repairable_multiple_emissions_per_source-equipment-file)
- [Sources File](#multiple_emissions_per_source-source-file)

Non-Repairable emissions:

- [Sites File](#non_repairable_multiple_emissions_per_source-sites-file)
- [Site type File](#non_repairable_multiple_emissions_per_source-site-type-file)
- [Equipment File](#non_repairable_multiple_emissions_per_source-equipment-file)
- [Sources File](#multiple_emissions_per_source-source-file)

**Notes on acquisition:** Users are encouraged to undertake an exercise to assess whether it's logical for a particular source to generate multiple emissions simultaneously.

**Notes of caution:** When set to false, it's possible to observe lower [emission production rates](#emissions_production_rate-propagating-parameter) than what has been parameterized, as existing emissions inhibit the generation of new emissions.

--------------------------------------------------------------------------------

## 8\. Program Inputs

### &lt;parameter_level&gt; (programs)

**Data Type:** String

**Default input:** 'programs'

**Description:** A string indicating the parameters in file are at the program settings level

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be set to ```parameter_level: programs``` for an output setting parameter file.

### &lt;version&gt; (programs)

**Data type:** String

**Default input:** 4.0

**Description:** Specify version of LDAR-Sim. See section _[Versioning of Parameter Files](#versioning-of-parameter-files)_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** Improper versioning will prevent simulator from executing.

### &lt;program_name&gt;

**Data Type:** String

**Default input:** "default"

**Description:** The name of the program. Typical naming convention is to include "P_" before a name.

**Notes on acquisition:** N/A

**Notes of caution:** Each program must have a unique program name. If names are duplicated, they will override each other.

### &lt;method_labels&gt;

**Data Type:** List[strings]

**Default input:** []

**Description:** A list of the methods used within the program. For example, the following will use the aircraft and the OGI_FU methods:

```yaml
method_labels:
- aircraft
- OGI_FU
```

The following is an alternative format for the same example:

```yaml
method_labels: ["aircraft","OGI_FU"]
```

**Notes on acquisition:** N/A

**Notes of caution:** The method labels that are referenced must be identical to an existing [method_name](#method_name), it is case sensitive.

### &lt;economics&gt;

**Description** Economic values that are used to generate cost related figures.

#### &lt;global_warming_potential_CH4&gt;

**Data Type:** Numeric

**Default input:** 28.0

**Description:** GWP of 28 over a 100-year time period was chosen as a default input. The model uses this value to convert between CH4 and CO2e when required. This value can be changed to 84-86 over 20 years to explore the impact that GWP has on mitigation costs.

**Notes of acquisition:** This value is from [Chapter 8](https://www.ipcc.ch/site/assets/uploads/2018/02/WG1AR5_Chapter08_FINAL.pdf) in the IPCC's Assessment Report 5 from Working Group 1 page 714, 2018.

**Notes of caution:** Using a GWP of CH4 for a 20-year time period may dramatically change results but all options should be explored.

#### &lt;sale_price_of_natural_gas&gt;

**Data Type:** Numeric

**Default input:** 3.0

**Description:** The sale price of natural gas per million Btu which is used to calculate the potential value of gas sold when captured as part of an LDAR program. LDAR-Sim takes the difference in emissions from a baseline scenario and multiplies this by the price of natural gas.

**Notes of acquisition:** This value can be taken from local distribution companies or natural gas trading hubs (ex. [eia](https://www.eia.gov/dnav/ng/hist/rngwhhdm.htm)).

**Notes of caution:** The default value of $3/MMbtu is a conservative estimate and users of LDAR-Sim will see different cost/benefit and cost/mitigation results if the price of natural gas is changed.

It is important to note that LDAR-Sim internally converts KG of methane to MMBtu of natural gas equivalent based on assuming the natural composition of gas at 0.949, temperature of 15C, and 1 atm.

### &lt;duration_estimate&gt;

**Description:** The following parameters are used to estimate the total emission amount according to the specified program's work practices.

#### &lt;duration_factor&gt;

**Data Type:** Numeric

**Default input:** 1.0

**Description:** A decimal number representing the ratio of time since the last survey or screening at a given site, used to estimate the duration of a given measurement.

For example, a value of 0.6 means that 60% of the duration was assumed to be the greater emitting value, between the two measurement points, and 40% of the duration would be assuming the smaller of the measured emission.

By default(1.0), it assumes that the greater measured value has been emitting since the last measurement.

```txt
Scenario
- A given site was surveyed January 1st, and 31st.
- It recorded 0kg/day and 5kg/day for the respective dates.

If duration_factor is set to 0.5:
  - The estimated volume emitted would be calculated by the following
      ((31 - 1) * 0.5)days * 5kg/day + ((31 - 1) * 0.5) * 0kg/day= 75 kg

If duration_factor is set to 0.2:
  - The estimated volume emitted would be calculated by the following
      ((31 - 1) * 0.2)days * 5kg/day + ((31 - 1) * 0.8) * 0kg/day= 30 kg

If the duration_factor is set to 1:
  - The estimated volume emitted for the same period would be 
      ((31 - 1) * 1)days * 5kg/day = 150 kg

```

**Notes of acquisition:** N/A

**Notes of caution:** When using `duration_method: measurement-based` with a `stationary` method, the only valid duration factors are 0.0 and 1.0. Any values greater than 0.0 will be handled the same as setting the `duration_factor: 1.0` because LDAR-Sim operates at a day scale - any partial dates are rounded to the next date.

#### &lt;duration_method&gt;

**Data Type:** String

**Default input:** "measurement-based"

**Description:** A string that specifies how the program as a whole will estimate the total emissions measured.

**`component-based`**- Only component level measurement work practices will be considered for estimating total emissions.

For example, with a duration factor of 1, if a given program uses two mobile methods, `A` and `B`, where `A` is a component-level survey and `B` is a site-level screening:

- `A` surveys `site_1` on January 1st and 30th, finding an emission on the 30th.
- `B` surveys `site_1` on January 15th.

The emission would be estimated to have lasted since January 1st, as that is the last valid component-level measurement conducted.

**`measurement-based`**- All methods are considered valid for estimating the total emissions measured.

For example, with a duration factor of 1, if a given program uses two mobile methods, `A` and `B`, where `A` is a component-level survey and `B` is a site-level screening:

- `A` surveys `site_1` on January 1st and 30th, finding an emission on the 30th.
- `B` surveys `site_1` on January 15th.

The measured total site level emission rate on January 30th is assumed to have lasted since January 15th.

**Notes of acquisition:** Currently the two valid duration estimation methods are `component-based` and `measurement-based`.

**Notes of caution:** All emissions estimation in simulation is based on the assumption that technologies quantify emissions.

If an emission estimation results in a negative value due to considerations of repairable emissions, the simulator will automatically set this value to 0 for reporting purposes.

--------------------------------------------------------------------------------

## 9\. Method Inputs

**Note of caution:** There are two sets of valid method default parameters based on the [deployment type](#deployment_type) of the parameterized method. These can be found in the following files:

- m_default_mobile.yml - for `mobile` deployment
- m_default_stationary.yml - for `stationary` deployment

Users should ensure they populate the correct set of parameters according to the method's [deployment type](#deployment_type). Parameters that are mobile or stationary deployment specific, will be labeled with _(mobile parameter)_ or _(stationary parameter)_ respectively.

### &lt;parameter_level&gt; (methods)

**Data Type:** String

**Default input:** 'methods'

**Description:** A string indicating the parameters in file are at the methods settings level

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be set to ```parameter_level: methods``` for a methods setting parameter file.

### &lt;version&gt; (methods)

**Data type:** String

**Default input:** 4.0

**Description:** Specify version of LDAR-Sim. See section _[Versioning of Parameter Files](#versioning-of-parameter-files)_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** Improper versioning will prevent simulator from executing.

### &lt;method_name&gt;

**Data type:** String

**Default input:** _placeholder_str_ (Required to be set for each method added to program)

**Description:** A character string denoting the label of the method.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must match the label name specified in the program input parameter file, and any supplementary files, such as the infrastructure file. This is a case sensitive parameter. It is important to note that different programs can call the same method files, provided that the work practices and technology involved are parameterized identically.

### &lt;measurement_scale&gt;

**Data type:** String

**Default input:** _placeholder_str_ (Required to be set for each method added to program)

**Description:** A character string describing the measurements scale. Possible inputs are `"component"`, `"equipment"`, and `"site"`.

- `component` level measurement scale technologies are able to measure the sum of emissions at a given component
- `equipment` level measurement scale technologies are able to measure the sum of emissions at a given equipment of a site
- `site` level measurement scale technologies measure the sum of the emissions of a given site

The following figure shows a graphical representation:

![emissions_behavior](doc-images/emissions_behavior.png)

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Only component scale methods are able to tag emissions for repair.

### &lt;deployment_type&gt;

**Data type:** String

**Default input:** _placeholder_str_ (Required to be set for each method added to program)

**Description:** Methods are comprised of both a deployment type and a sensor type. The deployment type is a character string denoting the deployment type used in the method. For instance, `'mobile'` or `'stationary'`. Custom deployment types can be added and referenced here.

Valid deployment types:

- `mobile`: Agent moves between sites. Surveys occur when a site is "ready" for a survey and a crew is available to survey.
- `stationary`: Each site has one or more _fixed_ sensors. Surveys are carried out daily.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Certain parameters are mobile/stationary deployment specific, which will be labeled with the following _(mobile parameter)_ or _(stationary parameter)_.

### &lt;sensor&gt;

**Description:** The parameters within this section are for specifying the measurement technology utilized in the simulation.

#### &lt;type&gt;

**Data type:** String

**Default input:** "default"

**Description:** Methods are comprised of both a deployment type and a sensor type. the sensor type is a character string denoting the sensor used in the method. For instance, `'OGI_camera_zim'`,`'OGI_camera_rk'`, or `'default'`. The `'default'` sensor uses the minimum detection limit (MDL) as a threshold to detect emissions based on the measurement scale of the method. Custom sensors can be added and referenced here. Built in sensors are:

- `default`: Uses a simple threshold where the emission rate is based on the [measurement_scale](#measurement_scale), for example if `measurement_scale = site` then the site's total emissions will be considered measured if greater than the sensors MDL.
- `OGI_camera_rk`: Uses detection curve based on Ravikumar, 2018. Requires [measurement_scale](#measurement_scale) = `'component'`.
- `OGI_camera_zim`: Uses detection curve based on Zimmerle 2020. Requires [measurement_scale](#measurement_scale) = `'component'`.
- `METEC_no_wind`: Uses a detection curve formula based on a typical METEC report where wind is normalized.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### &lt;quantification_error&gt;

**Data type:** Numeric

**Default input:** 0

**Description:** The parameters within this section are for specifying the functionality of quantification error within the simulation.

##### &lt;quantification_parameters&gt;

**Data type:** List, either Numeric (List of Floats) or String (List of Strings)

**Default input:** [0.0, 0.0]

**Description:** Parameters informing how quantification error functionality model measurement of emissions rates.

- With the `default` or `uniform` quantification types, the expected input is two numbers: the lower and upper bounds of a 95% confidence interval of possible signed quantification percent error values.
- With the `sample` quantification type, the expected input is two strings (text) the filename of the csv to use (including file extension), followed by the column in the file to use. The column specified of the file specified is expected to contain a list of possible signed quantification percent error values.

_Illustrative Example:_
For all quantification types, quantification error is applied as follows:

- A quantification error of +60% will result in a rate at 100 kg/h being measured as 160 kg/h.
- A quantification error of -60% will result in a rate at 100 kg/h being measured as 40 kg/h

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish quantification error 95% confidence intervals or using sample with all recorded possible quantification errors. Given the amount of work required to collect this information, we recommend using historical estimates where possible.

**Notes of caution:** As facility-scale quantification error remains poorly constrained for LDAR screening methods, and likely depend on work practice, dispersion modeling, and environment, screening programs should be evaluated using a range of possible quantification errors. We recommend understanding exactly how quantification error works before making use of this functionality.

##### &lt;quantification_type&gt;

**Data type:** String

**Default input:** "default"

**Description:**  The quantification module to use for determining quantification error. The shape of the [quantification_parameters](#quantification_parameters) must be support by the selected quantification types.

Currently three quantification types are supported:

- `default`: Quantification Error is drawn from a normal distribution centered on the midpoint between the upper and lower bounds of the 95% confidence interval of possible signed quantification percent error values provided through the [quantification_parameters](#quantification_parameters). The distribution will use a standard deviation also calculated from the 95% confidence interval assuming the empirical rule (95% percent of all observations lie within two standard deviations of the mean).
- `uniform`: Quantification Error is drawn from a uniform distribution bounded by the upper and lower bounds of the 95% confidence interval of possible signed quantification percent error values provided through the [quantification_parameters](#quantification_parameters).
  
  Both `default` and `uniform` types expect a list of 2 floating point numbers: the upper and lower bounds of the 95% confidence interval of possible quantification error values as input for [quantification_parameters](#quantification_parameters).

- `sample`: Quantification Error is drawn randomly from a list of possible signed quantification percent error values read in from a column of a csv file specified through the [quantification_parameters](#quantification_parameters).

  **NOTE**: Users may develop and implement their own quantification modules. Further documentation to support this practice will be added in a later release.

**Notes on acquisition:** The user must decide the most appropriate assumption on the distribution of quantification error.

**Notes of caution:** Note that when providing a quantification_type of "default", the normal distribution will be centered on the midpoint between the upper and lower bounds of the 95% confidence interval of possible quantification error values provided through the [quantification_parameters](#quantification_parameters). This can lead to misrepresentation of the quantification bias if the shape of the range of quantification error is not perfectly normal.

#### &lt;minimum_detection_limit&gt; (default)

**Data type:** Numeric or List of integers

**Default input:** [0.01] (Should be set for each Method)

**Description:** Minimum detection limit of the screening method in grams per second. Probability curves or surfaces as a function of emission rate, wind speed, distance, etc. must be hard coded.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** A single value for MDL is used here, although a parameter list could be used that defines a sigmoidal probability of detection curve. These are examples and with more experimental data, probability of detection surfaces can be generated that can estimate detection probabilities as a function of numerous relevant variables (e.g., distance, wind speed, emission rate, etc.)

#### &lt;minimum_detection_limit&gt; (OGI_camera_rk)

**Data type:** List of floats

**Default input:** [0.01275, 0.00000278]

**Description:** A list of parameters [_xₒ_, σ] that define the minimum detection limit of OGI. The two parameters define a sigmoidal Gaussian cumulative probability function as described in Ravikumar et al. (2018), where _xₒ_ is the emission rate (in grams per second) at which 50% of emissions are detected (i.e., median detection limit), and σ is one standard deviation of  _xₒ_. The probability detection of an emission with OGI is calculated using a sigmoidal probability function:

$$
f = \frac{1}{(1+exp(-k(log(x)-log(x_0))))}
$$

where f = is the fraction of emissions detected, _x_ is the emission rate in grams of methane per hour, _xₒ_ is the median detection limit (f = 0.5) and _k_ is the steepness of the sigmoid curve. Ravikumar et al. (2018) found that at 3 m _k_ =  4.9 g/hr +/- 3, and _xₒ_ = 0.47 +/- 0.1. However, detection limits were found to be an order of magnitude higher in the Zimmerle study. As such, LDAR-Sim assumes an _xₒ_ of 0.01275 g/s. For reasons listed below, we note that this is likely a conservative estimate. Also, this approach assumes a constant distance of 3 meters from camera to source.

**Notes on acquisition:** If no input is provided for the minimum detection limit (`minimum_detection_limit: []`), the values [0.01275, 0.00000278] will be used for the constants.

We recommend extensive controlled release testing under a range of representative release rates and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** Detection probabilities for OGI cameras have been shown to vary with operator experience, wind speed, scene background, and other variables. Estimates from Ravikumar et al. (2018) are experimentally derived but are likely low because (i) the OGI inspector knew where to look, (ii) measurements were performed over only 1 week of good conditions, (iii) OGI cameras were tripod mounted, and (iv) videos were analyzed by experts after data collection. Estimates from Zimmerle et al. (2020) are an order of magnitude higher, and likely closer to reality. However, this estimate applies only to experienced inspectors with over 700 site inspections under their belts, so the true median detection across all inspectors may be lower. Furthermore, the Zimmerle study for experienced inspectors could still represent an underestimate as (i) weather conditions were relatively good, (ii) OGI inspectors were participating in a formal study and were likely very focused, and (iii) many of the emissions were odorized. These results would therefore not include laziness, neglect, or missing of emissions from difficult to access areas. See [minimum_detection_limit(default)](#minimum_detection_limit-default) for more information on detection limits, including the use of single values or probability surfaces.

#### &lt;minimum_detection_limit&gt; (OGI_camera_zim)

**Data type:** List of floats

**Default input:** [0.24, 0.39]

**Description:** A list of parameters [a, b] that define the emissions rate based probability of detection of a emissions. The two parameters define power law cumulative probability function as described in Zimmerle (2020), where both a and b are empirical parameters that define the shape of the curve, and are based on the camera crew experience. The probability detection of an emission with OGI is calculated using the following function:

$$
p = a*x^{b}
$$

where p is the probability of detection, _x_ is the emission rate in grams of methane per second. The default
parameters used are that associated with the moderate ability to detect.

**Notes on acquisition:** If not input is provided for the minimum detection limit (`minimum_detection_limit: []`), the values [0.24, 0.39] will be used.

We recommend extensive controlled release testing under a range of representative release rates and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** Detection probabilities for OGI cameras have been shown to vary with operator experience, wind speed, scene background, and other variables. Parameters are experimentally derived. The Zimmerle study for experienced inspectors could still represent an underestimate as (i) weather conditions were relatively good, (ii) OGI inspectors were participating in a formal study and were likely very focused, and (iii) many of the emissions were odorized. These results would therefore not include laziness, neglect, or missing of emissions from difficult to access areas. See Section 3.8 for more information on detection limits, including the use of single values or probability surfaces.

#### &lt;minimum_detection_limit&gt; (METEC_no_wind)

**Data type:** List of floats

**Default input:** []

**Description:** A list of parameters [a, b, _, c] where a and b are constants in the following formula:

$$
p = \frac{1}{1 + e^{a - b * x}}
$$

and `c` represents the optional minimum threshold that the rate must exceed to be considered for detection and `x` represents the emission rate in kilograms of methane per hour.

**Notes on acquisition:** N/A

**Notes of caution:** Detection probabilities have been shown to vary with wind speed, scene background, and other variables. The METEC studies may still underestimate these probabilities, as not all variables can be accounted for in a controlled environment compared to real life working conditions.

### &lt;coverage&gt;

#### &lt;spatial&gt; _(propagating parameter)_

**Data type:** Numeric

**Default input:** 1.0

**Description:** Probability (0-1) that a technology and work practice can locate an emission. Internally, each emission will be randomly assigned a True or False value based on this probability indicating whether or not the emission can be detected by the technology and work practice. This value is rolled only once for each emission and technology-work practice pair, and remains consistent for subsequent surveys. Spatial coverage is also not affected by emission size.

`eg. coverage.spatial = 0.25`. The emission has a 25% chance of being detected regardless of the number of surveys.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#method_spatial-sites-file)
- [Site type File](#method_spatial-site-type-file)
- [Equipment File](#method_spatial-equipment-file)
- [Sources File](#method_spatial-source-file)

**Notes on acquisition:** N/A

**Notes of caution:** Future research is required!

#### &lt;temporal&gt;

**Data type:** Numeric

**Default input:** 1.0

**Description:** Probability (0-1) that a crew can locate an emission during a survey. Internally, each emission will be randomly assigned a True or False based on this probability increasing survey will improve the chances of the emission being detected.

`eg. coverage.temporal = 0.25`. The emission has a 25% chance of being detected **every time** it is surveyed.

**Notes on acquisition:** N/A

**Notes of caution:** Future research is required!

### &lt;cost&gt;

**Description:** The cost to deploy a given method. The type of currency is not considered, but it must be consistent across all cost inputs.

#### &lt;per_day&gt;

**Data type:** Numeric

**Default input:** 0

**Description:** The daily cost charged by the service provider (per crew). It is charged each time a crew is deployed, regardless of how many sites they survey that day.

For `stationary`, the cost per day is for each site the method is deployed on.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** `Stationary` deployment methods only use the `per_day` and `upfront` cost values.

#### &lt;per_site&gt;  _(propagating parameter)_ _(mobile parameter)_

**Data type:** Numeric

**Default input:** 0

**Description:** The cost charged by the service provider (per crew per site). It is charged each time a crew is deployed at a site.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#method_survey_cost-sites-file)
- [Site type File](#method_survey_cost-site-type-file)

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** `Stationary` deployment methods only use the `per_day` and `upfront` cost values.

#### &lt;upfront&gt;  _(propagating parameter)_

_TODO_ Doesn't exist

**Data type:** Numeric

**Default input:** 0

**Description:** The initial up-front cost of each crew. This cost is only charged once.

- For `mobile` deployment the total upfront cost will be upfront **times** the number of crews used.
- For `stationary` deployment the total upfront cost will be equal to the user input value. There is **no** scaling.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#sites_file)
- [Site type File](#site-type-file)

**Notes on acquisition:** Consult service provider.

**Notes of caution:** Does not account for maintenance activities or the cost of replacing devices at the end of their lifetime.

`Stationary` deployment methods only use the `per_day` and `upfront` cost values.

### &lt;crew_count&gt; _(mobile parameter)_

**Data type:**  Numeric (Integer)

**Default input:** 0

**Description:** The maximum number of distinct, independent crews that will be deployed using the same method. If the `crew_count` is not provided, LDAR-Sim will provide crews as needed. When explicitly stated, the maximum number of crews will be utilized for the given method.
Warning, for follow-up mobile methods, crew count will be defaulted to 1 if not explicitly stated, which may lead to crew shortage.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Unless explicitly evaluating labour constraints, ensure that sufficient crews are available to perform LDAR according to the requirements set out in the infrastructure_file. For example, if 2000 facilities require LDAR, and each takes an average of 300 minutes, ~10,000 work hours are required, or 3-4 crews working full time.

### &lt;consider_daylight&gt;

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to indicate whether crews should only work during daylight hours. If False, crews work the number of hours specified by the [max_workday](#max_workday-mobile-parameter) input variable used for each method. If True, crews work the shorter of either [max_workday](#max_workday-mobile-parameter) or the number of daylight hours calculated using the PyEphem package in python using latitude, longitude of each site, for each day of the year.

**Notes on acquisition:** Acquisition is automated using required latitude and longitude coordinates for each facility (see infrastructure_file input) at each time step.

**Notes of caution:** In most cases, True and False will yield similar results. Use of daylight constraints should be considered for companies that do not wish to deploy crews in the dark for safety reasons, especially for locations at high latitudes during winter months (e.g., Northern Alberta). However, this functionality should not be used to determine whether sunlight is available for passive remote sensing methods or other technologies that require sunlight operate, as the sun has already set when civil twilight occurs (see obs.horizon). Solar flux will vary with topography and cloud cover (use ERA5 data).

### &lt;surveys_per_year&gt; _(propagating parameter)_ _(mobile parameter)_

**Data type:**  Numeric (Integer)

**Default input:** N/A

**Description:** An integer indicating the number of required surveys at each facility per calendar year.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#method_surveys_per_year-sites-file)
- [Site type File](#method_surveys_per_year-site-type-file)

**Notes on acquisition:** Survey frequencies can be based on regulatory requirements, company policies, or can be fabricated by the modeler to explore different scenarios.

**Notes of caution:** Note that just because a number of surveys is prescribed, it does not mean that this number of surveys will necessarily be performed. For example, if labour limitations exist (i.e., not enough crews are available to inspect the number of facilities in the program) or if environmental conditions are unsuitable (i.e., a particular facility is in a cloudy location that cannot be accessed by satellite), the performed number of surveys may be less than the prescribed number. This variable is not required for continuous measurement methods.

**Note:** this parameter may also be set more granularly using the infrastructure files.

### &lt;survey_time&gt; _(propagating parameter)_ _(mobile parameter)_

**Data type:**  Numeric (Integer)

**Default input:** N/A

**Description:** The number in minutes required to complete a survey or screening at each facility.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#method_survey_time-sites-file)
- [Site type File](#method_survey_time-site-type-file)

**Notes on acquisition:** In most cases, an estimate will be made as data will not exist for the specific combination of facility and unique method. However, as new methods and programs are implemented, data will become available to better refine modeling estimates and develop more intelligent programs.

**Notes of caution:** This variable is an empirical estimate of how much time is required for a given mobile method to complete a survey at a given facility. This includes anything that happens onsite (e.g., calibrations, interfacing with the operator, etc.) but _does not include_ driving time between facilities or any other account of time spent offsite. This variable is simply the amount of time that passes from the start of a facility survey to the end. If a facility takes longer than there is time left in a day, then the agent/crew returns the following day to continue work, and so on and so forth, until the facility is completed. This variable is not required for continuous measurement methods.

**Note:** this parameter may also be set more granularly using the infrastructure files.

### &lt;max_workday&gt; _(mobile parameter)_

**Data type:**  Numeric (Integer)

**Default input:** 8

**Description:** The maximum number of hours a crew can work in day (includes travel time).

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** This can be overridden if [consider_daylight](#consider_daylight) is True and the valid daylight hours are shorter.

### &lt;reporting_delay&gt;

**Data type:** Numeric (Integer)

**Default input:** 2

**Description:** The number of days that pass between the end of a survey (when a site is flagged or emissions are tagged) and when the duty holder is informed. The reporting delay is then followed by either the [repair delay](#repairs) or [follow-up delay](#delay-follow_up) based on the simulated work practice.

**Notes on acquisition:** Get this information from the service provider.

**Notes of caution:** Many service providers have automated systems for reporting emissions as soon as they are found and tagged. However, some companies still provide paper or pdf reports days or even weeks later. It is important to understand the expectations between the duty holder and the service provider.

### &lt;time_between_sites&gt;

**Description:** The following parameters specify the time required between surveys for planning, travel, setup, and takedown. This includes all the time not spent on the actual site survey, but the time needed between each site survey by a crew.

#### file (time_between_sites) _(mobile parameter)_

**Data type:** String

**Default input:** None

**Description:** A string denoting the filename of a csv file containing travel times. The file should include one row, with a column header in row 1 of `time_between_sites`

**Notes on acquisition:** Each value should represent not only driving time, but all time spent not conducting surveys (driving, breaks, meals, break downs, trains, etc.) This data should be scraped from historical GPS data associated with LDAR survey crews, ideally for the facilities under evaluation.

**Notes of caution:** These data may be difficult to acquire and may lack representativeness.

#### values (time_between_sites) _(mobile parameter)_

**Data type:** List of Integers

**Default input:** [30]

**Description:** The list of numbers denotes the time in minutes required to plan, travel, setup, take down, required in between surveys. A value is selected at random from the provided list.

### &lt;scheduling&gt;

#### &lt;deployment_months&gt;  _(propagating parameter)_

**Data type:** List of integers

**Default input:** [1,2,3,4,5,6,7,8,9,10,11,12]

**Description:** A list of months used for scheduling. Methods can only be deployed during these months. For example, [8,9] indicates methods can only be deployed in August and September. If not defined, LDAR-Sim assumes methods can be deployed every month.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#method_deploy_months-sites-file)
- [Site type File](#method_deploy_months-site-type-file)

**Notes on acquisition:** N/A

**Notes of caution:** Only `mobile` [methods](#deployment_type) can use this functionality.

#### &lt;deployment_years&gt;  _(propagating parameter)_

**Data type:** List of integers

**Default input:** N/A

**Description:** A list of years used for scheduling. Methods can only be deployed during these years. For example, [2017,2018] indicates methods can only be deployed in 2017 and 2018\. If not defined, LDAR-Sim assumes methods can be deployed every year.

See the following files for examples on setting this value at a more granular level:

- [Sites File](#method_deploy_years-sites-file)
- [Site type File](#method_deploy_years-site-type-file)

**Notes on acquisition:** N/A

**Notes of caution:** Only `mobile` [methods](#deployment_type) can use this functionality.

### &lt;weather_envelopes&gt;

**Description:** The following parameters define the valid weather conditions for the given method. If the average weather condition for a given day falls outside of these valid conditions, the crews for the specified method will not be deployed and will attempt to conduct the survey the following day.

#### &lt;precipitation&gt;

**Data type:** List of floats

**Default input:** [0, 0.5]

**Description:** The range of precipitation accumulation allowed (mm) over one hour.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### &lt;temperature&gt;

**Data type:** List of floats

**Default input:** [-40, 40]

**Description:** The range of average hourly temperature (°C) between which crews will work.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Units are in degrees Celsius, not Fahrenheit.

#### &lt;wind&gt;

**Data type:** List of floats

**Default input:** [0, 10]

**Description:** The bounding range of maximum average hourly wind speed (m/s at 10m) between which crews will work.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### &lt;is_follow_up&gt;

**Data type:** Boolean

**Default input:** False (Required to be set for each method added to program)

**Description:** A binary True/False to indicate whether the method is used to survey sites previously flagged by screening technologies. If true this method will only visit sites flagged.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** No data acquisition required.

### &lt;follow_up&gt;

**Description:** The following parameters are used to specify the work practices that enforce the scheduling of the relevant follow-up method .

#### &lt;preferred_method&gt;

**Data type:** String

**Default input:** N/A

**Description:** This parameter allows surveying methods to determine which follow-up method to trigger if multiples are present. If not set, LDAR-Sim will expect only one follow-up method to be present for a single program. Leveraging this parameter enables the use of alternative site or equipment level follow-up methods, facilitating subsequent rounds of screenings based on initial screening results.

Moreover, this feature can model work practices involving multiple screenings to increase confidence in fugitive emissions, measurement accuracy, etc. Each method in the follow-up chain must have the preferred_method set to the corresponding method it triggers.

**Notes on acquisition:** N/A

**Notes of caution:** If a method within a program is set to have a preferred follow-up method, all methods requiring a follow-up in the program should also be set with a preferred method to avoid ambiguity regarding which follow-up method is being used. Moreover, the last follow-up method in a work practice must be at a component level for leaks to be tagged and repaired. The value of this parameter must be identical to an existing[method name](#method_name).

#### &lt;delay&gt; (follow_up)

**Data type:** Numeric (Integer)

**Default input:** 0

**Description:** The number of days required to have passed since the first site added to the site candidate flagged pool before a site can be flagged. The company will hold all measurements in a site candidate flagged pool.

The emissions rate for flagging mobile deployment methods is determined by the follow-up  [threshold](#threshold-mobile-parameter) and the specified [proportion](#proportion), as outlined  by the [redundancy filter](#redundancy_filter-mobile-parameter).

For `Stationary` deployment methods, flagging is based on the [rolling-average](#rolling_average) parameters and specified [proportion](#proportion).

**Notes on acquisition:** N/A

**Notes of caution:** N/A

#### &lt;instant_threshold&gt;

**Data type:** Numeric (Float)

**Default input:** 0.0

**Description:** The follow-up instant threshold in grams per second. Measured site-level emissions must be above this threshold if the site is to be immediately be flagged for follow-ups, instead of being added to the pool of candidate flagged sites.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** The instant threshold should be set above the [follow-up threshold](#threshold-mobile-parameter), as this is the minimum emission rate that a site must reach to be flagged.

Follow-up thresholds are explored in detail in Fox et al. 2021\. Choosing follow-up rules is complex and work practices should be developed following extensive analysis of different scenarios. It is important to understand how follow-up thresholds and follow-up ratios interact, especially if both are to be used in the same program. Note that follow-up thresholds are similar to minimum detection limits but that the former is checked against the measured emission rate (which is a function of quantification error) while the latter is checked against the true emission rate.

#### &lt;interaction_priority&gt;

**Data type:** String

**Default input:** "threshold"

**Description:** Specifies which algorithm to run first on candidate sites when determining which to flag. The following are the valid options for this parameter:

- `threshold`: The proportion of sites to follow up with will be taken from all sites over the threshold
- `proportion`: The proportion of sites will be taken from the candidate sites, then from those sites follow-up will occur at sites above the threshold.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### &lt;proportion&gt;

**Data type:** Numeric

**Default input:** 1.0

**Description:** A ratio (0 to 1.0) defines the proportion or percentage of flagged sites that will receive follow-ups. For example, if the follow-up ratio is 0.5, the top 50% of flagged sites (ranked by measured emission rate) will receive follow-up. Candidate flagged sites have already been checked against the minimum detection limit.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Specifies which measured emission rates to use when identifying flagged candidate sites for follow-up. This is relevant for individual sites that have had multiple independent measurements during the given period, resulting in the sites being added to a candidate pool of potentially flagged sites. The following are the three options available for this parameter:

#### &lt;redundancy_filter&gt; _(mobile parameter)_

**Data type:** String

**Default input:** "recent"

**Description:** Specifies which measured emission rates to utilize when identifying flagged candidate sites for follow-up. This is relevant for individual sites that have had multiple independent measurements in the given period where the candidate flagged site pool has been accumulating. The following are the 3 options available for this parameter:

- `recent`(default): The most recent measurement for a given site in the "flagged pool" will be used to check the follow-up threshold and proportion.
- `max`: The highest measured emission rates will be used.
- `average`: The average emission from all surveys for a given site will be used.

**Notes on acquisition:** N/A

**Notes of caution:** If the [follow\_up.delay](#delay-follow_up) is not zero, crews may survey a given site multiple times, adding to the candidate flagged site pool. This parameter becomes especially relevant in any methods involving frequent deployments.

#### &lt;sort_by_rate&gt;

**Data type:** Boolean

**Default input:** True

**Description:** Indicates whether the schedule of the follow-ups for the sites flagged will be sorted by their emission rates. If set to True, follow-up schedules will be sorted based on the observed site emission rates, prioritizing the largest emitting sites first. If set to False, the follow-ups will be scheduled based on the a first flagged basis.

**Notes on acquisition:** Based on operator work practices.

**Notes of caution:** For the intended follow-up `interaction_priority:proportion` use case, it's advisable to enable sorting by setting `sort_by_rate: True`. This ensures that the original purpose of using `interaction_priority:proportion` is maintained.

#### &lt;threshold&gt; _(mobile parameter)_

**Data type:** Float

**Default input:** 0.0

**Description:** The follow-up threshold in grams per second. Measured site-level emissions must be above the follow-up threshold before a site can be flagged.

The follow-up [delay](#delay-follow_up) parameter can be set to require multiple measurements for a site above threshold before a site is flagged.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Follow-up thresholds are explored in detail in Fox et al. 2021\. Choosing follow-up rules is complex and work practices should be developed following extensive analysis of different scenarios. It is important to understand how follow-up thresholds and follow-up ratios interact, especially if both are to be used in the same program. Note that follow-up thresholds are similar to minimum detection limits but that the former is checked against to the measured emission rate (which is a function of quantification error) while the latter is checked against the true emission rate.

### rolling_average

**Description:** This parameter provides the overarching heading for the nested parameters related to rolling averages. The following parameters are only relevant when [deployment type](#deployment_type) is set to `stationary`.

#### small_window _(stationary parameter)_

**Data Type:** Numeric(Integer)

**Default input:** 7

**Description:** The number of days to consider when taking the rolling average for the [small threshold](#small_window_threshold-stationary-parameter).

**Notes of acquisition:** N/A

**Notes of caution:** N/A

#### large_window _(stationary parameter)_

**Data Type:** Numeric(Integer)

**Default input:** 30

**Description:** The number of days to consider when taking the rolling average for the [large threshold](#large_window_threshold-stationary-parameter).

**Notes of acquisition:** N/A

**Notes of caution:** N/A

#### small_window_threshold _(stationary parameter)_

**Data Type:** Numeric(Float)

**Default input:** 0.0

**Description:** The threshold in grams per second to consider when triggering follow-up work practices, based on the smaller window rolling average.

**Notes of acquisition:** N/A

**Notes of caution:** When using the [stationary deployment type](#deployment_type),only the `small_window_threshold` is used by default. To enable two different rolling average considerations for the method, users will need to set the [large_window_threshold](#large_window_threshold-stationary-parameter).

#### large_window_threshold _(stationary parameter)_

**Data Type:** Numeric(Float)

**Default input:** _placeholder_float_

**Description:** The threshold in grams per second to consider when triggering follow-up work practices, based on the larger window rolling average. This is an optional second threshold value; if not set, the method will only consider the [small_window_threshold](#small_window_threshold-stationary-parameter) for triggering follow-up work practices.

**Notes of acquisition:** N/A

**Notes of caution:** When using the [stationary deployment type](#deployment_type),only the [small_window_threshold](#small_window_threshold-stationary-parameter) is used by default. To enable two different rolling average considerations for the method, users will need to set the `large_window_threshold`.

--------------------------------------------------------------------------------

## 10\. Virtual World Defining Files

In LDAR-Sim, the virtual world is defined by a combination of the virtual world parameter file and corresponding CSV files that contain the specific properties, as discussed in the [virtual world parameters](#7-virtual-world-setting).

The following figure offers a visual guideline for the various parameters that can be propagated and set at more granular levels to define a virtual world, outlining the lowest adjustable property level for each parameter.

![data structure](doc-images/input_data_structure.png)

**Note:** It is important to understand that for all the virtual world defining files, all optional columns have their values internally propagated down and set at the most granular level based on the provided higher-level values where relevant. For example, if the user sets the required surveys per year for a given site only in the method parameter file,  the simulator will internally set the _required surveys per year_ for each individual site.

--------------------------------------------------------------------------------

### Sites File

This file defines the individual sites that are simulated by LDAR-Sim. Each row in this file defines a single site.

At a minimum it must contain the following columns:

- [site_ID](#site_id)
- [lat](#lat)
- [lon](#lon)
- [site_type](#site_type-sites-file)

Other optional columns consist of the following:

- [equipment](#equipment-sites-file)
- [repairable_repair_delay](#repairable_repair_delay-sites-file)
- [repairable_repair_cost](#repairable_repair_cost-sites-file)
- [repairable_emissions_rate_source](#repairable_emissions_rate_source-sites-file)
- [repairable_emissions_production_rate](#repairable_emissions_production_rate-sites-file)
- [repairable_duration](#repairable_duration-sites-file)
- [repairable_multiple_emissions_per_source](#repairable_multiple_emissions_per_source-sites-file)
- [non_repairable_emissions_rate_source](#non_repairable_emissions_rate_source-sites-file)
- [non_repairable_emissions_production_rate](#non_repairable_emissions_production_rate-sites-file)
- [non_repairable_duration](#non_repairable_duration-sites-file)
- [non_repairable_multiple_emissions_per_source](#non_repairable_multiple_emissions_per_source-sites-file)

Method-specific columns are values that can be defined for a particular method. To use them, replace the `{method}` placeholder with the relevant [method_name](#method_name) that the user is parameterizing. The following method-specific columns are available for the Sites file:

- {method}_[surveys_per_year](#method_surveys_per_year-sites-file)
- {method}_[deploy_year](#method_deploy_years-sites-file)
- {method}_[deploy_month](#method_deploy_months-sites-file)
- {method}_[spatial](#method_spatial-sites-file)
- {method}_[survey_time](#method_survey_time-sites-file)
- {method}_[survey_cost](#method_survey_cost-sites-file)
- {method}_[site_deployment](#method_site_deployment-sites-file)

**Note:** As with most name-related parameters in LDAR-Sim, the values in the `site_type` and `equipment` columns are case-sensitive and must be consistent across all related files. Any method specific parameters also require the same care with the case-sensitivity and consistency in all relevant files with the method name.

See [sites file](#sites-file) for details on how to set the parameter for simulation.

--------------------------------------------------------------------------------

Below is an example _Sites file_:

|site_ID|lat|lon|site_type|equipment|OGI_site_deployment|repairable_emissions_rate_source|repairable_emissions_production_rate|
|----|----|----|----|----|----|----|----|
|1|55|-110|well pad|equipment2|FALSE|Bottom-Up Fugitive Emissions Rates|0.0001|
|2|45|-100|compressor station|equipment1, equipment2, equipment3|TRUE|Top-Down Fugitive Emission Rates|0.0064|
|3|56|-100|well pad|equipment1|TRUE|Bottom-Up Fugitive Emissions Rates|0.005|
|4|55|-109|compressor station|equipment1, equipment2, equipment3|TRUE|Top-Down Fugitive Emission Rates|0.0064|

--------------------------------------------------------------------------------

#### site_ID

**Description:** A unique identifier, defined by the user-defined, for each given site.

#### lat

**Description:** The latitude of the given site.

**Note of caution:** The latitude of the given site must be within the boundaries of the given weather file.

#### lon

**Description:** The longitude of the given site.

**Note of caution:** The longitude of the given site must be within the boundaries of the given weather file.

#### site_type (Sites file)

**Description:** A user-defined value that identifies and groups a particular site type.

**Note:** It is case-sensitive and must remain consistent if provided in the [site type file](#site-type-file).

#### equipment (Sites file)

**Description:** Equipment in LDAR-Sim allows users to group emissions at a more granular level than an entire site, suitable for technologies with higher resolution than a generic site but lower than individual emission sources.

Equipment in LDAR-Sim can be defined in two different ways: as a single integer or as a string of user-defined values.

- Numeric value: Defines the number of placeholder equipment items to create and populate. This **must** be a **single** number. For example setting the value to 5 will create `5` placeholder_equipments.
- One or more equipment identifier: Each value provided becomes an equipment group. Users can specify a list of equipment groups that define the given site by separating each item with a comma (,). For example setting this to `well, flare` will produce 2 equipments, one called _well_ and another called _flare_.

**Note:** When using a user-defined value, it is case-sensitive and must remain consistent with the [equipment file](#equipment-file).

**Note of caution:** Using a numeric value for equipment is a legacy feature from LDAR-Sim V3. It is recommended to use user-defined values or sets of values if your data permits.

#### repairable_repair_delay (Sites file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair delay](#values-delaypropagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value in days.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-delaypropagating-parameter)
- [Site type File](#repairable_repair_delay-site-type-file)
- [Equipment File](#repairable_repair_delay-equipment-file)
- [Source File](#repair_delay-source-file)

#### repairable_repair_cost (Sites file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair cost](#values-cost-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing cost to repair emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-cost-propagating-parameter)
- [Site type File](#repairable_repair_cost-site-type-file)
- [Equipment File](#repairable_repair_cost-equipment-file)
- [Source File](#repair_cost-source-file)

#### repairable_emissions_rate_source (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the repairable emissions for the given site. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given repairable emissions rate source.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Site type File](#repairable_emissions_rate_source-site-type-file)
- [Equipment File](#repairable_emissions_rate_source-equipment-file)
- [Source File](#emissions_rate_source-source-file)

#### repairable_emissions_production_rate (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of a repairable emissions occurring at the given site at any given day.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Site type File](#repairable_emissions_production_rate-site-type-file)
- [Equipment File](#repairable_emissions_production_rate-equipment-file)
- [Source File](#emissions_production_rate-source-file)

#### repairable_duration (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the maximum emissions duration in days for repairable emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Site type File](#repairable_duration-site-type-file)
- [Equipment File](#repairable_duration-equipment-file)
- [Source File](#duration-source-file)

#### repairable_multiple_emissions_per_source (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if there can be multiple repairable emissions produced by the component-sources at the given site at a single point in time.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Site type File](#repairable_multiple_emissions_per_source-site-type-file)
- [Equipment File](#repairable_multiple_emissions_per_source-equipment-file)
- [Source File](#multiple_emissions_per_source-source-file)

#### non_repairable_emissions_rate_source (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the non-repairable emissions for the given site. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given non-repairable emissions rate source.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Site type File](#non_repairable_emissions_rate_source-site-type-file)
- [Equipment File](#non_repairable_emissions_rate_source-equipment-file)
- [Source File](#emissions_rate_source-source-file)

#### non_repairable_emissions_production_rate (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of a non-repairable emissions occurring at the given site at any given day.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Site type File](#non_repairable_emissions_production_rate-site-type-file)
- [Equipment File](#non_repairable_emissions_production_rate-equipment-file)
- [Source File](#emissions_production_rate-source-file)

#### non_repairable_duration (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the maximum emissions duration in days for non-repairable emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Site type File](#non_repairable_duration-site-type-file)
- [Equipment File](#non_repairable_duration-equipment-file)
- [Source File](#duration-source-file)

#### non_repairable_multiple_emissions_per_source (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if there can be multiple non-repairable emissions produced by the component-sources at the given site at a single point in time.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Site type File](#non_repairable_multiple_emissions_per_source-site-type-file)
- [Equipment File](#non_repairable_multiple_emissions_per_source-equipment-file)
- [Source File](#multiple_emissions_per_source-source-file)

#### {method}_surveys_per_year (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[surveys_per_year](#surveys_per_year-propagating-parameter-mobile-parameter) for more details on what this parameter represents. In this file, this is a single integer representing the number of surveys to be conducted in a given year for the specified site for the specified method.

This parameter can also be set in the following files:

- [Method Parameter file](#surveys_per_year-propagating-parameter-mobile-parameter)
- [Site type File](#method_surveys_per_year-site-type-file)

#### {method}_deploy_years (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [deploy_year](#deployment_years--propagating-parameter) for more details on what this parameter represents. In this file, this is a list of integers representing which years the specified method can be deployed on for the given site.

This parameter can also be set in the following files:

- [Method Parameter file](#deployment_years--propagating-parameter)
- [Site type File](#method_deploy_years-site-type-file)

#### {method}_deploy_months (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[deploy_month](#deployment_months--propagating-parameter) for more details on what this parameter represents. In this file, this is a list of integers representing which months the specified method can be deployed on for the given site.

This parameter can also be set in the following files:

- [Method Parameter file](#deployment_months--propagating-parameter)
- [Site type File](#method_deploy_months-site-type-file)

#### {method}_spatial (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[spatial](#spatial-propagating-parameter) for more details on what this parameter represents. In this file, this is a single value, representing the chance in which the given method can detect each emissions at the given site.

This parameter can also be set in the following files:

- [Method Parameter file](#spatial-propagating-parameter)
- [Site type file](#method_spatial-site-type-file)
- [Equipment file](#method_spatial-equipment-file)
- [Source file](#method_spatial-source-file)

#### {method}_survey_time (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [survey_time](#survey_time-propagating-parameter-mobile-parameter) for more details on what this parameter represents. In this file, this is a single value, representing how long in minutes it takes for the specified method to survey the given site.

This parameter can also be set in the following files:

- [Method Parameter file](#survey_time-propagating-parameter-mobile-parameter)
- [Site type file](#method_survey_time-site-type-file)

#### {method}_survey_cost (Sites file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [survey_cost](#per_site--propagating-parameter-mobile-parameter) for more details on what this parameter represents. In this file, this is a single value, representing the cost of the specified method to survey the given site.

This parameter can also be set in the following files:

- [Method Parameter file](#per_site--propagating-parameter-mobile-parameter)
- [Site type file](#method_survey_cost-site-type-file)

#### {method}_site_deployment (Sites file)

**Description:** A True/False column that indicates whether the specified method will be deployed at the given site. For example, if the value is set to `FALSE`, the emissions at the site will be simulated, but the method will not be deployed at that site. This is similar to setting the[surveys per year](#surveys_per_year-propagating-parameter-mobile-parameter) to 0 for the site.

This parameter can also be set in the following file:

- [Site type file](#method_site_deployment-site-type-file)

**Note:** If site deployment is set to False for a site/site(s) in the sites file for all non-follow-up methods that make up a program, that site will be functionally not measured by the program. In this case, estimated emissions are computed using the annual average of all estimated emissions from all measured sites of the same type or, if not possible, the annual average of all measured sites.

--------------------------------------------------------------------------------

### Site Type File

This is an optional file that is used to define groups of sites. It must contain the [site_type](#site_type-site-type-file) column. All other columns are optional and based on the user's needs.

Possible column headers:

- [equipment](#equipment-site-type-file)
- [repairable_repair_delay](#repairable_repair_delay-site-type-file)
- [repairable_repair_cost](#repairable_repair_cost-site-type-file)
- [repairable_emissions_rate_source](#repairable_emissions_rate_source-site-type-file)
- [repairable_emissions_production_rate](#repairable_emissions_production_rate-site-type-file)
- [repairable_duration](#repairable_duration-site-type-file)
- [repairable_multiple_emissions_per_source](#repairable_multiple_emissions_per_source-site-type-file)
- [non_repairable_emissions_rate_source](#non_repairable_emissions_rate_source-site-type-file)
- [non_repairable_emissions_production_rate](#non_repairable_emissions_production_rate-site-type-file)
- [non_repairable_duration](#non_repairable_duration-site-type-file)
- [non_repairable_multiple_emissions_per_source](#non_repairable_multiple_emissions_per_source-site-type-file)

Method-specific columns are values that can be defined for a particular method. To use them, replace the `{method}` placeholder with the relevant [method_name](#method_name) that the user is parameterizing. The following method-specific columns are available for the site type file:

- {method}_[surveys_per_year](#method_surveys_per_year-site-type-file)
- {method}_[deploy_years](#method_deploy_years-site-type-file)
- {method}_[deploy_months](#method_deploy_months-site-type-file)
- {method}_[spatial](#method_spatial-site-type-file)
- {method}_[survey_time](#method_survey_time-site-type-file)
- {method}_[survey_cost](#method_survey_cost-site-type-file)
- {method}_[site_deployment](#method_site_deployment-site-type-file)

**Note:** As with most name-related parameters in LDAR-Sim, the values in the `site_type` and `equipment` columns are case-sensitive and must be consistent across all related files. Any method specific parameters also require the same care with the case-sensitivity and consistency in all relevant files with the method name.

See [site type file](#site-type-file) for details on how to set the parameter for simulation.

--------------------------------------------------------------------------------
Below is an example _Site type file_:

|site_type|equipment|OGI_site_deployment|repairable_emissions_rate_source|repairable_emissions_production_rate|
|----|----|----|----|----|
|well pad|equipment1|FALSE|Bottom-Up Fugitive Emissions Rates|0.0001|
|compressor station|equipment1, equipment2, equipment3|TRUE|Top-Down Fugitive Emission Rates|0.0064|

--------------------------------------------------------------------------------

#### site_type (Site type file)

**Description:** A unique user defined value that defines a particular site type.

**Note:** It is case-sensitive and must remain consistent when provided in the [sites file](#sites-file).

#### equipment (Site type file)

**Description:** Equipment in LDAR-Sim allows users to group emissions at a more granular level than an entire site, suitable for technologies with higher resolution than a generic site but lower than individual emission sources.

Equipment in LDAR-Sim can be defined in two different ways: as a single integer or as a string of user-defined values.

- Numeric value: Defines the number of placeholder equipment items to create and populate.
- User-defined value or set of values: Each value provided becomes an equipment group. Users can specify a list of equipment groups that define the given site by separating each item with a comma (,).

**Note:** When using a user-defined value, it is case-sensitive and must remain consistent with the [equipment file](#equipment-file).

**Note of caution:** Using a numeric value for equipment is a legacy feature from LDAR-Sim V3. It is recommended to use user-defined values or sets of values if your data permits.

#### repairable_repair_delay (Site type file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair delay](#values-delaypropagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value in days.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-delaypropagating-parameter)
- [Sites File](#repairable_repair_delay-sites-file)
- [Equipment File](#repairable_repair_delay-equipment-file)
- [Source File](#repair_delay-source-file)

#### repairable_repair_cost (Site type file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair cost](#values-cost-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing cost to repair emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-cost-propagating-parameter)
- [Sites File](#repairable_repair_cost-sites-file)
- [Equipment File](#repairable_repair_cost-equipment-file)
- [Source File](#repair_cost-source-file)

#### repairable_emissions_rate_source (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the repairable emissions for the given site type. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given repairable emissions rate source.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Sites File](#repairable_emissions_rate_source-sites-file)
- [Equipment File](#repairable_emissions_rate_source-equipment-file)
- [Source File](#emissions_rate_source-source-file)

#### repairable_emissions_production_rate (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of a repairable emissions occurring at any site of the given site type at any given day.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Sites File](#repairable_emissions_production_rate-sites-file)
- [Equipment File](#repairable_emissions_production_rate-equipment-file)
- [Source File](#emissions_production_rate-source-file)

#### repairable_duration (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the maximum emissions duration in days for repairable emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Sites File](#repairable_duration-sites-file)
- [Equipment File](#repairable_duration-equipment-file)
- [Source File](#duration-source-file)

#### repairable_multiple_emissions_per_source (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if there can be multiple repairable emissions produced by the component-sources at the given site type at a single point in time.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Sites File](#repairable_multiple_emissions_per_source-sites-file)
- [Equipment File](#repairable_multiple_emissions_per_source-equipment-file)
- [Source File](#multiple_emissions_per_source-source-file)

#### non_repairable_emissions_rate_source (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the non-repairable emissions for the given site type. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given non-repairable emissions rate source.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Sites File](#non_repairable_emissions_rate_source-sites-file)
- [Equipment File](#non_repairable_emissions_rate_source-equipment-file)
- [Source File](#emissions_rate_source-source-file)

#### non_repairable_emissions_production_rate (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of a non-repairable emissions occurring at any site of the given site type at any given day.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Sites File](#non_repairable_emissions_production_rate-sites-file)
- [Equipment File](#non_repairable_emissions_production_rate-equipment-file)
- [Source File](#emissions_production_rate-source-file)

#### non_repairable_duration (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the maximum emissions duration in days for non-repairable emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Sites File](#non_repairable_duration-sites-file)
- [Equipment File](#non_repairable_duration-equipment-file)
- [Source File](#duration-source-file)

#### non_repairable_multiple_emissions_per_source (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if there can be multiple non-repairable emissions produced by the component-sources at the given site type at a single point in time.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Sites File](#non_repairable_multiple_emissions_per_source-sites-file)
- [Equipment File](#non_repairable_multiple_emissions_per_source-equipment-file)
- [Source File](#multiple_emissions_per_source-source-file)

#### {method}_surveys_per_year (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[surveys_per_year](#surveys_per_year-propagating-parameter-mobile-parameter) for more details on what this parameter represents. In this file, this is a single numeric value representing the number of required surveys per year for the specified method for every site of the given site type.

This parameter can also be set in the following files:

- [Methods Parameter file](#surveys_per_year-propagating-parameter-mobile-parameter)
- [Sites file](#method_surveys_per_year-sites-file)

#### {method}_deploy_years (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [deploy_year](#deployment_years--propagating-parameter) for more details on what this parameter represents. In this file, this is a list of integers representing which years the specified method can be deployed on for every site of the given site type.

This parameter can also be set in the following files:

- [Methods Parameter file](#deployment_years--propagating-parameter)
- [Sites file](#method_deploy_years-sites-file)

#### {method}_deploy_months (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[deploy_month](#deployment_months--propagating-parameter) for more details on what this parameter represents. In this file, this is a list of integers representing which months the specified method can be deployed on for every site of the given site type.

This parameter can also be set in the following files:

- [Methods Parameter file](#deployment_months--propagating-parameter)
- [Sites file](#method_deploy_months-sites-file)

#### {method}_spatial (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[spatial](#spatial-propagating-parameter) for more details on what this parameter represents. In this file, this is a single value, representing the chance in which the given method can detect emissions at the given site type.

This parameter can also be set in the following files:

- [Methods Parameter file](#spatial-propagating-parameter)
- [Sites file](#method_spatial-sites-file)
- [Equipment file](method_spatial-equipment-file)
- [Source file](#method_spatial-source-file)

#### {method}_survey_time (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [survey_time](#survey_time-propagating-parameter-mobile-parameter) for more details on what this parameter represents. In this file, this is a single value, representing how long in minutes it takes for the specified method to survey a site of the given site type.

This parameter can also be set in the following files:

- [Methods Parameter file](#survey_time-propagating-parameter-mobile-parameter)
- [Sites file](#method_survey_time-sites-file)

#### {method}_survey_cost (Site type file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [survey_cost](#per_site--propagating-parameter-mobile-parameter) for more details on what this parameter represents. In this file, this is a single value, representing the cost of the specified method to survey a site of the given site type.

This parameter can also be set in the following files:

- [Methods Parameter file](#per_site--propagating-parameter-mobile-parameter)
- [Sites file](#method_survey_cost-sites-file)

#### {method}_site_deployment (Site type file)

**Description:** A True/False column that indicates whether the specified method will be deployed at the given site type. For example, if the value is set to `FALSE`, the emissions at the site will be simulated, but the method will no be deployed at any sites of that site type. This is similar to setting the[surveys per year](#surveys_per_year-propagating-parameter-mobile-parameter) to 0 for the site.

This parameter can also be set in the following file:

- [Sites file](#method_site_deployment-sites-file)

**Note:** If site_type deployment is set to False for a site_type in the sites file for all non-follow-up methods that make up a program, that site_type will be functionally not measured by the program. In this case, estimated emissions are computed using the annual average of all estimated emissions from all measured sites.

--------------------------------------------------------------------------------

### Equipment File

This optional file enables **users to define _equipment_ or equipment groups** for the simulation.

Only the [equipment](#equipment-equipment-file) column is mandatory.

Potential columns are:

- [{component}](#component-equipment-file)
- [repairable_repair_delay](#repairable_repair_delay-equipment-file)
- [repairable_repair_cost](#repairable_repair_cost-equipment-file)
- [repairable_emissions_rate_source](#repairable_emissions_rate_source-equipment-file)
- [repairable_emissions_production_rate](#repairable_emissions_production_rate-equipment-file)
- [repairable_duration](#repairable_duration-equipment-file)
- [repairable_multiple_emissions_per_source](#repairable_multiple_emissions_per_source-equipment-file)
- [non_repairable_emissions_rate_source](#non_repairable_emissions_rate_source-equipment-file)
- [non_repairable_emissions_production_rate](#non_repairable_emissions_production_rate-equipment-file)
- [non_repairable_duration](#non_repairable_duration-equipment-file)
- [non_repairable_multiple_emissions_per_source](#non_repairable_multiple_emissions_per_source-equipment-file)

Method-specific columns are values that can be defined for a particular method. To use them, replace the `{method}` placeholder with the relevant [method_name](#method_name) that the user is parameterizing. The following method-specific column is available for the equipment file:

- {method}_[spatial](#method_spatial-equipment-file)

**Note:** As with most name-related parameters in LDAR-Sim, the values in the `equipment` and the user defined _component_ columns are case-sensitive and must be consistent across all related files. Any method specific parameters also require the same care with the case-sensitivity and consistency in all relevant files with the method name.

See [equipment file](#equipment-file) for details on how to set the parameter for simulation.

--------------------------------------------------------------------------------

Below is an example of an _equipment file_ that defines 3 different groups:

| equipment |component1|component2|component3|
|----|----|----|----|
|group1|1|1|0|
|group2|0|0|2|
|group3|3|0|0|

--------------------------------------------------------------------------------

### equipment (Equipment File)

**Description:** A user-defined value that defines a specific equipment group identifier for the simulation. These equipment groups influence how  `equipment level` [measurement scale](#measurement_scale)  methods detect and measure emissions. Each row must define a unique equipment identifier.

**Note:** It is case-sensitive and must remain consistent when provided in other infrastructure files, such as the [sites file](#sites-file) or the [site type file](#site-type-file)

### {component} (Equipment File)

**Description:** The column header is a user defined value corresponding to the identifier of a specific component defined as part of the simulation. The values in each column and row indicate how many counts of the given component(column) exists for the given equipment(row). These _equipment_ groups can serve as building blocks for constructing complex sites.

**Note:**The column headers are case-sensitive and must be consistent with the [Source](#component-source-file) where they are defined.

### repairable_repair_delay (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair delay](#values-delaypropagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value in days.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-delaypropagating-parameter)
- [Site File](#repairable_repair_delay-sites-file)
- [Site type File](#repairable_repair_delay-site-type-file)
- [Source File](#repair_delay-source-file)

### repairable_repair_cost (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair cost](#values-cost-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing cost to repair emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-cost-propagating-parameter)
- [Sites File](#repairable_repair_cost-sites-file)
- [Site type File](#repairable_repair_cost-site-type-file)
- [Source File](#repair_cost-source-file)

### repairable_emissions_rate_source (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the repairable emissions for the given equipment. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given repairable emissions rate source.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Sites File](#repairable_emissions_rate_source-sites-file)
- [Site type File](#repairable_emissions_rate_source-site-type-file)
- [Source File](#emissions_rate_source-source-file)

### repairable_emissions_production_rate (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of a repairable emissions occurring at the given equipment at any given day.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Sites File](#repairable_emissions_production_rate-sites-file)
- [Site type File](#repairable_emissions_production_rate-site-type-file)
- [Source File](#emissions_production_rate-source-file)

### repairable_duration (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the maximum emissions duration in days for repairable emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Sites File](#repairable_duration-sites-file)
- [Site type File](#repairable_duration-site-type-file)
- [Source File](#duration-source-file)

#### repairable_multiple_emissions_per_source (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if there can be multiple repairable emissions produced by the component-sources at the given equipment at a single point in time.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Sites File](#repairable_multiple_emissions_per_source-sites-file)
- [Site type File](#repairable_multiple_emissions_per_source-site-type-file)
- [Source File](#multiple_emissions_per_source-source-file)

#### non_repairable_emissions_rate_source (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the non-repairable emissions for the given equipment. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given non-repairable emissions rate source.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Sites File](#non_repairable_emissions_rate_source-sites-file)
- [Site type File](#non_repairable_emissions_rate_source-site-type-file)
- [Source File](#emissions_rate_source-source-file)

#### non_repairable_emissions_production_rate (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of a non-repairable emissions occurring at the given equipment at any given day.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Sites File](#non_repairable_emissions_production_rate-sites-file)
- [Site type File](#non_repairable_emissions_production_rate-site-type-file)
- [Source File](#emissions_production_rate-source-file)

#### non_repairable_duration (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the maximum emissions duration in days for non-repairable emissions.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Sites File](#non_repairable_duration-sites-file)
- [Site type File](#non_repairable_duration-site-type-file)
- [Source File](#duration-source-file)

#### non_repairable_multiple_emissions_per_source (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if there can be multiple non-repairable emissions produced by the component-sources at the given equipment at a single point in time.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Sites File](#non_repairable_multiple_emissions_per_source-sites-file)
- [Site type File](#non_repairable_multiple_emissions_per_source-site-type-file)
- [Source File](#multiple_emissions_per_source-source-file)

#### {method}_spatial (Equipment file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[spatial](#spatial-propagating-parameter) for more details on what this parameter represents. In this file, this is a single value, representing the chance in which the given method can detect emissions at the given equipment.

This parameter can also be set in the following files:

- [Methods Parameter file](#spatial-propagating-parameter)
- [Sites file](#method_spatial-sites-file)
- [Site type file](method_spatial-site-type-file)
- [Source file](#method_spatial-source-file)

--------------------------------------------------------------------------------

### Source File

This is an optional file that allows users to define individual components and the different sources a component may have.

The sources file has a few mandatory predefined column headers:

- [component](#component-source-file)
- [source](#source-source-file)
- [repairable](#repairable-source-file)

**Note of caution:** The `component` and `source` columns together act as a compound key. In simple terms, each component/source pair must be unique and exist only once.

And optional column headers that define the emissions:

- [persistent](#persistent-source-file)
- [active_duration](#active_duration-source-file)
- [inactive_duration](#inactive_duration-source-file)
- [repair_delay](#repair_delay-source-file)
- [repair_cost](#repair_cost-source-file)
- [emissions_production_rate](#emissions_production_rate-source-file)
- [emissions_rate_source](#emissions_rate_source-source-file)
- [duration](#duration-source-file)
- [multiple_emissions_per_source](#multiple_emissions_per_source-source-file)

Method-specific columns are values that can be defined for a particular method. To use them, replace the `{method}` placeholder with the relevant [method_name](#method_name) that the user is parameterizing. The following method-specific columns are available for the Sites file:

- {method}_[spatial](#method_spatial-source-file)
  
As mentioned above, if the optional columns are not provided, they will be populated with any existing higher-level values. For example, if the duration column is missing but is provided in the virtual world parameter file, LDAR-Sim will populate the durations of the specified component-source with the relevant durations from the virtual world parameter file.

**Note:** As with most name-related parameters in LDAR-Sim, the values in the `component` and `emissions_rate_source` columns are case-sensitive and must be consistent across all related files. Any method specific parameters also require the same care with the case-sensitivity and consistency in all relevant files with the method name.

See [source file](#source-file) for details on how to set the parameter for simulation.

--------------------------------------------------------------------------------

Below is an example of a _source file_ that defines two different components and their relevant sources.

|component|source|emissions_rate_source|repairable|
|----------|----------|----------|----------|
|component1|fugitive|Bottom-Up Fugitive Emissions Rates|TRUE|
|component1|non-repairable|Top-Down Fugitive Emission Rates|FALSE|
|component2|fugitive|Bottom-Up Fugitive Emissions Rates|TRUE|

--------------------------------------------------------------------------------

#### component (Source File)

**Description:** A user-defined component represents the smallest item that the highest resolution technology would be able to decipher and detect emissions from in real life.

**Note:** A `component`can have multiple emission sources, each potentially producing emissions at the same time. A _component level_ [measurement strategy](#measurement_scale) measures the total sum of all emissions from these sources at any given moment.

**Note of caution:** The `component` and `source` columns together act as a compound key. In simple terms, each component/source pair must be unique and exist only once.

This column is case-sensitive and must match the corresponding columns provided in other infrastructure files.

#### source (Source File)

**Description:** A user-defined source represents a potential emission source for a given component. It is the smallest granular level considered for emission production.

**Note of caution:** The `source` column is often an identical value to the `emissions_rate_source` column; however, these two columns serve different purposes. The `source` column allow users to apply the same [emission_rate_sources](#header) for different `sources`. Additionally, the `source` column, in conjunction with the `component` column, forms a compound key. In simple terms, each component/source pair must be unique and exist only once.

#### repairable (Source File)

**Description:** A True/False column that defines if the given emission source produces repairable(`TRUE`) or non-repairable(`FALSE`) emission.

#### persistent (Source File)

**Description:** A True/False column that defines if the given emission source produces persistent(`TRUE`) or non-persistent(`FALSE`) emission. Non-persistent emissions have a total active duration of the user set parameter [duration](#duration-propagating-parameter). However each active and inactive period is defined by the following parameters respectively, [active_duration](#active_duration-source-file) and [inactive_duration](#inactive_duration-source-file).

**Note** Non-persistent emissions start from their emitting state, and then cycle between emitting and not emitting states.

#### active_duration (Source File)

**Description:** The number of days that the given non-persistent emission is emitting for at a given time.

#### inactive_duration (Source File)

**Description:** The number of days that the given non-persistent emission is not emitting.

#### repair_delay (Source file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair delay](#values-delaypropagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value in days.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-delaypropagating-parameter)
- [Site File](#repairable_repair_delay-sites-file)
- [Site type File](#repairable_repair_delay-site-type-file)
- [Equipment File](#repairable_repair_delay-equipment-file)

#### repair_cost (Source file)

**Description:** This is a propagating parameter that can be set at multiple level of granularity. See [repair cost](#values-cost-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing cost.

This parameter can also be set in the following files:

- [Virtual World Parameter file](#values-cost-propagating-parameter)
- [Sites File](#repairable_repair_cost-sites-file)
- [Site type File](#repairable_repair_cost-site-type-file)
- [Equipment File](#repairable_repair_cost-equipment-file)

#### emissions_rate_source (Source file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_rate_source](#emissions_rate_source-propagating-parameter) for more details on what this parameter represents. In this file this is a user defined value, that corresponds to the [source](#header) of the emissions for the given emission component-source. This case-sensitive value specifies which of the potential emissions characteristics in the [emissions file](#emissions-file) should be used for the given emissions rate source.

This parameter can also be set in the following files:

Repairable Emissions:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Sites File](#repairable_emissions_rate_source-sites-file)
- [Site type File](#repairable_emissions_rate_source-site-type-file)
- [Equipment File](#repairable_emissions_rate_source-equipment-file)

Non-Repairable Emissions:

- [Virtual World Parameter file](#emissions_rate_source-propagating-parameter)
- [Sites File](#non_repairable_emissions_rate_source-sites-file)
- [Site type File](#non_repairable_emissions_rate_source-site-type-file)
- [Equipment File](#non_repairable_emissions_rate_source-equipment-file)

#### emissions_production_rate (Source file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [emissions_production_rate](#emissions_production_rate-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value, representing the chance of an emissions arising from the given source at any given day.

This parameter can also be set in the following files:

Repairable Emissions:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Sites File](#repairable_emissions_production_rate-sites-file)
- [Site type File](#repairable_emissions_production_rate-site-type-file)
- [Equipment File](#repairable_emissions_production_rate-equipment-file)

Non-Repairable Emissions:

- [Virtual World Parameter file](#emissions_production_rate-propagating-parameter)
- [Sites File](#non_repairable_emissions_production_rate-sites-file)
- [Site type File](#non_repairable_emissions_production_rate-site-type-file)
- [Equipment File](#non_repairable_emissions_production_rate-equipment-file)

#### duration (Source file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [duration](#duration-propagating-parameter) for more details on what this parameter represents. In this file, this is a single numeric value in days, representing the maximum duration of the given emission.

This parameter can also be set in the following files:

Repairable emissions:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Sites File](#repairable_duration-sites-file)
- [Site type File](#repairable_duration-site-type-file)
- [Equipment File](#repairable_duration-equipment-file)

Non-Repairable emissions:

- [Virtual World Parameter file](#duration-propagating-parameter)
- [Sites File](#non_repairable_duration-sites-file)
- [Site type File](#non_repairable_duration-site-type-file)
- [Equipment File](#non_repairable_duration-equipment-file)

#### multiple_emissions_per_source (Source file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See [multiple_emissions_per_source](#multiple_emissions_per_source-propagating-parameter) for more details on what this parameter represents. In this file, this is a `TRUE`/`FALSE` value, representing if the given source can produce multiple emissions at a given time.

This parameter can also be set in the following files:

Repairable emissions:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Sites File](#repairable_multiple_emissions_per_source-sites-file)
- [Site type File](#repairable_multiple_emissions_per_source-site-type-file)
- [Equipment File](#repairable_multiple_emissions_per_source-equipment-file)

Non-Repairable emissions:

- [Virtual World Parameter file](#multiple_emissions_per_source-propagating-parameter)
- [Sites File](#non_repairable_multiple_emissions_per_source-sites-file)
- [Site type File](#non_repairable_multiple_emissions_per_source-site-type-file)
- [Equipment File](#non_repairable_multiple_emissions_per_source-equipment-file)

#### {method}_spatial (Source file)

**Description:** This is a propagating parameter that can be set at multiple levels of granularity. See[spatial](#spatial-propagating-parameter) for more details on what this parameter represents. In this file, this is a single value, representing the chance in which the given method can detect the emissions coming from the given source.

This parameter can also be set in the following files:

- [Methods Parameter file](#spatial-propagating-parameter)
- [Sites file](#method_spatial-sites-file)
- [Site type file](method_spatial-site-type-file)
- [Equipment file](#method_spatial-equipment-file)

--------------------------------------------------------------------------------

### Emissions File

This is a mandatory file that describes emission rate characteristics. See [emissions file](#emissions-file) for details on how to set the parameter for simulation.

Each column in the emissions file represents a single emissions source. Each row represents a specific value, in the following order:

- [Header](#header)
- [Data Use](#data-use)
- [Distribution type](#distribution-type)
- [Maximum emission rate](#maximum-emission-rate)
- [Units (amount)](#units-amount)
- [Units (time)](#units-time)
- [Source](#source-emission-file)

--------------------------------------------------------------------------------

Below is an example of an Emissions file:

| Bottom-Up Fugitive Emissions Rates | Top-Down Fugitive Emission Rates |
|----------|----------|
| dist | sample |
| lognormal | n/a |
| 100000 | 100000 |
| kilogram | gram |
| hour | second |
| -1.79 | 10 |
| 2.17 | 4 |
| | 1.2|
| | 2.2|

--------------------------------------------------------------------------------

#### Header

**Description:** A user defined unique identifier, that corresponds to the [emissions rate source](#emissions_rate_source-propagating-parameter) references used in the virtual world parameters or in the infrastructure files.

**Notes on acquisition:** User defined

#### Data Use

**Description:** Describes way the numerical information in the column is utilized. Valid inputs are:

- `sample`: Sample random values as emission rates from the list provided
- `dist`: Generate random values to use as emissions based on the distribution shape and scale provided

#### Distribution Type

**Description:** The name of a distribution from the scipy library, only relevant if the [data use](#data-use) set to `dist`.

**Notes on acquisition:** See [scipy documentation](https://docs.scipy.org/doc/scipy/reference/stats.html) for more details.

#### Maximum Emission Rate

**Description:** The maximum possible emission rate that can be sampled from a distribution, in grams per second.

#### Units (amount)

**Description:** Units of the amount measurement used for inputs of emissions.  Can be one of:

- gram
- kilogram
- cubic meter
- tonne
- pound
- cubic feet
- liter
- mscf

**Notes on acquisition:** User defined

**Notes of caution:** All units are converted into base grams per second. Conversions are based on standard atmospheric temperature and pressure conditions and may have slight variations.

#### Units (time)

**Description:** The time units for the inputs of emissions. Can be one of:

- second
- minute
- hour
- day
- week
- month
- year

**Notes on acquisition:** User defined

**Notes of caution:** All units are converted into base grams per second. Conversions are based on standard atmospheric temperature and pressure conditions and may have slight variations.

#### Source (Emission file)

**Description:** Each following row defines a single input. Depending on the [data use](#data-use) input, the values specify either individual emission rates (`sample`) or the shape and scale of the distribution (`dist`).

- sample: Each row is a single emission value. LDAR-Sim randomly selects one of these values to generate a new emission.
- dist: Each row becomes an input to describe the distribution shape. LDAR-Sim generates a random number based on this distribution for each new emission.

**Notes of caution:** The sources of emissions should align with the [emission production rates](#emissions_production_rate-propagating-parameter).  For instance, if the emission sources identified here originate from a screening that only detects emissions above a minimum threshold of 10 kg/hr and occurs infrequently, the [emission production rates](#emissions_production_rate-propagating-parameter) should also be derived from these specific screenings. They should not be based on surveys conducted at the same site that reported a significantly higher number of emissions, with different rates.

--------------------------------------------------------------------------------

## 11\. Legacy Inputs

As LDAR-Sim continues to advance, certain parameters may become obsolete and consequently removed from the current version. This section will comprehensively list such parameters, along with the version in which they were removed and, if applicable, their replacements.

--------------------------------------------------------------------------------

### Legacy Simulation Settings Parameters

#### &lt;reference_program&gt;

- Removed as of version 4.1.0

The reference program functionality has been temporarily removed to avoid confusion. It will be reinstated once it is re-implemented and becomes relevant.

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

### Legacy Virtual World Settings Parameters

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

### Legacy Program Parameters

#### &lt;verification_cost&gt;

- Removed as of version 4.0.0

#### &lt;carbon_price_tonnes_CO2_equivalent&gt;

- Removed as of version 4.0.0

--------------------------------------------------------------------------------

## 12\. Data sources, modelling confidence and model sensitivity

There are a broad range of inputs used in LDAR-Sim that must be derived from various sources. Each of these parameters should be carefully considered and understood before using LDAR-Sim to inform decision making. Like other models, the quality of simulation results will depend on the quality and representativeness of the inputs used.

The sensitivity of modeling results to inputs will vary on a case-by-case basis. In general, it is best to assume that all parameters in LDAR-Sim are important before modeling begins. It is strongly recommended to perform sensitivity analyses each time LDAR-Sim is used in order to understand the impact that uncertainty in inputs might have on results. Each LDAR program is unique in many ways. Therefore, there is no universal set of rules or guidelines to indicate _a priori_ which parameters will have the greatest impact on results.

In the same way, the confidence in the accuracy of input data can only be determined by the user who provides the data. For example, if provided an empirical leak-size distribution consisting of only 5 measurements, LDAR-Sim will run and generate results without generating warnings. It is the responsibility of the user to have sufficient experience to understand how LDAR-Sim processes different types of data so that they can confidently provide high quality inputs.

In terms of data source, inputs can come from oil and gas companies, technology providers, or solution providers. Some parameters and inputs can also be sourced from peer reviewed literature or can be used simply as experimental levers to explore different scenarios within LDAR-Sim. The lists below provide a general overview of what stakeholders will _generally_ be responsible for different parameters and inputs. Exceptions will always exist, and may vary according to the purpose of modeling, the jurisdiction, and the scope of the modeling exercise. In general, we strongly suggest deriving method performance metrics from single-blind controlled release testing experiments.

Below are some examples of common sources of LDAR-Sim data. Not all parameters are covered. In the absence of operator-specific data, published estimates can be used.

### Duty Holder / Operator (historical LDAR data)

- [emissions_file](#emissions_file)*
- [emission production rate](#emissions_production_rate-propagating-parameter)*

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
