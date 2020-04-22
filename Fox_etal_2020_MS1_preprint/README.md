# Reproducibility Guide
This guide is intended to help interested parties reproduce the results from Fox et al 2020, which introduces LDAR-Sim and presents a case study demonstrating various hypothetical LDAR programs in Alberta, Canada.

## Step 1: Before you begin
Read and understand the LDAR-Sim LICENSE (GNU Affero General Public License Version 3).
Read Fox et al 2020 to familiarize yourself with LDAR-Sim fundamentals. 

## Step 2: Libraries and data
Ensure all required python modules/packages/libraries are available: numpy, pandas, datetime, csv, sys, os, random, math, plotnine, ephem, gc, time, warnings, gdal (osgeo), osr (osgeo), Dataset (netCDF4), date_format (mizani.formatters), ECMWFDataServer (ecmwfapi).

Open ldar_sim_main and set your working directory on line 49.
Ensure that all input files and program files are in your working directory.
No other changes should be required to run the OGI scenarios from the case study.

## Step 3: Reproduce OGI simulations
Run LDAR-Sim from the file 'ldar_sim_main'. This file lets users define global parameters, inputs, and as many different LDAR programs as desired. Program intercomparisons are made, output, and plotted automatically.

Just as each simulation can compare multiple LDAR programs, so can each LDAR program consist of multiple different LDAR methods. We provide generic OGI, aircraft, and truck methods, but others can be devised using generic methods as templates.

The ldar_sim_main file is currently configured for the OGI comparison case study presented in Fox et al 2020. Four different OGI-based LDAR programs are parameterized, which differ only according to weather and labour constraints.

These reproducibility simulations will take some time to run, as 25 sets of simulations are used for each program over multiple years. Results should resemble Figures 2C and 2D in Fox et al 2020.

## Step 4: Reproduce alt-LDAR simulations
Reconfigure ldar_sim_main to have the alternative programs defined in Table 1 of Fox et al 2020. Both aircraft and MGL (truck) programs require a second method called OGI follow-up (OGI_FU) to diagnose individual leaks and perform repairs. The reference program will be the same as Step 3 above. Please see the bottom of ldar_sim_main for the method library as parameterization vary somewhat. Also note that OGI_FU does not have a minimum survey interval. The file 'altLDAR_batch_demosntration' contains the exact program parameterizations - these can be copy and pasted into ldar_sim_main.
