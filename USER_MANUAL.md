# LDAR-Sim Documentation for Input Parameters and Data

Github Repository: IM3S

Version: 2.0

Branch: Master

Document Custodian: Thomas Fox

Email: thomas@highwoodemissions.com

--------------------------------------------------------------------------------

## 1\. Read This First

Please note the following before reading, using, or modifying this document:

- The purpose of this document is to introduce LDAR-Sim, provide guidance for use, and catalogue input parameters, files, data, and arguments required to run the LDAR-Sim model.
- The document you are now reading will _always_ be associated with a specific version or branch of LDAR-Sim. Multiple versions of this document therefore exist, as multiple versions and sub-versions of LDAR-Sim exist.
- **If you are submitting a pull request to the public LDAR-Sim repo**, please update this documentation alongside modifications to code. Your pull request will not be approved without updating this document with relevant changes to inputs, how they work, and their implications for outputs.
- Within each category, please maintain alphabetic ordering on contents.
- For more information on LDAR-Sim, including code, instructions, and additional resources, please visit the Github page by [clicking this link](https://github.com/tarcadius/LDAR_Sim).
- If you find any errors or inaccuracies in this documentation or in LDAR-Sim, please contact the document custodian (email included above).

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

  - inputs
  - install
  - outputs
  - src
  - simulations

- CHANGELOG.md

- LICENSE.txt
- README.md
- USER_MANUAL.md

The **Root** folder includes all code, inputs, and outputs necessary to run LDAR-Sim. From a software perspective, the root folder is the parent to the src folder (folder containing LDAR_sim_main). This folder will be always be the root folder when making relative references in LDAR-Sim. For example, if input_directory is specified as_ ./inputs _from anywhere in the code, the targeted folder will be_ {absolute_path_to} / Root / inputs_.

The **inputs** folder contains input files required to run LDAR-Sim. These include airport files, empirical leak and vent data, facility lists, facility type defaults, and other inputs.

The **outputs** folder stores all output data files produced by LDAR-Sim. The folder is cleaned, and added if required each time ldar_sim_main is run.

The **src** folder stores the python source code. The main code of LDAR-Sim, LDAR_sim_main.py is stored in the base folder of src.

The **simulations** stores >V2 input parameter files.

--------------------------------------------------------------------------------

## 4\. Running the Model

To run the model, supply one or more input parameter files as arguments to the program. The main function is called `ldar_sim_main.py` and is the main entrypoint to the model. File paths can be relative to the root directory (e.g., `./parameter_file1.yaml`) or absolute (e.g., `D://parameter_files//parameter_file1.yaml`). File paths are positional arguments and should be seperated by a single space.

```buildoutcfg
python ldar_sim_main.py parameter_file1.yaml parameter_file2.yaml
```

Alternatively, a single folder name (absolute or relative to root) can be passed by flagged argument _-P_ or _--in_dir_. All json or yaml files within that folder will be added as parameter_files. For example the following will use all parameter files within the sample simulation folder:

```buildoutcfg
python ldar_sim_main.py --in_dir ./simulations
```

We recommend running the model with a working directory set to /LDAR_Sim/src.

### Parameter File Structure

Parameter files are all key-value pairs (i.e., Python dictionary), with multiple levels of nesting. The model runs with 3 main levels in a hierarchy:

- `global`: global parameters that are common across all programs in a simulation or set of simulations such as system parameters, etc.
- `program`: program parameters that relate to a specific emissions reduction program (or lack thereof), of which there could be multiple within a given simulation. Commonly, an 'alternative' custom program is compared to a defined regulatory program. Many programs can be compared at once.
- `method`: emissions reduction methods (e.g., specific LDAR technologies and work practices and/or LDAR service provider companies) that are deployed within a program. Methods are specified in a given program for deployment and multiple methods may be used at once (e.g., satellite + aircraft + OGI follow-up + routine AVO)

Although a single program can be evaluated on its own, a typical simulation would compare at least two programs: a reference program and one or more test programs. Including a baseline program is also common.

- `baseline program`: The program against which mitigation is estimated for reference and test programs (mitigation = baseline emissions - LDAR emissions). Typically involves running LDAR-Sim in the absence of a formal LDAR program (commonly denoted as 'P_none'). Even without a formal LDAR program, leaks are eventually removed from the simulation due to operator rounds (e.g., AVO), routine maintenance, refits and retrofits, or other factors.
- `reference program`: The program against which test programs are compared (e.g., to establish equivalency). The reference program is often defined by regulations that require the use of OGI (commonly denoted 'P_OGI').
- `test program`: A custom alternative program that the user wants to evaluate. Commonly denoted using 'P_' + program name (e.g., 'P_aircraft', 'P_GasCompanyX', 'P_drone', etc.).

A simulation can consist of any number of programs and each program can consist of any number of methods. For example, the reference program could deploy one method (OGI). The test program could deploy two new LDAR methods (magical helicopter and unmagical binoculars). Each program would be run on the asset base multiple times through time to create a statistical representation of the emissions and cost data. Finally, the statistical emissions and cost distributions of the reference program can be compared to those of the test program. It is often the differences between the programs that represents the important information that is of interest to users of LDAR-Sim.

In this example, the hierarchy looks like:

```yaml
Global parameters
Programs:
    Baseline program
    Reference program:
        Reference LDAR method (OGI)
    Test program:
        New LDAR method 1 (Magical Helicopter)
        New LDAR method 2 (Unmagical Binoculars)
```

### Parameter file usage

We recommend supplying LDAR-Sim with a full set of parameters, copied from the default parameters in the `default_parameters` folder and modified for your purposes. This will ensure you are familiar with the parameters you have chosen to run the model.

However, it may be more convenient once you are familiar with how parameter files update each other to use multiple parameter files to create your simulations and rely upon the default parameters.

All simulations using multiple parameter files are created the following way:

1. Default parameters in the `inputs` folder are read into the model.
2. Each parameter file is read on top of the respective parameter set, updating only the keys that are supplied.

Parameter files are read on top of each other, starting with the default set of parameters. How does this work? Here is an example `parameter_file1.yaml`:

```yaml
version: 2.0
n_simulations: 30
LPR: 0.0065
```

This will revise the `n_simulations` key to 30, from whatever was default, and the `LPR` key to 0.0065, from whatever was default. Next, `parameter_file2.yaml` is read, which looks like this:

```yaml
version: 2.0
n_simulations: 3
```

This will replace the `n_simulations` key with 3 (instead of 30), but leave the `LPR` key, and all other parameters in the model untouched. The model will now run with parameters that look like this:

```yaml
version: 2.0
n_simulations: 3
LPR: 0.0065
.... ALL OTHER PARAMETERS RUN WITH DEFAULT VALUES ....
```

Keep in mind that only 2 parameters have been changed with these parameter files - all other parameters run with the default values. We have attempted to choose representative defaults, but be aware the default values may not be what is appropriate for your use case - _it is your responsibility to verify the default parameters are appropriate_.

In this example, changing the `n_simulations` key to 3 makes the model run faster and provides a way to test the model without waiting for it to complete 30 simulations. A reasonable workflow with these parameters would be something like running the model in a test configuration with:

```buildoutcfg
python ldar_sim_main.py parameter_file1.yaml parameter_file2.yaml
```

Then, when comfortable understanding the outputs and ready to run the model for longer to get more statistically valid results, run:

```buildoutcfg
python ldar_sim_main.py parameter_file1.yaml
```

The model will now run for the full 30 simulations because we did not load `parameter_file2.yaml` and the `n_simulations` key did not get overwritten to 3\. Essentially `parameter_file2.yaml` is a run configuration for testing, it is something you could add onto any simulation you like to test out the configuration, then drop it when you are ready to get more robust results.

To ensure reproducibility, the full set of parameters (all defaults plus any that are specified and overwritten) are written to the output directory so the model run can be transparently reproduced or interrogated.

Keep in mind that the **order matters** because LDAR-Sim reads in parameter files in the order that they are provided - if you change around the order of parameter files, the outcome will be different.

The example above focused on demonstrating a run configuration, but the parameter file functionality is designed to be used to enable modularization. For example, parameter files can be modularized into categories like:

- specific asset bases and infrastructure types
- specific program definitions
- specific method definitions
- specific run configurations (e.g., as example above)
- specific scheduling configurations
- specific computer systems

For example, running an existing program with an existing collection of methods in a new jurisdiction could be as simple as just revising the asset parameter file to the new set of sites, leaving the other parameter files untouched.

While global parameters are straightforward to specify this way (and the above example shows how to do this), a few extra parameters are required to directly specify programs or methods, which are at different levels in the hierarchy.

### LDAR-Sim Parameter Hierarchy

As noted above, LDAR-Sim uses a 3 level hierarchy of simulations, programs, and methods. To tell LDAR-Sim what level in the hierarchy your parameter file is destined for, you must specify a `parameter\_level` parameter that will specify what level your parameter file is aimed at - otherwise LDAR-Sim will interpret it as global.

The `parameter_level` parameter can be one of three values:

- `global`: parameters are aimed at the global level.
- `program`: parameters are used to define a program.
- `method`: parameters are used to define a method and update a given method by name.

There are special considerations for methods:

- All methods require a unique `label`. This is use internally as a unique id, and is required to utilize `_RS` and `_time` variables from the facility file.
- All methods require a `deployment_type`. This can be custom coded following the `template_crew` and `template_company` modules or one of the prebuilt methods can be used:

  - `mobile`: Agent moves between sites. Surveys occur when a site is "ready" for a survey and a crew is available to survey.
  - `stationary`: Each site has one or more _fixed_ sensors. Surveys are carried out daily.
  - `orbit`: Agent 'orbits' site and performs surveys at regular intervals.

- All methods require a `measurement_scale`. This can be one of:

  - `site`: Sensor measures the aggregate of all leaks at site.
  - `equipment`: Sensor measures the aggregate of all leaks at within a single equipment group.
  - `component`: Sensor measures each individual leak.

- All methods require a `sensor` This can can either be custom built or one of the following can be used:

  - `default`: Uses a simple threashold where the leak rate is based on the measurement scale, for example if `measurement_scale = site` then the site's total emissions will be considered measured if greater than the sensors MDL. -`OGI_camera`: Uses detection curve based on Ravikumar, 2018.Requires measurement_scale = 'component'.

- Follow up technologies need to be set explicitly. `is_follow_up = True`. The default value is false
- Third, because methods are often carefully designed and used in treatment / control experiments, it is helpful to allow reuse of specific methods by referring to methods by their `label`.

Consider the following simulation:

```yaml
Global parameters
Programs:
    Reference program:
        Reference LDAR method
    Test program 1:
        New LDAR method 1
    Test program 2:
        New LDAR method 1
        New LDAR method 2
```

Here, there is a situation where `New LDAR method 1` is used in both `Test program` and `Test program 2`. The definition for `New LDAR method 1` can and should be specified only once and reused as it is common among two test programs. However, the two programs may differ in _how_ they implement the same method (e.g., different basins).

To specify this, we can refer to the program by name in the program definitions with the addition of the `method_labels` parameter to our program. Note, we leave the `methods` key empty as the specified `new_LDAR_method_1` will be injected in at runtime.

```yaml
test_program_1:
    version: '2.0'
    parameter_level: program
    method_labels: [new_LDAR_method_1]
    methods: []
    .... OTHER PROGRAM PARAMETERS ....
```

This `new_LDAR_method_1` has to be defined elsewhere in a separate parameter file to be called by name.

```yaml
new_LDAR_method_1:
    version: '2.0'
    parameter_level: method
    label: new_LDAR_method_1
    .... OTHER OGI METHOD PARAMETERS ....
```

When the simulation is put together, the program will be assembled to look like this:

```yaml
test_program:
  version': '2.0',
  parameter_level: program,
  method_names: [new_LDAR_method_1],
  methods: [
    new_LDAR_method_1: {
    parameter_level: method,
    label: OGI,
    .... OTHER OGI METHOD PARAMETERS ....
  .... OTHER PROGRAM PARAMETERS ....
```

To review, the following parameters are necessary to enable this modularization and reproducibility within the parameter suites:

`parameter_level`: `global`, `program`, or `method`, this defines the target level in the hierarchy. Without specification, LDAR-Sim interprets the parameters as global.

`label`: in method definitions `label` provides a unique name to refer to each method.

`type`: in method definitions `type` provides a lookup for checking parameters and allows lookup of default parameters, which enables partial parameter specification and out of the box reverse compatibility.

`method_labels`: shorthand method to specify methods by their labels, and include them in more than one program or simulation easily and reliably. Used only in programs.

### Parameter File Formats

LDAR-Sim includes a flexible input parameter mapper that accepts a variety of input parameter formats. Choose the one that you like the best. [YAML](https://en.wikipedia.org/wiki/YAML) is the easiest to read for humans, allows inline comments, and is recommended. The following formats are accepted:

- yaml files (extension = '.yaml' or '.yml')
- json files (extension = '.json')

For example, here is a program definition in yaml:

```buildoutcfg
version: '2.0'
parameter_level: program
```

Here is a method definition in yaml:

```buildoutcfg
version: '2.0'  
parameter_level: method
awesome_method:
  label: awesome_method
```

Note that programs are interpreted as a flat list of parameters that are incorporated into a list where methods have one parameter (the method name), and other method parameters nested below.

### Versioning of Parameter Files

All parameter files must specify a version to enable mapping and reverse compatibility. This versioning is used to call code that modifies a different version of the code to run properly. In cases this is simple mapping of parameters, in other cases, this involves calculations. Refer to `input_mapper_v1.py` for a template file and discussion document on input parameter mapping. Reverse compatibility mapping only exists for v2 forwards.

### Notes for Developers

If you are developing in LDAR-Sim, please adhere to the following rules:

1. All parameters must be documented, refer to the examples below on the precise format.

2. All parameters must sit in a key-value hierarchy that semantically makes sense and can be understood by the diversity of users that use LDAR-Sim.

3. All parameter files require `parameter_level` to define the position within the hierarchy.

4. If adding new functionality - please set the default to be 'off' or otherwise reverse compatible with existing functionality - this allows test simulations to run properly. Keep in mind older parameter files will use this default without realizing it, and if the behaviour of LDAR-Sim changes, you must add appropriate mapping hooks to the input mapper such that upon detecting an older parameter file, parameters are set to run identical to the old model.

5. Please do not modify parameters in the program during simulation - consider parameters as 'read only' throughout the simulation.

--------------------------------------------------------------------------------

## 5\. Global Inputs

### baseline_program

**Data type:** String

**Default input:** 'P_none'

**Description:** A program that represents a scenario where there is no formal LDAR, or that has no LDAR methods. This is currently used for economic functions.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### end_date

**Data type:** List of integers [year, month, day]

**Default input:** [2020,12,31]

**Description:** The date at which the simulations ends.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** We recommend running the simulation for several years due to the stochastic nature of LDAR systems and the periods of time over which leaks arise and are repaired.

### input_directory

**Data type:** String

**Default input:** "./inputs"

**Description:** Specify location containing input files like infrastructure and weather. Can be an absolute path, or relative path to the root folder.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### n_processes

**Data type:** Integer or None

**Default input:** None

**Description:** The number of parallel processes to use. None = all available processes, 1 = one virtual core, and so on. We recommend using None to greatly reduce simulation run time.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Using None will require almost all of your computer's total processor utilization across all cores. If background tasks require CPU (e.g., OneDrive, internet browser) your computer may crash.

### n_simulations

**Data type:** Integer

**Default input:** 3 (much more required to constrain uncertainty)

**Description:** The number of repeat simulations to perform for each program.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Using more simulations leads to better-constrained results but requires greater run time. For high-consequence scenarios that are meant to inform decision-making, we recommend using 10+ simulations for each scenario modeled. A minimum of two simulations is required to compare a set of different LDAR programs.

### output_directory

**Data type:** String

**Default input:** './outputs'

**Description:** Specify folder location to generate output files into. Can be an absolute path, or relative path to the root folder.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### reference_program

**Data type:** String

**Default input:** 'P_OGI'

**Description:** The program against which alternative or test programs are compared, which is used to create relative emissions and cost output graphs. Often this is regulatory OGI.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### pregen_leaks

**Data type:** Boolean

**Default input:** False

**Description:** If set to True, leaks will be generated prior to running the simulations. This can be used to test a set of program simulations with the same leaks and the same sites. This can reduce modelling uncertainty when comparing two programs with a limited number of simulations, especially from very large leaks.

If enabled, the leaks will be stored locally in /inputs/generation after running (this also enables users to share leaks used to test programs, which enhances transparency and reproducibility). On subsequent simulations the user will be prompted to use the stored data or to regenerate. At this time, input parameters are not checked, therefore the user should generate new leaks after changing input parameters.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### preseed_random

**Data type:** Boolean

**Default input:** False

**Description:** If set to True, a timeseries of daily random integers will be created, and passed into each program, where each program within a simulation set receives the same timeseries. Then within each day of the simulation, the numpy and random seeds are set using the daily integer. This ensures that the output values will be the same in identical programs regardless of the stocastic nature of the software.

**Notes on acquisition:** N/A

**Notes of caution:** This should only be used for QC and testing.

### print_from_simulations

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to indicate whether to print informational messages from within the simulations. These messages can have value when debugging or troubleshooting.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### start_date

**Data type:** List of integers [year, month, day]

**Default input:** [2017,1,1]

**Description:** The date at which the simulations begins.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** The NetCDF file should encompass the start date and end date.

### version

**Data type:** String

**Default input:** N/A

**Description:** Specify version of LDAR-Sim. See section _Versioning of Parameter Files_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### write_data

**Data type:** Boolean

**Default input:** True

**Description:** A binary True/False to activate the export of simulation data to csv files. Generally recommended that this remains set to True unless it is desired to reduce time/storage requirements during sensitivity analyses.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be True to make automated maps and plots.

--------------------------------------------------------------------------------

## 6\. Program Inputs

### economics

#### carbon_price_tonnesCO2e

**Data type:** Numeric

**Default input:** 40.0

**Description:** The current federal price on carbon in Canada of $40/tonne CO2e is input as a default metric to compare the cost to mitigation ratios of LDAR programs to.

**Notes on acquisition:** See economic section below.

**Notes of caution:** See economic section below.

#### cost_CCUS

**Data type:** Numeric

**Default input:** 20

**Description:** The cost of pure stream CCUS was taken from the International Energy Agency's (IEA) report here: <https://www.iea.org/commentaries/is-carbon-capture-too-expensive>. It offers another metric to compare the cost/mitigation ratios of LDAR programs to.

**Notes on acquisition:** See economic section below.

**Notes of caution:** See economic section below.

#### cost_low_bleed_pneu_tCO2e

**Data type:** Numeric

**Default input:** 875.0

**Description:** Similar to the carbon price and cost of CCUS, the cost of low bleed retrofits can be compared to LDAR program cost/mitigation ratios for context.

**Notes on acquisition:** See economic section below.

**Notes of caution:** See economic section below.

#### GWP_CH4

**Data type:** Numeric

**Default input:** 28.0

**Description:** GWP of 28 over a 100-year time period was chosen as a default input. The model uses this value to convert between CH4 and CO2e when required. This value can be changed to 84-86 over 20 years to explore the impact that GWP has on mitigation costs.

**Notes on acquisition:** See economic section below.

**Notes of caution:** See economic section below.

#### repair_cost

**Data type:** Integer

**Default input:** N/A

**Description:** The average cost of leak repair. This value is added to the total program cost each time a leak is repaired, whether as a result of an LDAR program or due to routine maintenance by the operator.

**Notes on acquisition:** The duty holder should have data on cost of repairs.

**Notes of caution:** Cost of repair is highly variable and not well characterized by a single value. For example, a percentage of leaks will have near-zero repair costs if it is just a matter of tightening a valve. Other repairs, especially if specialized equipment is involved, could be extremely expensive – especially if a shutdown is required and production declines, leading to indirect costs. Those with good data and an intimate understanding of LDAR-Sim may opt to reprogram the model to accept a distribution of repair costs associated with different kinds of repairs – this could greatly improve LDAR cost estimates.

#### sale_price_natgas

**Data type:** Numeric

**Default input:** 3.0

**Description:** The sale price of natural gas which is used to calculate the potential value of gas sold when captured as part of an LDAR program. LDAR-Sim takes the difference in emissions from a baseline scenario and multiplies this by the price of natural gas.

**Notes on acquisition:** See economic section below.

**Notes of caution:** See economic section below.

#### social_cost_CH4_tonnes

**Data type:** Numeric

**Default input:** 1406.0

**Description:** Currently Unused

**Notes on acquisition:** See economic section below.

**Notes of caution:** See economic section below.

#### verification_cost

**Data type:** Integer

**Default input:** 0

**Description:** The average cost of repair verification. This value is added to the total program cost each time a repair is verified. Some regulations require verification of successful repair within a certain number of days following repair. If the operator is already onsite and can easily verify the repair with readily available instruments (e.g., FID), the cost of verification could be negligible. If the operator has to drive long distances or engage an independent service provider to verify repairs, costs could be high.

**Notes on acquisition:** The duty holder should have data on cost of verification.

**Notes of caution:** Cost of verification is likely to be facility specific. Modelers with good data and an intimate understanding of LDAR-Sim may opt to reprogram the model to accept a distribution of site-level verification cost estimates.

**Notes on acquisition (economics):** The default values for these parameters represent generic costs of mitigation options and a conservative price for natural gas. Firms may have unique costs for carbon taxes based on the regulatory jurisdiction where their operations are located, CCUS, or low bleed retrofits that they want to input into the model. If not, default parameters can be used, or information from the IEA and RFF report from Munnings and Krupnick (2017) can be used to derive alternative values. Provinicial/State or Federal government websites should have carbon pricing scenarios available online.

**Notes of caution (economics):** The value used for the cost of low bleed retrofits from Munnings and Krupnick (2017) is based on a national marginal abatement cost curve for methane abatement technologies in the U.S. O&G sector. As a result, this cost may not be truly representative of the costs for low bleed retrofits at sites in the O&G sector under LDAR regulations.

### emissions

#### consider_venting

**Data type:** Boolean

**Default input:** N/A

**Description:** A binary True/False to activate the presence of vented emissions. We do not recommend a default, as the importance of vented emissions varies by LDAR program. With only close-range methods (e.g., OGI), the presence of vented emissions should not matter, as technicians operating close-range instruments should be able to perform the classification. For screening technologies, which cannot distinguish vented from fugitive emissions, including vented emissions will result in a more realistic depiction of program performance, especially if only fugitive emissions are being targeted.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Screening technology performance will typically suffer if only fugitive emissions are being targeted due to the confounding presence of design (e.g., vented) emissions. Results from simulations of screening technologies that do not consider venting are therefore optimistic and unlikely to be representative of true reductions. When vented emissions are considered, it will change what facilities are selected for follow-up by screening technologies.

#### leak_dist_params

**Data type:** List

**Default input:** [-2.776, 1.462]

**Description:** A list describing the empirical leak function from which leak emission rates are drawn. The first term is the distribution scale and and any subsequent terms are the the distribution shape. These are used in conjunction with the leak_dist_type. See scipy documentation for more uses. Because the Lognormal distribution is often used in literature, it is considered a special case where the scale is the mu value , or the log of the scale used by the scipy function `eg. scale = exp(leak_dist_params)[0]`. The default value is a lognormal fit of the clearstone dataset, which were taken from OGI measurements of leaks from Canadian gas facilities.

**Notes on acquisition:** N/A

**Notes of caution:** None

#### leak_dist_type

**Data type:** string

**Default input:** 'lognorm'

**Description:** The name of a distribution from the scipy library, used in conjunction with leak_dist_params. See scipy documentation for more details.

**Notes on acquisition:** N/A

**Notes of caution:** None

#### leak_file

**Data type:** String

**Default input:**"leaks_rates.csv"

**Description:** The leak\_file specifies the leak rates and relevant characteristics of empirical leaks, forming the basis of the leak-rate distribution that is sampled once for each new leak that is generated. At the bare minimum, the csv contains a single column with the heading name _gpersec_. Each cell contains a numeric value representing the emission rate of a real, previously detected, and quantified leak, in grams per second. For many applications, this single column may be sufficient. Additional columns can be included if 'intelligent' sampling of leak rates is to be used. These fields must have matching fields in the infrastructure_file. Examples include facility type, production type, company, and so on. Beyond column A, any column headings can be used, and all data contents are treated as character strings (category labels).

**Notes on acquisition:** It is important that leak rate data are collected using the same instrument that is used to estimate the leak production rate (i.e., both collected using M21 or both collected using OGI). Ideally, LPR and leak data would be collected at the same time and for the same sites.

**Notes of caution:** For non-mandatory columns (columns B onward), the number of leaks required for the distribution should increase exponentially for each new column, because leak rate sampling will become increasingly specific. Categories must also be sufficiently exhaustive to be representative.

#### leak_use

**Data type:** String

**Default input:** "sample"

**Description:** If a leak file is provided, this variable determines how to use it. It can either be set as `sample` or `fit`. If set to `sample`, leaks will be sampled from the file. If set to `fit`, The leaks will be used to generate a distribution specified by the `leak_dist_type`, from which leak rates are generated by pulling from the distribution.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

#### LPR

**Data type:** Numeric

**Default input:** 0.0065

**Description:** A numeric scalar that denotes the leak production rate (LPR). New leaks are generated using a site-level empirical LPR that is independent of the number of leaks already present on site. LPR is the probability that a new leak will arise, each day, for each site. The LPR is an empirical representation of all conditions that lead to the occurrence of leaks, including facility age, management practices, predictive maintenance, and random chance. Currently, a single LPR is used for all facility types, production types, facility ages, and so on. In the future, as more LDAR data becomes available, LPRs could be calculated that are specific to each of these or other variables, or distributions of LPRs could be generated. For an extended discussion on LPR, see Fox et al. (2020).

**Notes on acquisition:** While the "true" LPR is elusive, it can be estimated by dividing the number of leaks found during an LDAR survey at a facility by the number of days that have passed since the previous LDAR survey at the same facility. If this is done for a large number of survey intervals at a large number of facilities, one should eventually converge on a representative estimate. When LDAR-Sim is used, operator-specific LPR values should be estimated if sufficient data exist to do so.

**Notes of caution:** Available techniques for estimating LPR make a number of problematic assumptions. Ultimately, we have relatively poor data on LPR and the relationship between LPR and NRR. Modeling results are extremely sensitive to LPR. Given that LPR is elusive, we strongly recommend that a broad range of LPR values is evaluated in LDAR-Sim before any decisions are made. For more information, refer to discussions in the main text and supplementary information of Fox et al. (2020).

#### max_leak_rate

**Data type:** Numeric

**Default input:** 1000.0 (g/second)

**Description:** The maximum possible leak rate that can be sampled from a distribution.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### subtype_leak_dist_file

**Data type:** List

**Default input:** [False, 'subtype_distributions.csv']

**Description:**

**Notes on acquisition:**

**Notes of caution:** If True, will overwrite global leak distribution.

#### units

**Data type:** List of Strings

**Default input:** ['kilogram', 'hour']

**Description:** Units used for inputs of leak and vent samples / distributions. Consists of two terms, an amount and an increment. the amount can be one of:

- gram
- kilogram
- cubic meter
- tonne
- pound
- cubic feet
- liter
- mscf

The increment can be one of:

- second
- minute
- hour
- day
- year

**Notes on acquisition:** N/A

**Notes of caution:** N/A

#### vent_file

**Data type:** String

**Default input:** "site_rates.csv"

**Description:** The vent\_file specifies the facility-scale emission rates that are resampled alongside leak rate data to generate distributions of design (vented + incomplete combustion) emissions at each site. The csv contains a single column with the heading name _gpersec_. Each cell contains a numeric value representing the emission rate of a real, previously detected, and quantified facility-scale emission rate in grams per second.

**Notes on acquisition:** Established methods should be used, when possible, and data should be representative of the region and facilities of study. Recommended approaches for facility-scale estimates include the tracer-release method, OTM33A, and aerial mass balance, among others.

**Notes of caution:** N/A

### infrastructure_file

**Data type:** String

**Default input:**"facility_list_template.csv"

**Description:** Character string that specifies the name of the csv file that contains all of the required data on the facilities that comprise the LDAR program. At a bare minimum, the csv must contain the following columns: 'facility_ID', 'lat', 'lon'. For each mobile measurement company used as part of the LDAR program, the number of annual surveys (survey frequency) must be indicated and the inspection time for each method indicated (in minutes). The number of fixed sensors used at each site must also be indicated. Subsections 1.7.X describe individual columns in greater detail.

**Notes on acquisition:** See subsections.

**Notes of caution:** Although facility-specific inputs provide flexibility, in most cases the appropriate data will not be available, and the same survey time or survey frequency may be used for all facilities. In general, LDAR-Sim does not hard-code methods, facility types, production types, and so on. These are provided by the user as categorical variables and can be anything. However, categorical variables must be consistent among different input files or errors will occur.

#### facility_ID

**Data type:** String

**Default input:** N/A

**Description:** A character string indicating the unique facility code.

**Notes on acquisition:** Should be available from the facility operator or can be made up.

**Notes of caution:** Must be a unique identifier.

#### lat

**Data type:** Numeric

**Default input:** N/A

**Description:** A numeric scalar indicating facility latitude in decimal degrees.

**Notes on acquisition:** N/A

**Notes of caution:** Should range between -90 (South Pole) and 90 (North Pole). Will be negative for facilities south of the equator. Fewer decimal places or offsets can be used to anonymize location.

#### lon

**Data type:** Numeric

**Default input:** N/A

**Description:** A numeric scalar indicating facility longitude in decimal degrees.

**Notes on acquisition:** N/A

**Notes of caution:** Should be between -180 and 180 (both correspond to the 180th meridian). Will be negative for facilities west of the Prime Meridian and positive for facilities east of it. Fewer decimal places can be used to anonymize location.

#### \*\*\__RS

**Data type:** Integer

**Default input:** N/A

**Description:** For each method, an integer indicating the number of required surveys at each facility per calendar year. The three asterisks indicate the interchangeable method name (e.g., OGI_RS, truck_RS).

**Notes on acquisition:** Survey frequencies can be based on regulatory requirements, company policies, or can be fabricated by the modeler to explore different scenarios.

**Notes of caution:** Note that just because a number of surveys is prescribed, it does not mean that this number of surveys will necessarily be performed. For example, if labour limitations exist (i.e., not enough crews are available to inspect the number of facilities in the program) or if environmental conditions are unsuitable (i.e., a particular facility is in a cloudy location that cannot be accessed by satellite), the performed number of surveys may be less than the prescribed number. This variable is not required for continuous measurement methods.

#### \*\*\_time

**Data type:** Integer

**Default input:** N/A

**Description:** For each mobile method, the number of minutes required to complete a survey at each facility. Three asterisks indicate the interchangeable method name (e.g., OGI_time).

**Notes on acquisition:** In most cases, an estimate will be made as data will not exist for the specific combination of facility and unique method. However, as new methods and programs and implemented, data will become available to better refine modeling estimates and develop more intelligent programs.

**Notes of caution:** This variable is an empirical estimate of how much time is required for a given mobile method to complete a survey at a given facility. This includes anything that happens onsite (e.g., calibrations, interfacing with the operator, etc.) but _does not include_ driving time between facilities or any other account of time spent offsite. This variable is simply the amount of time that passes from the start of a facility survey to the end. If a facility takes longer than there is time left in a day, then the agent/crew returns the following day to continue work, and so on and so forth, until the facility is completed. This variable is not required for continuous measurement methods.

#### fixed_sensors

**Data type:** Integer

**Default input:** N/A

**Description:** An integer indicating the number of fixed sensors installed at each facility.

**Notes on acquisition:** Can be based on regulatory requirements, company policies, or can be fabricated by the modeler to explore different scenarios.

**Notes of caution:** None

#### additional categories

**Data type:** String

**Default input:** N/A

**Description:** Any column heading that helps to refine the numerical sampling process (i.e., 'intelligent' sampling). Common examples include facility type, production type, facility age, etc.

**Notes on acquisition:** Specific to the category chosen and up to the user to define.

**Notes of caution:** Categories used here must correspond with any categories used elsewhere in the model. In particular, when sampling from the leak_file, LDAR-Sim will match the additional categories specified in all files to refine the sampling process and generate emissions information that is representative of the facility for which sampling is being performed. Note that the number of leak rates required for the custom empirical distribution should increase exponentially for each new additional category used, because sampling will become increasingly specific. Categories must also be sufficiently exhaustive to be representative.

### make_maps

**Data type:** Boolean

**Default input:** True

**Description:** A binary True/False to control whether output maps are generated for each simulation. These maps can be used to understand where/when different technologies are effective and where/when deployment blackout periods occur. During runs with a very large number of simulations, setting make_maps to False will reduce run time.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### make_plots

**Data type:** Boolean

**Default input:** True

**Description:** A binary True/False to control whether output plots are generated for each individual run of a simulation. Automatically generating plots provides a broad range of insights into individual simulation runs that can be extremely useful for interpretation. When dozens, 100s, or 1000s of simulation runs are being performed in succession (i.e., for sensitivity analysis or when comparing multiple different programs), plots from individual runs may not be needed and this variable can be turned to False (in these cases, the target information is in the aggregate results, so individual runs can be ignored). Turning this variable to False will reduce the run time of each simulation by a few seconds, which can be significant if the required number of simulations is high.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### method_labels

**Data type:** List of methods

**Default input:** None

**Description:** List of modules used within the program referenced by the method label (see method inputs section - labels for more info). For example, the following will use the aircraft and the OGI_FU methods:

```yaml
method_labels:
- aircraft
- OGI_FU
```

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### NRD

**Data type:** Integer

**Default input:** 150

**Description:** The natural kill date of each leak in number of days. Represents leak removal from the leak pool due to routine maintenance, refits, retrofits, and other unintentional leak repairs.

**Notes on acquisition:** Estimate from empirical data or use previously published value.

**Notes of caution:** This value is highly uncertain and likely depends on context. Sensitivity analyses should be used to explore the impact of different NRd values.

### program_name

**Data type:** String

**Default input:** N/A; Common programs include 'P_none', 'P_OGI', etc.

**Description:** The name of the program. Typical naming convention is 'P_' + some name.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### site_samples

**Data type:** Integer

**Default input:** 500

**Description:** The user can randomly subset/bootstrap all of the sites for a smaller or larger sample of sites. Teis variable is a integer indicating the number of sites to subset.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** This functionality could be used to 'increase' the number of sites in a program, as sampling occurs with replacement. For example, if a program only had 5 sites, sampling of 100 sites would create the illusion of more sites in the program. However, the sites will only represent 5 locations, so if simulations include geographical considerations (e.g. road networks), this may not be advisable as travel times might not be meaningful.

### subtype_times_file

**Data type:** List

**Default input:** [False, 'subtype_times_file.csv']

**Description:** Imports a lookup table that allows the modeler to set the survey time per facility according to facility type. This functionality can be used when survey times are not known for each individual site, but can be approximately estimated by facility subtype. Each row represents a facility type and each column represents a method. Times are the number of minutes that pass between arrival at a facility and completion of the inspection at that facility (exclusive of time between workdays and travel time if a site is too large to finish in any given day).

**Notes on acquisition:** Ideally, empirical data for similar facilities are used to inform the lookup table and that each value represents a representative average based on a reasonable number of surveys

**Notes of caution:** Facility types must match those used in infrastructure_file. When used, subtype_times_file overwrites any facility-specific times present in infrastructure_file.

### version (program level)

**Data type:** String

**Default input:** N/A

**Description:** Specify version of LDAR-Sim. See section _Versioning of Parameter Files_ for more information.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

### weather_file

**Data type:** String

**Default input:** "ERA5_2017_2020_AB.nc" (hourly weather file in Alberta)

**Description:** Specifies the name of the ERA5 NetCDF4 file that contains all weather data to be used in the analysis. Generally, at a minimum, OGI requires wind, temperature, and precipitation data. LDAR-Sim reads in temperature data in degrees Celsius at 2 meters above ground, wind in meters per second at 10 meters above ground, and total precipitation in millimeters accumulated per hour. Other weather variables are freely available for download.

**Notes on acquisition:** Raw data are available from the European Centre for Medium-Range Weather Forecasts. Pre-processed and ready to use weather data have been prepared and are available for download on AWS for Alberta, Colorado, and New Mexico. LDAR-Sim will access these files directly if the file names are specified correctly in the program file. Currently available files are:

- Alberta: "ERA5_AB_1x1_hourly_2015_2019.nc"
- Colorado: "ERA5_CO_1x1_hourly_2015_2019.nc"
- New Mexico: "ERA5_NM_1x1_hourly_2015_2019.nc"

Each of these files provides hourly weather (wind, temp, precip) data spanning the years specified at a spatial resolution of 1 degree latitude and 1 degree longitude. If custom configurations are needed for different regions, spatial resolutions, temporal resolutions, dates, or weather variables (e.g., clouds, snow cover, etc.), they must be downloaded manually from the ERA5 database. The 'ERA5_downloader' python file in the model code folder provides code and guidance for accessing custom weather data.

**Notes of caution:**

Weather file sizes can become quite large, especially when spatial and temporal resolution increase (maximum resolutions of 1.25 degrees and 1 hour, respectively). Modelers must decide how to navigate these tradeoffs, and understand the implications of the resolutions chosen.

If using different weather files for different programs (e.g., when comparing different regions), weather data must be downloaded manually and saved to the inputs folder before beginning simulations, as the automatic downloader built into LDAR-Sim will only download one file at a time.

### weather_is_hourly

**Data type:** Boolean

**Default input:** True

**Description:** Specify if the weather file is ERA5 reanalysis hourly data downloaded directly from ERA5 copernicus database or API. If false, the weather file is assumed to be daily average data generated using the /weather/ERA5_hourly_to_daily.py script.

**Notes on acquisition:** N/A

**Notes of caution:** N/A

--------------------------------------------------------------------------------

## 7\. Method Inputs

### consider\_daylight

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to indicate whether crews should only work during daylight hours. If False, crews work the number of hours specified by the 'max_workday' input variable used for each method. If True, crews work the shorter of either 'max_workday' or the number of daylight hours calculated using the PyEphem package in python using latitude, longitude of each site, for each day of the year. PyEphem accepts two arguments: obs.horizon and obs.pressure.

**Notes on acquisition:** Acquisition is automated using required lat and lon coordinates for each facility (see infrastructure_file input) at each timestep.

**Notes of caution:** In most cases, True and False will yield similar results. Use of daylight constraints should be considered for companies that do not wish to deploy crews in the dark for safety reasons, especially for locations at high latitudes during winter months (e.g., Northern Alberta). However, this functionality should not be used to determine whether sunlight is available for passive remote sensing methods or other technologies that require sunlight operate, as the sun has already set when civil twilight occurs (see obs.horizon). Solar flux will vary with topography and cloud cover (use ERA5 data).

### cost

Method costs. Currency is not important but must be consistent across all inputs.

#### per\_day

**Data type:** Integer

**Default input:** N/A

**Description:** The daily cost charged by the service provider (per crew). It is charged each time a crew is deployed, regardless of how many sites they survey that day.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### per\_hour

**Data type:** Integer

**Default input:** 0

**Description:** The cost charged by the service provider (per crew per hour). The cost includes travel time.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### per_site

**Data type:** Integer

**Default input:** N/A

**Description:** The cost charged by the service provider (per crew per site). It is charged each time a crew is deployed at a site.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### upfront

**Data type:** Integer

**Default input:** N/A

**Description:** The initial up-front cost of each crew. This cost is only charged once.

**Notes on acquisition:** Consult service provider.

**Notes of caution:** Does not account for maintenance activities or the cost of replacing devices after at the end of their lifetime.

### coverage

#### spatial

**Data type:** Numeric

**Default input:** 1.0

**Description:** Probability (0-1) that an agent can locate a leak. Internally, each leak will be randomly assigned a True or False based on this probability indicating whether or not they are covered on the first pass. The leak will be checked if the value is true for the first and all subsequent surveys.

`eg. coverage.spatial = 0.25`. The leak has a 25% chance of being detected regardless of the number of surveys.

**Notes on acquisition:** N/A

**Notes of caution:** Future research is required!

#### temporal

**Data type:** Numeric

**Default input:** 1.0

**Description:** Probability (0-1) that an agent can locate a leak during a survey. Internally, each leak will be randomly assigned a True or False based on this probability increasing survey will improve the chances of the leak being detected.

`eg. coverage.temporal = 0.25`. The leak has a 25% chance of being detected **every time** it is surveyed.

**Notes on acquisition:** N/A

**Notes of caution:** Future research is required!

### deployment_type

**Data type:** String

**Default input:** "mobile"

**Description:** Methods are comprised of both a deployment type and a sensor type. The deployment type is a character string denoting the deployment type used in the method. For instance, 'mobile', 'stationary', or 'orbit'. Custom deployment types can be added and referenced here.

- `mobile`: Agent moves between sites. Surveys occur when a site is "ready" for a survey and a crew is available to survey.
- `stationary`: Each site has one or more _fixed_ sensors. Surveys are carried out daily.
- `orbit`: Agent 'orbits' site and performs surveys at regular intervals.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### follow_up

#### delay

**Data type:** Integer

**Default input:** 0

**Description:** The number of days required to have passed since the first site added to the site watchlist before a site can be flagged. The company will hold all measurements in a site_watchlist. The emissons rate used to triage flagging based on followup threshold and proportion are specified with follow_up.redundancy

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### instant\_threshold

**Data type:** Float

**Default input:** 0.0

**Description:** The follow-up instant threshold in grams per second. Measured site-level emissions must be above the follow-up threshold before a candidate site becomes immediately available for flagging. If _follow_up.instant_threshold_type_ is "absolute", the numeric value indicates the follow-up threshold in grams per second. If "relative", the numeric value is passed to a function that calculates emission rate that corresponds to a desired proportion of total emissions for a given leak size distribution. The function estimates the MDL needed to find the top X percent of sources for a given leak size distribution. For example, given a proportion of 0.01 and a leak-size distribution, this function will return an estimate of the follow-up threshold that will ensure that all leaks in the top 1% of leak sizes are found.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Follow-up thresholds are explored in detail in Fox et al. 2021\. Choosing follow-up rules is complex and work practices should be developed following extensive analysis of different scenarios. It is important to understand how follow-up thresholds and follow-up ratios interact, especially if both are to be used in the same program. Note that follow-up thresholds are similar to minimum detection limits but that the former is checked against to the measured emission rate (which is a function of quantification error) while the latter is checked against the true emission rate.

#### instant\_threshold\_type

**Data type:** String

**Default input:** "absolute"

**Description:** How to establish the follow-up threshold for the instand threshold. Can be "absolute" or "relative". See _follow_up.instant_threshold_ and _follow_up.threshold_ for more information.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** See _follow_up.threshold_ for more information.

#### interaction\_priority

**Data type:** String

**Default input:** "threshold"

**Description:** Specifies which algorithm to run first on candidate sites when determining which to flag. If the value is _threshold_ the proportion of sites to follow up with will be taken from all sites over the threshold. If the value is _proportion_ the proportion of sites will be taken from the candidate sites, then from those sites followup will occur at sites above the threshold.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### proportion

**Data type:** Numeric

**Default input:** 1.0

**Description:** A single value that defines the proportion of candidate flags to receive follow-up. For example, if the follow-up ratio is 0.5, the top 50% of candidate flags (ranked by measured emission rate) will receive follow-up. Candidate flags have already been checked against the minimum detection limit.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** The follow-up proportion ranks sites based on their measured emission rate, which may differ from the true emission rate if quantification error is used. The effect of follow_up.proportion will depend on the temporal interval over which sites accumulate in the candidate flags pool.

#### redundancy\_filter

**Data type:** String

**Default input:** "recent"

**Description:** Specifies which measured emissions rate to use to identify which candidate sites to follow up at if individual sites have multiple independent measurements that have accumulated in the candidate flag pool. If the _follow\_up.delay_ is not zero, crews can survey the site several times before flagging the site. If this value is set to _recent_, the most recent site measurement will be used to check followup threshold and proportion. If the value is set to _max_, the highest emissions rate wil be used. If the value is set to _average_ the average emissions from all surveys will be used.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### threshold

**Data type:** Float

**Default input:** 0.0

**Description:** The follow-up threshold in grams per second. Measured site-level emissions must be above the follow-up threshold before a site can be flagged. If _follow_up.threshold_type_ is "absolute", the numeric value indicates the follow-up threshold in grams per second. If "relative", the numeric value is passed to a function that calculates an emission rate that corresponds to a desired proportion of total emissions for a given leak size distribution. The function estimates the MDL needed to find the top X percent of sources for a given leak size distribution. For example, given a proportion of 0.01 and a leak-size distribution, this function will return an estimate of the follow-up threshold that will ensure that all leaks in the top 1% of leak sizes are found.

The follow-up delay parameter can be set to require multiple measurements for a site above threshold before a site is flagged.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Follow-up thresholds are explored in detail in Fox et al. 2021\. Choosing follow-up rules is complex and work practices should be developed following extensive analysis of different scenarios. It is important to understand how follow-up thresholds and follow-up ratios interact, especially if both are to be used in the same program. Note that follow-up thresholds are similar to minimum detection limits but that the former is checked against to the measured emission rate (which is a function of quantification error) while the latter is checked against the true emission rate.

#### threshold_type

**Data type:** String

**Default input:** "absolute"

**Description:** Can be "absolute" or "relative". See _follow_up.threshold_ for more information.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** See _follow_up.threshold_ for more information.

### is_follow_up

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to indicate whether the method is used to survey sites previously flagged by screening technologies. If true this method will only visit sites flagged.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** No data acquisition required.

### label

**Data type:** String

**Default input:** "OGI"

**Description:** A character string denoting the label of the method.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must match the label name specified in the program input parameter file, and any supplimentary files, such as the infrastructure file.

### MDL (General)

**Data type:** List

**Default input:** [0.01]

**Description:** Minimum detection limit of the screening method in grams per second. Probability curves or surfaces as a function of emission rate, wind speed, distance, etc. must be hard coded.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** A single value for MDL is used here, although a parameter list could be used that defines a sigmoidal probability of detection curve. These are examples and with more experimental data, probability of detection surfaces can be generated that can estimate detection probabilities as a function of numerous relevant variables (e.g., distance, wind speed, emission rate, etc.)

### MDL (OGI)

**Data type:** List of floats

**Default input:** [0.01275, 2.78e-6]

**Description:** A list of parameters [_xₒ_, σ] that define the minimum detection limit of OGI. The two parameters define a sigmoidal Gaussian cumulative probability function as described in Ravikumar et al. (2018), where _xₒ_ is the emission rate (in grams per second) at which 50% of leaks are detected (i.e., median detection limit), and σ is one standard deviation of  _xₒ_. The probability detection of a leak with OGI is calculated using a signmoidal probability function:

$$
f = 1/{(1+exp(-k(log(x)-log(x_0))))}
$$

where f = is the fraction of leaks detected, _x_ is the emission rate in grams of methane per hour, _xₒ_ is the median detection limit (f = 0.5) and _k_ is the steepness of the sigmoid curve. Ravikumar et al. (2018) found that at 3 m _k_ =  4.9 g/hr +/- 3, and _xₒ_ = 0.47 +/- 0.1. However, detection limits were found to be an order of magnitude higher in the Zimmerle study. As such, LDAR-Sim assumes an _xₒ_ of 0.01275 g/s. For reasons listed below, we note that this is likely a conservative estimate. Also, this approach assumes a constant distance of 3 meters from camera to source.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** Detection probabilities for OGI cameras have been shown to vary with operator experience, wind speed, scene background, and other variables. Estimates from Ravikumar et al. (2018) are experimentally derived but are likely low because (i) the OGI inspector knew where to look, (ii) measurements were performed over only 1 week of good conditions, (iii) OGI cameras were tripod mounted, and (iv) videos were analyzed by experts after data collection. Estimates from Zimmerle et al. (2020) are an order of magnitude higher, and likely closer to reality. However, this estimate applies only to experienced inspectors with over 700 site inspections under their belts, so the true median detection across all inspectors may be lower. Furthermore, the Zimmerle study for experienced inspectors could still represent an underestimate as (i) weather conditions were relatively good, (ii) OGI inspectors were participating in a formal study and were likely very focused, and (iii) many of the leaks were odorized. These results would therefore not include laziness, neglect, or missing of leaks from difficult to access areas. See Section 3.8 for more information on detection limits, including the use of single values or probability surfaces.

### max_workday

**Data type:** Integer

**Default input:** 10

**Description:** The maximum number of hours a crew can work in day (includes travel time).

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Can be overwritten if consider_daylight is True and days are short.

### measurement_scale

**Data type:** String

**Default input:** "component"

**Description:** A character string describing the measurements scale. Possible inputs are "component", "equipment", and "site".

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### n_crews

**Data type:** Integer

**Default input:** 1

**Description:** The number of distinct, independent crews that will be deployed using the same method.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Unless explicitly evaluating labour constraints, ensure that sufficient crews are available to perform LDAR according to the requirements set out in the infrastructure_file. For example, if 2000 facilities require LDAR, and each takes an saverage of 300 minutes, ~10,000 work hours are required, or 3-4 crews working full time.

### parameter_level

_see Global Inputs - parameter_level_

### QE

**Data type:** Numeric

**Default input:** 0

**Description:** The standard deviation of a normal distribution with a mean of zero from which a quantification error multiplier is drawn each time an emission rate is estimated. For example, for a value of 2.2, ~35% of measured emission rates will fall within a factor of two of the true emission rate. For a value of 7.5, ~82% of measurements will fall within an order of magnitude of the true emission rate. When QE = 0, the measured emission rate equals the true emission rate. As QE increases, so does the average absolute difference between measured and true emission rates. See Fox et al. (2021) for more information and Ravikumar et al. (2019) for empirical quantification error estimates.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish quantification error. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** As facility-scale quantification error remains poorly constrained for LDAR screening methods, and likely depends on work practice, dispersion modeling, and environment, screening programs should be evaluated using a range of possible quantification errors. We recommend understanding exactly how quantification error works before making use of this functionality. Alternatively, we suggest using literature values of 2.2 and 7.5.

### reporting_delay

**Data type:** Integer

**Default input:** 0

**Description:** The number of days that pass between the end of a survey (when a site is flagged or leaks are tagged) and when the duty holder is informed. The reporting delay is then followed by repair_delay.

**Notes on acquisition:** Get this information from the service provider.

**Notes of caution:** Many service providers have automated systems for reporting leaks as soon as they are found and tagged. However, some companies still provide paper or pdf reports days or even weeks later. It is important to understand the expectations between the duty holder and the service provider.

### scheduling

#### deployment_months

**Data type:** List of integers

**Default input:** N/A

**Description:** A list of months used for scheduling. Methods can only be deployed during these months. For example, [8,9] indicates methods can only be deployed in August and Septamber. If not defined, LDAR-Sim aussmes methods can be depolyed every month.

**Notes on acquisition:** N/A

**Notes of caution:** Only mobile methods can use this functionality.

#### deployment_years

**Data type:** List of integers

**Default input:** N/A

**Description:** A list of years used for scheduling. Methods can only be deployed during these years. For example, [2017,2018] indicates methods can only be deployed in 2017 and 2018\. If not defined, LDAR-Sim aussmes methods can be depolyed every year.

**Notes on acquisition:** N/A

**Notes of caution:** Only mobile methods can use this functionality.

#### LDAR_crew_init_location (mobile only)

**Data type:** List of floats

**Default input:** N/A

**Description:** A list of coordinates [longitude, latitude] that define the initial location of the LDAR crew. It is only required if route_planning is activated.

**Notes on acquisition:** N/A

**Notes of caution:** Only mobile methods can use this functionality.

#### home_bases_files (mobile only)

**Data type:** String

**Default input:** N/A

**Description:** Specifies the name of the csv file that contains all of the required data on the home bases used for LDAR scheduling. At a bare minimum, the csv must contain the following columns: 'name', 'lat', and 'lon', where 'name' indicates the name of home bases (e.g., Calgary), and 'lat' and 'lon' are the coordinates of each home base. The home bases for the aircraft method should be airports and the home bases for all other mobile methods should be towns, cities, or hotels.

**Notes on acquisition:** It is only required if route_planning is activated.

**Notes of caution:** Only mobile methods can use this functionality.

#### route_planning (mobile only)

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to activate the route planning. Route planning allows LDAR crews to choose the nearest facility and home bases to visit based on the shortest travelling cost. The travelling cost is travel time that is calculated using the Haversine distance metric and maximum speed limit of travelling. The maximum speed limit is sampled from speed_list. It also allows LDAR crews to depart from the home base (town, city, or airport) at the start of each day and return to the home base at the end of each day. This will be improved in the future, especially for OGI, drone, and trucks.

**Notes on acquisition:** It requires the user to also define an input for home_bases_files, speed_list, and LDAR_crew_init_location.

**Notes of caution:** Only mobile methods can use this functionality.

#### speed_list (mobile only)

**Data type:** List of floats

**Default input:** [60.0,70.0,80.0,90.0] for road-based methods, [200.0,210.0,220.0,230.0] for aircraft.

**Description:** A list of speed limits that define the maximum travelling speed of technologies. A random speed is sampled from this list when calculating the travel time between two facilities or between the facility and a home base. This can also be a list with a single value.

**Notes on acquisition:** It is only required if route_planning is activated.

**Notes of caution:** Only mobile methods can use this functionality.

### sensor

**Data type:** String

**Default input:** "default"

**Description:** Methods are comprised of both a deployment type and a sensor type. the sensor type is a character string denoting the sensor used in the method. For instance, 'OGI_camera', or 'default'. The 'default' sensor uses the MDL as a threshold to detect leaks based on the measurement scale of the method. Custom sensors can be added and referenced here.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### t_btw_sites

#### file

**Data type:** Character String

**Default input:** None

**Description:** A string denoting the filename of a csv file containing travel times. The file should include one row, with a headcolumn in row 1 of `time_btw_sites`

**Notes on acquisition:** Each value should represent not only driving time, but all time spent not conducting surveys (driving, breaks, meals, break downs, trains, etc.) This data should be scraped from historical GPS data associated with LDAR survey crews, ideally for the facilities under evaluation.

**Notes of caution:** These data may be difficult to acquire and may lack representativeness. An alternative is to use geospatial road data and route planning with LDAR-Sim.

#### vals

**Data type:** List of Integers

**Default input:** [30]

**Description:** Time between sites. denotes the time in minutes required to plan, travel, setup, take down, required in between surveys. A value is selected at random from the list

### weather_envs

Method weather envelopes

#### precip

**Data type:** List of Integers

**Default input:** [0, 1]

**Description:** The range of precipitation accumulation allowed (mm) over one hour.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

#### temp

**Data type:** List of Integers

**Default input:** [-40, 40]

**Description:** The range of average hourly temperature (°C) between which crews will work.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Note that units are in degrees Celsius, not Fahrenheit.

#### wind

**Data type:** List of Integers

**Default input:** [0, 10]

**Description:** The bounding range of maximum average hourly wind speed (m/s at 10m) between which crews will work.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

### TLE_files (satellite only)

**Data type:** String

**Default input:** N/A

**Description:** Specifies the name of the text file that contains orbit information of satellites. TLE stands for a two-line element set, which is a data format encoding a list of orbital elements of an Earth-orbiting object for a given point in time, the epoch. By using TLE of a satellite, LDAR-Sim can estimate the postion of satellite above earth at specific time.

**Notes on acquisition:** It is only required for satellite.

**Notes of caution:** Please be sure the satellite is inlcuded in the TLE file

### satellite_name (satellite only)

**Data type:** Character string that specifies the name of satellite.

**Default input:** N/A

**Description:** The name of satellite.

**Notes on acquisition:** It is only required for satellite.

**Notes of caution:** Please be sure the satellite is included in the TLE file

### version (method level)

_see Global Inputs - version_

--------------------------------------------------------------------------------

## 8\. Data sources, modelling confidence and model sensitivity

There are a broad range of inputs used in LDAR-Sim that must be derived from various sources. Each of these parameters should be carefully considered and understood before using LDAR-Sim to inform decision making. Like other models, the quality of simulation results will depend on the quality and representativeness of the inputs used.

The sensitivity of modeling results to inputs will vary on a case-by-case basis. In general, it is best to assume that all parameters in LDAR-Sim are important before modeling begins. It is strongly recommended to perform sensitivity analyses each time LDAR-Sim is used in order to understand the impact that uncertainty in inputs might have on results. Each LDAR program is unique in many ways. Therefore, there is no universal set of rules or guidelines to indicate _a priori_ which parameters will have the greatest impact on results.

In the same way, the confidence in the accuracy of input data can only be determined by the user who provides the data. For example, if provided an empirical leak-size distribution consisting of only 5 measurements, LDAR-Sim will run and generate results without generating warnings. It is the responsibility of the user to have sufficient experience to understand how LDAR-Sim processes different types of data so that they can confidently provide high quality inputs.

In terms of data source, inputs can come from oil and gas companies, technology providers, or solution providers. Some parameters and inputs can also be sourced from peer reviewed literature or can be used simply as experimental levers to explore different scenarios within LDAR-Sim. The lists below provide a general overview of what stakeholders will _generally_ be responsible for different parameters and inputs. Exceptions will always exist, and may vary according to the purpose of modeling, the jurisdiction, and the scope of the modeling exercise. In general, we strongly suggest deriving method performance metrics from single-blind controlled release testing experiments.

Below are some examples of common sources of LDAR-Sim data. Not all parameters are covered. In the absence of operator-specific data, published estimates can be used.

### Duty Holder / Operator (historical LDAR data)

- leak_file*
- LPR*
- vent_file*

### Duty Holder / Operator (organizational data)

- infrastructure_file (Id, lat, lng, OGI_RS, OG_time)
- repair_cost*
- repair_delay*
- t_offsite_file
- verification_cost

### Technology / Solution Provider / Operator (if self-performing LDAR)

- OGI – n_crews, min_temp_, max_wind_, max_precip_, min_interval, max_workday, cost_per_day_, reporting_delay, MDL* , consider_daylight
- Screening Methods – n_crews, [various weather and operational envelopes]_, min_interval, max_workday, cost_per_day_, reporting_delay, MDL_, consider_daylight, follow_up_thresh, follow_up_ratio, QE_
- Fixed sensor – same as screening methods & up_front_cost, time to detection

### Modeling Expert

- weather_file
- consider_venting

--------------------------------------------------------------------------------

## 9\. References

Fox, Thomas A., Mozhou Gao, Thomas E. Barchyn, Yorwearth L. Jamin, and Chris H. Hugenholtz. 2021\. "An Agent-Based Model for Estimating Emissions Reduction Equivalence among Leak Detection and Repair Programs." _Journal of Cleaner Production_, 125237\. <https://doi.org/10.1016/j.jclepro.2020.125237>.

Ravikumar, Arvind P., Sindhu Sreedhara, Jingfan Wang, Jacob Englander, Daniel Roda-Stuart, Clay Bell, Daniel Zimmerle, David Lyon, Isabel Mogstad, and Ben Ratner. 2019\. "Single-Blind Inter-Comparison of Methane Detection Technologies–Results from the Stanford/EDF Mobile Monitoring Challenge." _Elem Sci Anth_ 7 (1).

Ravikumar, Arvind P., Jingfan Wang, Mike McGuire, Clay S. Bell, Daniel Zimmerle, and Adam R. Brandt. 2018\. "Good versus Good Enough? Empirical Tests of Methane Leak Detection Sensitivity of a Commercial Infrared Camera." _Environmental Science & Technology_.

Zimmerle, Daniel, Timothy Vaughn, Clay Bell, Kristine Bennett, Parik Deshmukh, and Eben Thoma. 2020\. "Detection Limits of Optical Gas Imaging for Natural Gas Leak Detection in Realistic Controlled Conditions." _Environmental Science & Technology_ 54 (18): 11506–14.
