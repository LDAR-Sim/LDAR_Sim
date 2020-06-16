# The LDAR Simulator
## About LDAR-Sim
The Leak Detection and Repair Simulator (LDAR-Sim) is an open-source modeling framework for exploring the effectiveness of methane leak detection programs. The purpose of LDAR-Sim is to enable transparent, collaborative, flexible, and intuitive investigation of emerging LDAR technologies, methods, work practices, regulations, and deployment strategies.

To learn more about LDAR-Sim, you can read about it in *this paper*.

For first time users, we recommend attempting to reproduce the case study results in Fox et al. 2020 (see below).

Thomas Fox: t.arcadius@gmail.com / thomas.fox@ucalgary.ca

Mozhou Gao: mozhou.gao@ucalgary.ca

Thomas Barchyn: tbarchyn@ucalgary.ca

Chris Hugenholtz: chhugenh@ucalgary.ca

## LDAR-Sim Licensing and Use
LDAR-Sim was invented by Thomas Fox, Mozhou Gao, Thomas Barchyn, and Chris Hugenholtz at the University of Calgary's Centre for Smart Emissions Sensing Technologies. 

LDAR-Sim is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3. LDAR-Sim is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GNU Affero General Public License for more details.

This code may not be modified without sharing the changes, pursuant to the GNU Affero GPL v3 License.

## [Fox_etal_2020_preprint Release](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020_preprint)
This release contains the exact code and inputs used in our LDAR-Sim synthesis paper (currently in preprint and in review). Although this version may change with peer review, we recommend using this release, especially for first time users.

Preprint paper (Fox et al 2020): #PREPRINT LINK#
Citation for this release: #DOI#

You are currently in the master branch, which is evolving dynamically and is not a stable release. The Fox et al. 2020 preprint release is immortalized in a separate branch that can be found by [clicking here](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020_preprint).

### Getting started
This guide is intended to help interested parties reproduce the results from Fox et al 2020, which introduces LDAR-Sim and presents a case study demonstrating various hypothetical LDAR programs in Alberta, Canada.

#### Step 1: Before you begin
Read and understand the LDAR-Sim LICENSE (GNU Affero General Public License Version 3).
Read Fox et al 2020 to familiarize yourself with LDAR-Sim fundamentals.

#### Step 2: Libraries and data
Install python 3.x. and ensure all required python modules/packages/libraries are available, as listed in the Pipfile.
The easiest way to prepare your python installation is to use [pipenv](https://pipenv.pypa.io/en/latest/) to manage a virtual environment that has the required packages. Navigate to the model_code directory and type: 

`pipenv install`

To make things easier, we have included windows binaries for the specific versions of cftime, GDAL, netCDF4, and pyproj. In the Pipfile, basemap is downloaded directly from https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/basemap-1.2.1-cp37-cp37m-win_amd64.whl. If this link breaks or the package is no longer available, this is not a problem for base operations of LDAR-Sim as basemap is only used in the live plotter demonstration.

#### Step 3: Reproduce OGI simulations
The ldar_sim_main file is currently configured for the OGI comparison case study presented in Fox et al 2020. Four different OGI-based LDAR programs are parameterized, which differ only according to weather and labour constraints.

Open and run ldar_sim_main.py - you may need to set your workding directory on line 32, but if you download the entire preprint branch from Github, you should not need to. The working directory used in LDAR-Sim should contain all inputs (this is the case_study folder provided to you). If all input files and program files are in your working directory, no other changes should be required to run the OGI scenarios from the case study. 

The only difference between these simulations and those in the Fox et al. 2020 is that only 3 repeat simulations are run for each program in this demonstration, whereas in the paper, 25 simulations are run for each program to constrain uncertainty. Running 3 sets of simulations for each program over multiple years, rather than 25, will take much less time. Results should resemble Figures 2C and 2D in Fox et al 2020 but will not be exactly the same as the model is stochastic.

LDAR-Sim will automatically output a set of figures and spreadsheets comparing between programs and a folder for each program. The program-specific folders will each contain exhaustive data on leaks, facilities, inspection crews, and so on for each simulation that is run.

#### Step 4: Reproduce alt-LDAR simulations
To run the alternative programs from the case study, change the program list on line 34 of ldar_sim_main to read ['P_ref', 'P_1', 'P_2']. This will change to the appropriate input files, which are already in your working directory.

The main differences among programs are presented in Table 1 of Fox et al 2020. Both aircraft and MGL (truck) programs require a second method called OGI follow-up (OGI_FU) to diagnose individual leaks and perform repairs. The reference program will be the same as Step 3 above.

#### Step 5: Explore
Once familiar with the case study, users can explore different input configurations. Just as each simulation can compare multiple LDAR programs, so can each LDAR program consist of multiple different LDAR methods. We provide generic OGI, aircraft, and truck methods, but others can be devised using generic methods as templates. Users should explore different facility inputs, methods combinations and parameterizations, empirical emissions data, and so on.

## Other versions
Several LDAR-Sim advances are not publicly available at this time, including more advanced equivalence scenario modeling, specific method modules, and cost-effectiveness comparisons.
