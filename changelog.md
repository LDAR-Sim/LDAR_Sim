Change Log Version 2.0 (21/09):
1.	**Added external leak generator -** for creating a single leak timeseries and initial leaks for each simulation-set.
2.	**Removed Leak Count and Spin up -** Replaced with leaks generated within the NRd time period.
3.	**Changed to YAML inputs -**  Switched from text to YAML with default program parameters hardcoded in python. 
4.	**Added Satellite sensor, and deployment type**
5.	**Create a Base Class Module system -** Modules are now comprised of a deployment method, a sensor type, the scale of measurement (equipment vs component vs site), and whether they are follow-up. Old method modules are now redundant. 
6.	**Added an in-repo Input document**
7.	**Added an input mapper function -** Will check types and inputs prior to running programs.
8.  **Updated Python packages, requirements file and pip.loc**
9.	**Added company, and crew scheduling modules -**  Allows route-planning, allowable dates/months for surveys, and includes route optimization based on site location and airport locations.
10.	**Rollover applied to all new methods**
11. **Switched to MIT license for LDAR-Sim**
12.	**Restructured software folder -** to be more modular and follow current practices.
13.	**Removed unused or obsolete code –** old sensitivity analysis
14.	**Updated Input data structure -** to object orientated structure.
15.	**Updated time to have a start and end date -** instead of start year and timesteps.
16.	**Added ability to use hourly weather**
17.	**Added a function to convert weather data to local time zone.**
18.	**Improved ERA5 download program and support (in file) documentation**
19.**	Added a seed timeseries generator –** Useful for testing as each day will have the same seed for all programs in a simulation set. 
20.	**Added a sensitivity analysis program called ldar_sim_sens.py -** This runs LDAR sim from a rapper that will generate either a series of programs based on a single range of variables or a series of simulations sets based on a single range of variables.
21.	**Added a number of crews and minimum survey interval estimator -**  This is performed before simulations are ran and is used to estimate when a survey should be performed based on the RS and how many of crews are required to perform all surveys within the RS time period.
22.	**Added Operator agent -** Uses stationary method and new AVO sensor
23.	**Added follow-up delay grace period -**  Allows company to wait a set amount of time before deciding which sites to follow up with.  Site redundancy can be handled using the redundancy filter where max, average, or recent emission rates can be used.
23.	**Added instant follow-up -**  Allows company to flag sites immediately if the emission rate from the site is greater than a user defined threshold.