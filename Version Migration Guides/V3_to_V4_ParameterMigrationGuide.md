# LDAR-Sim V4 Parameter Migration Guide

## Purpose

This guide is intended to assist users users who are updating to LDAR-Sim V4 by providing instructions on how to transfer as much of their parameter files as possible to the V4 format from V3. Do note that some new LDAR-Sim behavior has been introduced in V4 and some existing behavior has been changed, thus it is impossible to completely transfer all parameter files and inputs.

## What changed between V3 and V4

The majority of the LDAR-Sim parameters from V3 still exist in V4, but many of them have been renamed or reworked. Some parameters have been removed entirely. There are many new input files users can provide to define the modelled infrastructure in more granularity and previously existing input files have mostly been removed or reworked.

## Guidance on moving from V3 to V4

When moving from V3 to V4, it is advised to read the updated [user manual](../USER_MANUAL.md) to get an initial understanding of the scope of all the changes that have occurred. Users will need to make new input files in order to run V4 simulations: Critically users will need a [sites file](../USER_MANUAL.md#sites-file) and the new [emissions file](../USER_MANUAL.md#emissions-file) to run any simulations. Many parameters have been changed or renamed. Reference the [Parameter File Changes](#parameter-file-changes) section for more detailed information. It may be easier for users to attempt to parameterize the V4 parameters while referencing the user manual for aid instead of attempting to "migrate" V3 simulation parameters.

## Parameter File Changes

### Simulation Settings

#### Simulation Settings: Renamed Parameters

| V3 Parameter | V4 Parameter    | Notes                                                                 |
|--------------------|-----------|-----------------------------------------------------------------------|
| n_processes| processes_count  | None |
| n_simulations| simulation_count  | None |

#### Simulation Settings: Removed Parameters

| V3 Parameter | Notes                                                                   |
|--------------------|-----------|
| print_from_simulations| now always enabled  |
| pregenerate leaks| now always enabled  |
| outputs| functionality moved to [output parameters](../USER_MANUAL.md#6-output-settings) |
| start_date| moved to virtual world |
| end_date| moved to virtual world |

#### Simulation Settings: New Parameters

No new parameters were introduced in simulation settings.

### Virtual World

#### Virtual World: Renamed Parameters

| V3 Parameter | V4 Parameter    | Notes                                                                 |
|--------------------|-----------|-----------------------------------------------------------------------|
| infrastructure_file| infrastructure: sites_file  | What was the infrastructure is now just one of the files that define infrastructure. See the [user_manual](../USER_MANUAL.md#infrastructure) on new infrastructure parameters in the virtual world for more information|
| repair_delay| repairs: delay| repair_delay was moved under the repairs heading and renamed to delay|
|emissions: LPR| emissions: repairable_emissions: emissions_production_rate| Not quite just a rename, but the functionality is very similar |
| NRD | emissions: repairable_emissions: duration | Not quite just a rename, but the functionality is very similar |

#### Virtual World: Removed Parameters

| V3 Parameter | Notes                                                                   |
|--------------------|-----------|
| weather_is_hourly| weather functionality has been streamlined  |
| emissions: consider_venting| emissions granularity has been reworked. See [emissions section](../USER_MANUAL.md#emissions) and all emissions relating parameters in the user manual for more information|
| emissions: leak_dist_params| Effectively moved this functionality into the [emissions file](../USER_MANUAL.md#emissions-file)|
| emissions: leak_dist_type| Effectively moved this functionality into the [emissions file](../USER_MANUAL.md#emissions-file)|
|leak_file| Effectively moved this functionality into the [emissions file](../USER_MANUAL.md#emissions-file)|
|emissions: leak_file_use|Fit functionality has been removed. This is to avoid scenarios where emissions rates an incorrectly fit to a lognormal distribution when the data is not lognormal|
| emissions: max_leak_rate | Effectively moved this functionality into the [emissions file](../USER_MANUAL.md#emissions-file) |
| emissions: units | Effectively moved this functionality into the [emissions file](../USER_MANUAL.md#emissions-file) |
| n_init_leaks_prob | To be reintroduced in later updates as needed |
| n_init_days | To be reintroduced in later updates as needed |

#### Virtual World: New Parameters

| New Parameter | Notes                                                                   |
|--------------------|-----------|
| start_date| moved to virtual world from simulation_settings  |
| end_date| moved to virtual world from simulation_settings |
| repairs: cost | moved to virtual world from program parameters |
| infrastructure: site_type_file | See relevant [section](../USER_MANUAL.md#site-type-file) in the user manual |
| infrastructure: equipment_group_file | See relevant [section](../USER_MANUAL.md#equipment-file) in the user manual |
| infrastructure: sources_file | See relevant [section](../USER_MANUAL.md#source-file) in the user manual |
| emissions: emissions_file| See relevant [section](../USER_MANUAL.md#emissions_file) in the user manual |
| emissions: repairable_emissions: emissions_rate_source | See relevant [section](../USER_MANUAL.md#emissions_rate_source-propagating-parameter) in the user manual |
| emissions: repairable_emissions: multiple_emissions_per_source | See relevant [section](../USER_MANUAL.md#multiple_emissions_per_source-propagating-parameter) in the user manual |
| emissions: non_repairable_emissions: emissions_production_rate| See relevant [section](../USER_MANUAL.md#emissions_production_rate-propagating-parameter) in the user manual |
| emissions: non_repairable_emissions: emissions_rate_source | See relevant [section](../USER_MANUAL.md#emissions_rate_source-propagating-parameter) in the user manual |
| emissions: non_repairable_emissions: duration | See relevant [section](../USER_MANUAL.md#duration-propagating-parameter) in the user manual |
| emissions: non_repairable_emissions: multiple_emissions_per_source | See relevant [section](../USER_MANUAL.md#multiple_emissions_per_source-propagating-parameter) in the user manual |

### 3. Programs

#### Programs: Changes To Existing Parameters

| V3 Parameter | Notes                                                                 |
|--------------------|-----------------------------------------------------------------------|
| parameter_level | The default value for parameter_level for program parameters has been changed from **program** to **programs**|

#### Programs: Renamed Parameters

| V3 Parameter | V4 Parameter    | Notes                                                                 |
|--------------------|-----------|-----------------------------------------------------------------------|
| economics: carbon_price_tonnesCO2e | economics: carbon_price_tonnes_CO2_equivalent |  |
| economics: CWP_CH4 | economics: global_warming_potential_CH4| |
| economics: sale_price_natgas | economics: sale_price_of_natural_gas| **Note**: the units of this parameter have changed |

#### Programs: Removed Parameters

| V3 Parameter | Notes                                                                   |
|--------------------|-----------|
| economics: cost_CCUS | Removed due to limited use in outputs |
| repair_costs | Moved to virtual world |

#### Parameters: New Parameters

| New Parameter | Notes                                                                   |
|--------------------|-----------|
| duration_estimate: duration_factor| See [relevant](../USER_MANUAL.md#duration_estimate) section in the user manual |
| duration_estimate: duration_method| See [relevant](../USER_MANUAL.md#duration_method) section in the user manual |

### 4. Methods

Note there are now two default method parameter files: One for mobile deployment_type methods and one for stationary deployment_type methods. See [method parameters](../USER_MANUAL.md#9-method-inputs) in the user manual for more details.

#### Methods: Changes To Existing Parameters

| V3 Parameter | Notes                                                                 |
|--------------------|-----------------------------------------------------------------------|
| parameter_level | The default value for parameter_level for method parameters has been changed from **method** to **methods**|

#### Methods: Renamed Parameters

| V3 Parameter | V4 Parameter    | Notes                                                                 |
|--------------------|-----------|-----------------------------------------------------------------------|
| label| method_name |  |
| sensor: MDL | sensor: minimum_detection_limit | |
| n_crews | crew_count| |
| RS | surveys_per_year | |
| time | survey_time | |
| weather_envs | weather_envelopes | |
| weather_envs: precip | weather_envelopes: precipitation | |
| weather_envs: temp | weather_envelopes: temperature | |
| weather_envs: wind | weather_envelopes: wind | |

#### Methods: Removed Parameters

| V3 Parameter | Notes                                                                   |
|--------------------|-----------|
| sensor: QE| Replaced with [quantification_error](../USER_MANUAL.md#quantification_error) heading, under which are new quantification error parameters.|
| mod_loc | Removed as with new object oriented structure type can support this when new sensor types are properly implemented |
| cost: per_hour | Removed as it was misleading, LDAR-SIm functions on a day timescale |
| scheduling: LDAR_crew_init_location | Removed all routing parameters as it was not fully functional |
| scheduling: home_base-files | Removed all routing parameters as it was not fully functional |
| scheduling: travel_speeds | Removed all routing parameters as it was not fully functional |
| scheduling: min_time_bt_surveys | New scheduling algorithm uses queue based scheduling, removing the need for this parameter |
| follow_up: instant_threshold_type | [Instant threshold](../USER_MANUAL.md#instant_threshold) is now fixed to an absolute threshold|
| follow_up: min_followups| To be reimplemented if needed|
| follow_up: min_followup_type| To be reimplemented if needed|
| follow_up: min_followup_days_to_end| To be reimplemented if needed|
| follow_up: instant_threshold_type | [Threshold](../USER_MANUAL.md#threshold-mobile-parameter) is now fixed to an absolute threshold|

#### Methods: New Parameters

| New Parameter | Notes                                                                   |
|--------------------|-----------|
| sensor: quantification_error: quantification_parameters | See [relevant](../USER_MANUAL.md#quantification_parameters) section in the user manual|
| sensor: quantification_type: quantification_parameters | See [relevant](../USER_MANUAL.md#quantification_type) section in the user manual|
| rolling_average : small_window | stationary methods only. See [relevant](../USER_MANUAL.md#small_window-stationary-parameter) section in the user manual|
| rolling_average : large_window | stationary methods only. See [relevant](../USER_MANUAL.md#large_window-stationary-parameter) section in the user manual|
| rolling_average : small_window_threshold | stationary methods only. See [relevant](../USER_MANUAL.md#small_window_threshold-stationary-parameter) section in the user manual|
| rolling_average : large_window_threshold | stationary methods only. See [relevant](../USER_MANUAL.md#large_window_threshold-stationary-parameter) section in the user manual|

## Input Files

### Unchanged Input Files

The weather file has remained unchanged from V3 to V4.

### Infrastructure

A new, much more granular infrastructure design has been introduced. See [infrastructure](../USER_MANUAL.md#infrastructure) and [virtual world defining files](../USER_MANUAL.md#10-virtual-world-defining-files) sections in the user manual for more information.

### Emissions File (New to V4)

New to V4 is a new file called the Emissions Fie. This file is mandatory to run any V4 simulations. Read more about it in the User Manual [here](../USER_MANUAL.md#emissions-file). It must be set in the virtual world parameters, see the relevant section [here](../USER_MANUAL.md#emissions_file).
