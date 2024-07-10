# Change Log

## 2024-07-11 - Version 4.1.0

1. Implemented duration estimation factor - See user manual for more details

## 2024-07-11 - Version 4.0.5

1. Fixed crew count always being overwritten by estimated crew count
2. Update language around sensitivity analysis
3. Update language of stacked cost (now value) bar chart
4. Fix bug with sites considered for follow-ups and queue for follow-ups

## 2024-07-07 - Version 4.0.4

1. Fixed per day costs
2. Fixed scaling with surveys at the equipment group level
3. Fixed error preventing users from setting parameters at the equipment group level
4. Updated default parameter data types
5. New unit tests added
6. Other various bugs/future exception warnings

## 2024-07-02 - Version 4.0.3

1. Fixed potential crew shortage warning message
2. Fixed tick labels on output visualizations to show numbers between -1 to 1, specifically 0 when using metric prefixes
3. Added option to disable program specific visualizations
4. Fixed error that would sometimes occur with summary output generation

## 2024-06-20 - Version 4.0.2

1. Mitigation related plots will automatically not be rendered when there are no mitigation in the simulation.
2. Updated the sensitivity analysis module script to be in line with the ldar_sim_run script

## 2024-06-19 - Version 4.0.1

1. Fixed an Issue where users would encounter an error when trying to simulate only non-repairable emissions

## 2024-06-17 - Version 4.0.0

The version bump to 4.0 of LDAR-Sim included a significant overhaul of the existing code base and functionality overhaul.

1. Improved User Manual
2. Improved stationary deployment - continuous monitoring is now based on rolling averages
3. Improved quantification error
4. Refactored emissions, added granularity - see User Manual for more details
5. Refactored infrastructure, added granularity - see User Manual for more details
6. Refactored sensors, the following sensors are now built into ldar-sim: METEC_NoWind, OGI_Zim, and OGI_RK (See user manual for more details on how to use them)
7. Refactored scheduling, significant runtime improvement from v3
8. New Output parameters to disable outputs
9. New uncertainty outputs
10. New Sensitivity Analysis Module
11. New debugging mode - enables benchmarking
12. _Removed routing functionality_
13. New unit tests

## 2024-03-18 - Version 3.3.6

1. **New Documentation** Added new installation guide documentation.

## 2023-11-30 - Version 3.3.5

1. **Bug fix for METEC wind sensor** Fixed the wind factor units. Previously used km/hr, changed to m/s to properly reflect the METEC wind dependent curve.

## 2023-11-23 - Version 3.3.4

1. **New External Sensor** Added new external sensor - METEC Wind normalized curve

## 2023-11-21 - Version 3.3.3

1. **Bugfix for file input for repair cost** Resolved a bug where repair cost input as file was not working.

## 2023-10-19 - Version 3.3.2

1. **Bugfix for concurrent mobile method survey times** Resolved a bug where previously survey time for concurrent mobile methods would be incorrect.

## 2023-09-21 - Version 3.3.1

1. **Follow-up Watchlist sorting toggle** Sorting on the follow-up watch list can be turned off.

## 2023-09-14 - Version 3.3.0

1. **Bugfix to Proportion** LDAR-Sim proportion has been fixed to properly proportion by top proportion % of emitting sites where previously proportioning was done by dropping sites with the longest time since last being surveyed.

## 2023-08 - Version 3.2.3

1. **Splitting of natural repair cost** The cost of repair due to NRd was split from repair cost.

## 2023-08 - Version 3.2.2

1. **Fix to update_tag** Fix applied to update tag to increment natural_n_tags when the natural company overwrites an existing tag and repairs the book.

## 2023-08 - Version 3.2.1

1. **Performance Improvements** Runtime performance improvements have been made for LDAR-Sim initialization.

## 2023-08 - Version 3.2.0

1. **Added outputs parameters to control files output from LDAR-Sim** New output parameters introduced to the LDAR-Sim simulation settings allow for users to select specific outputs to enable/disable. This can help reduce the memory load of simulations for users running large simulations if they do not care about every result.

## 2023-08 - Version 3.1.1

1. **Added new E2E functionality** As part of the pass pass criteria for E2E tests, outputs must contain all the same files as expected outputs.

## 2023-08 - Version 3.1.0

1. **Reworked n_init_leaks** The parameter n_init_leaks was reworked to n_init_leaks_prob. See the User Manual for details on how to use the parameter.

