# LDAR-Sim Batch Running Manual

The batch runner offers an alternative method for executing LDAR-Sim. With this feature, users can run the standard simulation in multiple batches, consolidating the outputs of these batches into a single averaged value whenever applicable

## How to use

To utilize the batch script, configuring LDAR-Sim with all parameters in a designated directory. Then, employ the following command:
```ldar_sim_batchrun.py --n_rep {number_of_repetitions} -P {directory_path}```

Example command to run 100 batch simulations contained in the folder simulations would be:
```ldar_sim_batchrun.py --n_rep 100 -P simulations```

## Outputs

### Regular Outputs

The following files are maintained for each of programs of the last batch of simulations.
```timeseries_output_{simulation}_{Program name}.csv```
```leaks_output_{simulation}_{Program name}.csv```
```sites_output_{simulation}_{Program name}.csv```

### Sites

`sites_output_{program}_concat.csv`

The output file will only be created if all the sites from the infrastructure file are utilized in a single simulation, and if the sites output feature is enabled. The `sites_output_{program}_concat.csv` takes the individual sites output files and summarizes the values.


|Column Names      |Unit   |Description                |
|------------------|-------|---------------------------|
|facility_ID       |N/A    |Unique ID of the site/locations simulated|
|Cum_leaks         |N/A    |Average cumulative number of leaks at the site|
|init_leaks        |N/A    |Average number of initial leaks found at the site|
|total_emissions_kg|kg     |Average total emissions at the site(in kilograms)|
|subtype_code      |N/A    |The subtype code of the site|
|lat               |Degrees|Latitude of the site|
|lon               |Degrees|Longitude of the site|
|equipment_groups  |N/A    |Number of equipment groups at the site|
|n_sims            |N/A    |Number of simulations the site participated in|

```sites_summary.csv```

For this file, each individual row is representing the summary statistics of a single program of a single simulation run.

|Column Names                       |Unit       |Description                |
|-----------------------------------|-----------|---------------------------|
|Program                            | N/A       |Name of the program             |
|Mean_emissions_per_site            |per site   |Mean emissions per site in kg for a single site, calculated for each simulation set|
|5th_percentile_Emissions_per_site  |per site   |5th percentile of emissions per site in kilograms, calculated for each simulation set|
|95th_percentile_Emissions_per_site |per site   |95th percentile of emissions per site in kilograms, calculated across for each simulation set|
|Mean_leaks_per_site                | # per site|Mean number of leaks per site, calculated for each simulation set|
|5th_percentile_leaks_per_site      | # per site|5th percentile of the number of leaks per site, calculated for each simulation set|
|95th_percentile_leaks_per_site     | # per site|95th percentile of the number of leaks per site, calculated for each simulation set|

### Leaks

```leaks_summary.csv```

In this file, each row represents summary statistics for an individual program during each simulation run, focusing on a per-leak basis.

|Column Names                |Unit   |Description                |
|----------------------------|-------|---------------------------|
|Program                     | N/A   |Name of the program|
|Volume_mean                 |kg     |Mean emissions volume in kilograms per leak, calculated for a run of the simulation|
|5th_percentile_Volume       |kg     |5th percentile emissions volume in kilograms per leak, calculated for a run of the simulation|
|95th_percentile_Volume      |kg     |95th percentile emissions volume in kilograms per leak, calculated for a run of the simulation|
|Mean_leak_rate              |g/sec  |Overall mean leak rate per leak in a simulation|
|5th_percentile_leak_rate    |g/sec  |5th percentile leak rates per leak in a simulation|
|95th_percentile_leak_rate   |g/sec  |95th percentile leak rates per leak in a simulation|
|Mean_Days_Active            |days   |Mean number of days active per leak in a simulation|
|5th_percentile_Days_active  |days   |5th percentile of days active per leak in a simulation|
|95th_percentile_days_active |days   |95th percentile of days active per leak in a simulation|

### Time Series

```timeseries_summary.csv```

For this file, each individual row is representing the summary statistics of a single program of a single simulation run.

|Column Names                              |Unit      |Description|
|------------------------------------------|----------|------------|
|Program                                   | N/A      |Name of the program |
|Mean_daily_emissions_kg_per_day           |kg/per day|Mean daily emissions of the program in kilograms|
|5th_percentile_daily_emissions_kg_per_day |kg/per day|5th percentile of daily emissions in kilograms for the program|
|95th_percentile_daily_emissions_kg_per_day|kg/per day|95th percentile of daily emissions in kilograms for the program|
|Mean_total_daily_cost_per_day             |$/per day |Mean average daily cost for the program|
|5th_percentile_total_daily_cost_per_day   |$/per day |5th percentile of daily cost per day for the program|
|95th_percentile_total_daily_cost_per_day  |$/per day |95th percentile of daily cost per day for the program|
|Mean_repair_cost_per_day                  |$/per day |Mean average repair cost per day for the program|
|5th_percentile_repair_cost_per_day        |$/per day |5th percentile of daily repair cost for the program|
|95th_percentile_repair_cost_per_day       |$/per day |95th percentile of daily repair cost for the program|
|Mean_active_leaks_per_day                 |leaks/day |Mean number of active leaks per day for the program|
|5th_percentile_active_leaks_per_day       |leaks/day |5th percentile of active leaks per day for the program|
|95th_percentile_active_leaks_per_day      |leaks/day |95th percentile of active leaks per day for the program|
|Mean_new_leaks_per_day                    |leaks/day |Mean number of new leaks per day for the program|
|5th_percentile_new_leaks_per_day          |leaks/day |5th percentile of new leaks per day for the program|
|95th_percentile_new_leaks_per_day         |leaks/day |95th percentile of new leaks per day for the program|
|Mean_n_tags_per_day                       |tags/day  |Mean number of new tags per day for the program|
|5th_percentile_n_tags_per_day             |tags/day  |5th percentile of new tags per day for the program|
|95th_percentile_n_tags_per_day            |tags/day  |95th percentile of new tags per day for the program|
|Additional Statistics                     |N/A       |Contains a dictionary of additional statistics that are program specific. This column will provide additional information on the number of site visits, and effective flags and tags of a given method of a program. |
