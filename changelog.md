# Change Log

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