## 2023-07 - Version 3.0.1

1. **Updated Output CSV file names** The output file names will now also contain program name.

## 2023-07 - Version 3.0.0

1. **Refactored Parameter Structure** The LDAR-Sim parameter structure has been refactored. Many of the parameters previously in the program level can now be located in the new virtual_world parameters file. This will help make LDAR-Sim parameterization more intuitive.

## 2023-07 - Version 2.4.0

1. **Removed Subtype_times_file** The ability to set survey times for sites on a per subtype basis using the "subtype_times_file" parameter has been removed. This functionality will be reintroduced in the subtype file at a later date.

## 2023-07 - Version 2.3.1

1. **Added_End_to_end testing for program parameters** A new End-to_end test has been added to test previously untested program parameters.

## 2023-07 - Version 2.3.0

1. **Added functionality for initializing pre-simulation leaks** Users can now utilize n_init_days and n_init_leaks to initialize pre-simulation leaks - leaks LDAR-Sim generates before the start date of the simulation.

## 2023-07 - Version 2.2.1

1. **Cost bug fix** Specific bug was encountered when using per_site costs with methods that take multiple days to finish surveying.

## 2023-07 - Version 2.2.0

1. **Added external sensors** Users have access to more technology sensors, documentation and guidance on how to create their own technology sensors.

## 2023-06 - Version 2.1.4

1. **Added functionality for site level follow-ups** Users can now have measurement_scale "site" level follow ups by leveraging the follow-up: preferred_method parameter. This allows for modelling of multiple screenings based on the results of each prior screening (Which could increase confidence in fugitives, improve measurement accuracy, etc).

## 2023-06 - Version 2.1.3

1. **Added documentation for subtype_file functionality** Added documentation to the user manual to describe subtype file functionality.
2. **Added ability to sample for leak rates, vent rates per subtype** Users can now specify vent rate and leak rate files to sample from on a per subtype basis in the subtype file.

## 2023-06 - Version 2.1.2

1. **New Output added to track site-visits** A new output csv file has been added to LDAR-Sim containing information tracking the results of site-visits by methods.
2. **Site-Level Venting Rates** Venting rates can now be provided at a site level in the infrastructure file. This is a breaking change that removes previous venting behavior.

## 2023-05

1. **Added Unit Testing** Unit testing can now be found under testing/unit_testing in the main LDAR-Sim folder
2. **Requirements update** Requirements have been updated to allow users to use newest versions of libraries and python 3.11 for the conda environment.

## 2022-11

1. **Survey Scheduling bug fixes**  Bug fixes made to survey scheduling for mobile methods.
    1. ***Changed logic for scheduling surveys for sites*** Changed site survey scheduling logic to begin counting time since a site was last surveyed from the starting date of the previous survey, not the end date.
    2. ***Changed rollover of mobile_crew to shared*** The rollover variable was for mobile crews was moved to a class variables so all crews now share a rollover list. This ensures survey progress is no longer reset if the crew surveying the site changes.
    3. ***Added scheduling fix to reduce schedule slipping*** Added scheduling to add sites to the survey pool if half the survey duration(campaign) has passed. This is intended to reduce the observed issue of schedule slipping.
    4. ***Bugfix for survey scheduling*** Fixed behavior where surveys completed on Jan 1 of any year would wrongly be considered as a survey done the previous year.
2. **Added new parameter min_time_bt_surveys** Added a new parameter for setting value of minimum time that must pass between surveys, this is now the value used for determining when to add sites to survey pool.

    ***_min_time_bt_surveys*** can be set like ***_RS*** or ***_time*** in the infrastructure file.

## 2022-09

1. **Subtype File addition** Programs: specify LPR, LDR for subtypes. Deprecates subtype-distribution. Will eventually also combine the subtype-times-file.
2. **Updated Default parameters** Methods/Programs: Several parameters were updated to support floats(from ints).
3. **Preferred Follow Up** - Methods: Ability to specify different followups for a single program having multiple non-component level surveys.
4. **Updated User Manual** Updated user manual with additions.
5. **Spatial coverage bug fix**
6. **Repair delay** Programs: can now be a single value, a list or a log normal distribution.
7. **Estimate emissions** Optionally allows for additional outputs related to estimating emissions based on survey frequency and leak rate.

## Change Log Version 2.0 (21/09)

