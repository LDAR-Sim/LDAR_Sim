# The LDAR Simulator
## About LDAR-Sim
The Leak Detection and Repair Simulator (LDAR-Sim) is an open-source modeling framework for exploring the effectiveness of methane leak detection programs. The purpose of LDAR-Sim is to enable transparent, collaborative, flexible, and intuitive investigation of emerging LDAR technologies, methods, work practices, regulations, and deployment strategies.

To learn more about LDAR-Sim, you can read about it in *this paper*.

Thomas Fox: t.arcadius@gmail.com / thomas.fox@ucalgary.ca

Mozhou Gao: mozhou.gao@ucalgary.ca

Thomas Barchyn: tbarchyn@ucalgary.ca

Chris Hugenholtz: chhugenh@ucalgary.ca

## LDAR-Sim Licensing and Use
LDAR-Sim was invented by Thomas Fox, Mozhou Gao, Thomas Barchyn, and Chris Hugenholtz at the University of Calgary's Centre for Smart Emissions Sensing Technologies. 

LDAR-Sim is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3. LDAR-Sim is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU Affero General Public License for more details.

This code may not be modified and distributed without sharing the changes, pursuant to the GNU Affero GPL v3 License.

## Fox_etal_2020_MS1_preprint Release
This release contains the exact code and inputs used in our LDAR-Sim synthesis paper (currently in preprint and in review). Although this version may change with peer review, we recommend using this release.

Preprint paper (Fox et al 2020): #PREPRINT LINK#
Citation for this release: #DOI#

### Getting started
This guide is intended to help interested parties reproduce the results from Fox et al 2020, which introduces LDAR-Sim and presents a case study demonstrating various hypothetical LDAR programs in Alberta, Canada.

#### Step 1: Before you begin
Read and understand the LDAR-Sim LICENSE (GNU Affero General Public License Version 3).
Read Fox et al 2020 to familiarize yourself with LDAR-Sim fundamentals.

#### Step 2: Libraries and data
Install python 3.x. and ensure all required python modules/packages/libraries are available: numpy, pandas, datetime, csv, sys, os, random, math, plotnine, ephem, gc, time, warnings, gdal (osgeo), osr (osgeo), Dataset (netCDF4), date_format (mizani.formatters), ECMWFDataServer (ecmwfapi).

Open ldar_sim_main.py and set your working directory on line 49.
Ensure that all input files and program files are in your working directory.
No other changes should be required to run the OGI scenarios from the case study.

#### Step 3: Reproduce OGI simulations
Run LDAR-Sim from the file 'ldar_sim_main.py'. This file lets users define global parameters, inputs, and as many different LDAR programs as desired. Program intercomparisons are made, output, and plotted automatically.

Just as each simulation can compare multiple LDAR programs, so can each LDAR program consist of multiple different LDAR methods. We provide generic OGI, aircraft, and truck methods, but others can be devised using generic methods as templates.

The ldar_sim_main file is currently configured for the OGI comparison case study presented in Fox et al 2020. Four different OGI-based LDAR programs are parameterized, which differ only according to weather and labour constraints.

These reproducibility simulations will take some time to run, as 25 sets of simulations are used for each program over multiple years. Results should resemble Figures 2C and 2D in Fox et al 2020 but will not be exactly the same as the model is stochastic.

#### Step 4: Reproduce alt-LDAR simulations
Reconfigure ldar_sim_main to have the alternative programs defined in Table 1 of Fox et al 2020. Both aircraft and MGL (truck) programs require a second method called OGI follow-up (OGI_FU) to diagnose individual leaks and perform repairs. The reference program will be the same as Step 3 above. Please see the bottom of ldar_sim_main for the method library as parameterizations vary somewhat. Also note that OGI_FU does not have a minimum survey interval. The file 'altLDAR_batch_demonstration.py' contains the exact program parameterizations - these can be copy and pasted into 'ldar_sim_main.py'.

## Other versions
Several LDAR-Sim advances are not publicly available at this time, including more advanced equivalence scenario modeling, specific method modules, and cost-effectiveness comparisons.
