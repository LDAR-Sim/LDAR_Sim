# The LDAR Simulator V3.3

See changelog [here](changelog.md)

## About LDAR-Sim

The Leak Detection and Repair Simulator (LDAR-Sim) is an open-source modeling framework for exploring the effectiveness of methane leak detection programs. The purpose of LDAR-Sim is to enable transparent, collaborative, flexible, and intuitive investigation of emerging LDAR technologies, methods, work practices, regulations, and deployment strategies.

LDAR-Sim has many potential uses, including:

  1) Test emissions reduction equivalence among distinct LDAR programs
  2) Evaluate performance and cost of methane sensing technologies and work practices
  3) Predict the emissions mitigation of proposed or existing fugitive methane policies
  4) Inform the development and niche of technologies and work practices

To learn more about LDAR-Sim, you can:

  1) User [manual](USER_MANUAL.md)
  2) Read our [story map](https://arcg.is/1rXeX10) (less technical introduction).
  3) Read [Fox et al., 2021](https://www.sciencedirect.com/science/article/pii/S0959652620352811).

For first time users, we recommend attempting to reproduce the case study results in Fox et al. 2021 (see below).

Thomas Fox: thomas@highwoodemissions.com

Mozhou Gao: mozhou.gao@ucalgary.ca

Thomas Barchyn: tbarchyn@ucalgary.ca

Chris Hugenholtz: chhugenh@ucalgary.ca

## LDAR-Sim Licensing and Use

LDAR-Sim was invented by Thomas Fox, Mozhou Gao, Thomas Barchyn, and Chris Hugenholtz at the University of Calgary's Centre for Smart Emissions Sensing Technologies.

LDAR-Sim is free software: you can redistribute it and/or modify it under the terms of the MIT License. LDAR-Sim is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose.

NOTE: This applies to all versions following Commit 69c27ec, Made on March 1st, 2021, Previous versions of LDAR-Sim were licensed under the GNU Affero General Public License. All redistributions or modifications made on LDAR-Sim versions created before Commit 69c27ec (March 1st, 2021) are required to be in compliance with version 3 of the GNU Affero General Public License.

## [Fox_etal_2020 Release](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020)

The Fox et al. 2020 release is immortalized in a separate branch that can be found by [clicking here](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020).

The Fox et al., 2020 release contains the exact code and inputs used in [our LDAR-Sim synthesis paper](https://www.sciencedirect.com/science/article/pii/S0959652620352811). We recommend using this release, especially for first time users.

Citation for this release: Fox, Thomas A., Mozhou Gao, Thomas E. Barchyn, Yorwearth L. Jamin, and Chris H. Hugenholtz. "An agent-based model for estimating emissions reduction equivalence among leak detection and repair programs." Journal of Cleaner Production (2021): 125237.

### Getting started

This guide is intended to get a user running with LDAR-Sim, **note** that even though we have supplied default variables, these should be used with caution, as many are not fully understood, are dependent on specific company workpractices, and vary by geographical region.

#### Step 1: Before you begin

Read and understand the LDAR-Sim LICENSE (MIT License).
Read the user [manual](USER_MANUAL.md).

Read [Fox et al 2021](https://www.sciencedirect.com/science/article/pii/S0959652620352811) to familiarize yourself with LDAR-Sim fundamentals.

#### Step 2: Installing Packages with Conda

Using Conda (Conda-forge) and the requirements file included in the "install folder" Follow the directions included in the Setting Up LDAR Sim Dev Environment file. The requirements.txt file can also be used with PIP and pipenv, but Python should be installed separately.

- Install Miniconda3 newest version
- From Conda Shell: cd into LDAR-Sim/install

  `conda config --add channels conda-forge`

  `conda config --set channel_priority strict1`

  `conda create -n ldar_sim --file requirements.txt`

  `conda activate ldar_sim`

Alternatively pip and pipenv can be used to install the requirements file with:

  `pip install ldar_sim -r requirements.txt`

if you are using satellite modules orbit predictor needs to be added to environment

  `pip install orbit_predictor==1.14.2`

#### Step 3: Get Weather and Facility Data

The application requires both facility and weather data to run. We have included sample facilities and weather data for Alberta as an example. Check out the [user manual](USER_MANUAL.md) for more information on formatting of facility data. Weather data can either be downloaded manually, or ERA5 data can be downloaded directly from Copernicus using the /module_code/weather/ERA5_downloader.py module (see file for instructions). Note the output data is in hourly format, therefore the flag weather_is_hourly should be set to True. Multiple ERA nc files can be concatenated with ERA5_concat.py.

#### Step 4: Populate the simulation folder with Programs and associated methods

The simulation files allow a user to set simulation_setting / virtual_world / program/ and method parameters. If a parameter is not included in the file a default value will be used. One simulation_settings file, one virtual world file and at least one Program File is required for running the program while method files are required for running a method.

##### Example

A simulation settings yaml file is required, the most basic setup is as follows (note that P_OGI and P_none are required):
Simulation_settings.yaml =>

``` yaml
  parameter_level: simulation_settings     // Denotes the parameter level (used for input handling)
  version: '2.0'              // Denotes the version
  reference_program: P_OGI    // Denotes the regulatory reference program for relative differences
  baseline_program: P_none    // Denotes a baseline program for estimating program mitigation, usually in place of no formal LDAR
```

P_OGI.yaml =>
A Program yaml file is required, the most basic setup is as follows (where a method Label points at a global parameter):

``` yaml
  program_name: P_OGI           // Denotes program name (must be unique)
  parameter_level: program      // Denotes the program level (used for input handling)
  version: '2.0'                // Denotes the version
  method_labels:                // Denotes the associated methods
    - OGI 
```

P_none.yaml =>

``` yaml
  program_name: P_none
  parameter_level: program
  version: '2.0'
  method_labels: []

```

M_OGI.yaml =>

A Method yaml file is required, the most basic setup is as follows:

``` yaml
    parameter_level: method         // Denotes program name (must be unique)
    version: '2.0'                  // Denotes the version
    label: OGI                      // Specify the label to link to an associated program
    deployment_type: mobile         // How the technology operates, 'mobile', 'stationary' or 'orbit'
    measurement_scale: component    // Does the sensor measure at a site level, equipment level or component level
    is_follow_up: False             // Does the technology survey sites after a screening technology flags the site.
    sensor:                     
      MDL: [0.0362]                 // Minimum detectable leak in g/s.
    cost:
      per_site: 600                 // Cost per site survey ($)
    t_bw_sites: 
      vals: [30]                    // Time to travel between sites (minutes)
    RS: 2                           // Surveys required per year per site (ie. 2 surveys per site every year)
    time: 120                       // Time to perform detection at a site (minutes)
```

Check out the [user manual](USER_MANUAL.md) for more info on the parameters.

#### Step 5: Run the program

The main program is a python script called LDAR_Sim_main.py. Within the virtual environment (or where all py packages are installed) run:

 ```Python LDAR_Sim_main.py {SS_XXX} {VW_XXX} {P_XXX} {M_YYY}```

  where each argument is a path to a simulation settings, virtual world, program, or method input parameter file. for example:

```Python LDAR_Sim_main.py ./simulations/Simulation_settings.yaml ./simulations/virtual_world.yaml ./simulations/P_aircraft.yaml ./simulations/P_none.yaml ./ simulations/M_aircraft.yaml ./simulations/M_OGI_FU.```

alternatively, an entire directory can be passed using the "-P", "--in_dir" flags where all files within the directory are added to the program. for example:

 ```Python LDAR_Sim_main.py --in_dir ./simulations```

 will load all files in the simulations folder into the program.

 Output files, including maps, charts and csv files will be generated and placed in the output folder.

 **Note**: that you can use absolute references or relative, where the root folder is this folder.

## Other versions

Several LDAR-Sim advances are not publicly available at this time, including more advanced equivalence scenario modeling, specific method modules, and cost-effectiveness comparisons.

## Contributions and collaboration

The Included python code follows strict PEP8 Standards for formatting with a modification to the Line Length rule, where lines cannot exceed 100 characters. Contributed code will be rejected if it does not meet this standard. We suggest using PEP8 autoformatters and Linting (Flake8 , Black) when making contributions.

When submitting Issues, Commits and Pull Requests, please use the provided templates to ensure consistent format. For instructions on how to setup the LDAR-Sim commit message template please see the [Setup Instructions](LDAR_Sim/install/SetupInstructions.md)

The authors welcome all contributions and collaborations. Please reach out - we would love to hear from you and/or work with you!