1. **External leak generator -** Optionally creates a single set of leaks that can be used across multiple simulations to enable "apples to apples" comparisons of different programs. Leak lists can also be saved and shared to improve reproducibility.
2. **Modularized methods -** Methods (e.g., aircraft) are now comprised of a deployment style (platform), a sensor type, the scale of measurement (equipment vs component vs site), and whether or not they perform follow-up inspections. Old method modules are now defunct.
3. **User manual -** Comprehensive documentation for all input parameters, including descriptions and warnings. Also includes a developer guide for those who want to contribute to the public code base.
4. **Added satellite -** Satellite module now available, including satellite sensors, deployment strategies, and scheduling.
5. **Crew scheduling -** Allows route-planning, specifying survey dates and date ranges, and includes route optimization based on site, home base, and airport locations.
6. **Company scheduling -** Companies can deploy crews strategically to spatial clusters of sites. Useful when assets are distributed across large geographical areas.
7. **Switched to MIT license** MIT licensing will be used from version 2 onwards.
8. **Start and end dates -** Instead of start year and a number of timesteps, specific start and end dates must be provided.
9. **Hourly weather -** Optional ability now exists to query weather on an hourly basis rather than only a daily basis.
10. **New sensitivity analysis -** Added a sensitivity analysis program called ldar_sim_sens.py that runs LDAR-Sim from a wrapper that will generate either a series of programs based on a single range of variables or a series of simulation sets based on multiple ranges of variables.
11. **Operator agent -** A new operator agent that can be assigned to a site and can use any sensor (default is AVO - auditory, visual, olfactory)
12. **Instant follow-up -** Allows company to flag sites immediately and prioritize them for follow up if the emission rate from the site is greater than a user-defined threshold.
13. **Follow-up delay -** Allows a company to wait a set amount of time (i.e., accumulate multiple screening measurements, even of the same site) before triaging sites for follow-up. Site redundancy can be handled using a new redundancy filter where maximum, average, or recent emission rates can be used to rank sites by severity.
14. **Input mapper -** Maps user-defined inputs to relevant internal defaults and checks input types for issues before running simulations.
15. **Local weather -** Added a function to convert weather data to local time zone when large regions are modeled.
16. **Accessible weather -** Improved custom ERA5 downloader and in-file support documentation.
17. **Internal defaults -** Internal default parameters for all methods to mitigate mistakes due to previously complex parameter tracking.
18. **Rollover -** All methods now use a rollover, meaning that if a site cannot be completed before the end of the day, crews return to a home base and come back the next day to finish that site. If a site requires multiple days to inspect, crews will continue to return to that site until it is completed. This update more accurately reflects real field operations.
19. **Labor calibration -** Option to automatically estimate the number of required crews for a given program and set minimum intervals to ensure that surveys are approximately evening distributed across each compliance period. This is performed before simulations are run and is used to estimate when a survey should be performed based on the required survey frequency and how many of crews are required to perform all surveys within the set time interval.
20. **Improved economics -** New economics functionality with cost_mitigation.py that calculates the value of natural gas mitigated with LDAR programs below baseline emissions. This value is used, along with total costs, to derive a cost mitigation ratio for each LDAR program input into the model. Automatically outputs new figures.
21. **Removed leak count and spin up -** These two inputs were redundant and prone to error. Initial emissions are now estimated using leak generation and removal assumptions.
22. **Seed timeseries generator –** Useful for testing as each day will have the same seed for all programs in a simulation set.
23. **Code cleanup –** Removed unused or obsolete code, including defunct sensitivity analyses.
24. **Changed to YAML inputs -**  Switched from text file inputs to YAML to improve readability.
25. **Restructured software folder -** Improved folder structure for entire software to be more modular and follow current practices.
26. **Updated input data structure -** An object-orientated input data structure is now used.
27. **Package upgrades -** Updated Python packages, requirements file and, pipenv files to enable flexibility in package management
28. **Improved parameter organization -** Input parameter lists are now much longer but are better organized. New rules are also implemented to ensure that consistent data types are used for lists and that nested dictionaries are appropriately managed.
29. **Addition of technology coverage** Users can specify the probability that an agent can locate a leak independent of leak size. Coverage is split into two variables, `spatial` where the leaks unlocated leaks will not be found on subsequent surveys, and `temporal` where they can be found on subsequent surveys.
30. **Performance improvements**: Leaks are moved as subobjects of sites, allowing fewer iterations of code during runtime.
