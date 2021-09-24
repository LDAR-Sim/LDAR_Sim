Change Log Version 2.0 (21/09):
1.	**External leak generator -** Optionally creates a single set of leaks that can be used across multiple simulations to enable "apples to apples" comparisons of different programs. Leak lists can also be saved and shared to improve reproducibility.
2.	**Modularized methods -** Methods (e.g., aircraft) are now comprised of a deployment style, a sensor type, the scale of measurement (equipment vs component vs site), and whether or not they perform follow-up inspections. Old method modules are now defunct.
3.	**User manual -** Added comprehensive documentation for all input parameters, including descriptions and warnings. Also includes a developer guide for those who want to contribute to the public code base.
4.	**Added satellite -** Satellite module now available, including satellite sensors, deployment strategies, and scheduling.
5.	**Crew scheduling -** Allows route-planning, specifying survey dates and date ranges, and includes route optimization based on site, home base, and airport locations. 
6.	**Company scheduling -** Companies can deploy crews strategically to spatial clusters of sites. Useful when assets are distributed across large geographical areas.
7.	**Switched to MIT license** MIT licensing will be used from version 2 onwards.
8.  **Start and end dates -** Instead of start year and a number of timesteps, specific start and end dates must be provided.
9.	**Hourly weather -** Optional ability now exists to query weather on an hourly basis rather than only a daily average.
10.	**New sensitivity analysis -** Added a sensitivity analysis program called ldar_sim_sens.py that runs LDAR-Sim from a wrapper that will generate either a series of programs based on a single range of variables or a series of simulation sets based on multiple ranges of variables.
11. **Operator agent -** A new operator agent that can be assigned to a site and can use any sensor (default is AVO - auditory, visual, olfactory)
12.	**Instant follow-up -** Allows company to flag sites immediately and prioritize them for follow up if the emission rate from the site is greater than a user-defined threshold.
13.	**Follow-up delay -** Allows a company to wait a set amount of time (i.e., accumulate multiple screening measurements, even of the same site) before triaging sites for follow-up. Site redundancy can be handled using a new redundancy filter where max, average, or recent emission rates can be used to rank sites by severity.
14.	**Input mapper -** Maps user-defined inputs to relevant internal defaults and checks input types for issues before running simulations.
15.	**Local weather -** Added a function to convert weather data to local time zone when large regions are modeled.
16.	**Accessible weather -** Improved custom ERA5 downloader and in-file support documentation.
17. **Internal defaults -** Internal default parameters for all methods to mitigate mistakes due to previously complex parameter tracking.
18. **Rollover -** All methods now use a rollover, meaning that if a site cannot be completed before the end of the day, crews return to a home base and come back the next day to finish that site. If a site requires multiple days to inspect, crews will continue to return to that site until it is completed.
19.	**Labor calibration -** Option to automatically estimate the number of required crews for a given program and set minimum intervals to ensure that surveys are approximately evening distributed across each compliance period. This is performed before simulations are run and is used to estimate when a survey should be performed based on the required survey frequency and how many of crews are required to perform all surveys within the set time interval.
20. **Improved economics -** New economics functionality with cost_mitigation.py that calculates the value of natural gas mitigated with LDAR programs below baseline emissions. This value is used, along with total costs, to derive a cost mitigation ratio for each LDAR program input into the model. Automatically outputs new figures.
21. **Removed leak count and spin up -** These two inputs were redundant and prone to error. Initial virtual world emissions are now estimated using leak generation and removal assumptions.
22. **Seed timeseries generator –** Useful for testing as each day will have the same seed for all programs in a simulation set. 
23.	**Code cleanup –** Removed unused or obsolete code, especially the old and defunct sensitivity analysis.
24. **Changed to YAML inputs -**  Switched from text file inputs to YAML to improve readability.
25.	**Restructured software folder -** Improved folder structure for entire software to be more modular and follow current practices.
26.	**Updated input data structure -** An object-orientated input data structure is now used.
27. **Package upgrades -** Updated Python packages, requirements file and pip.loc.
28. **Improved parameter organization -** Input parameter lists are now much longer but are better organized. New rules are also implemented to ensure that consistent data types are used for lists and that nested dictionaries are appropriately managed.
