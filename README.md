# The LDAR Simulator
## About LDAR-Sim
The Leak Detection and Repair Simulator (LDAR-Sim) is an open-source modeling framework for exploring the effectiveness of methane leak detection programs. The purpose of LDAR-Sim is to enable transparent, collaborative, flexible, and intuitive investigation of emerging LDAR technologies, methods, work practices, regulations, and deployment strategies.

LDAR-Sim has many potential uses, including: 
  1) Test emissions reduction equivalence among distinct LDAR programs
  2) Evaluate performance and cost of methane sensing technologies and work practices
  3) Predict the emissions mitigation of proposed or existing fugitive methane policies
  4) Inform the development and niche of technologies and work practices

To learn more about LDAR-Sim, you can:
  1) Read our [story map](https://arcg.is/1rXeX10) (less technical introduction).
  2) Read [Fox et al., 2020](https://www.sciencedirect.com/science/article/pii/S0959652620352811).

For first time users, we recommend attempting to reproduce the case study results in Fox et al. 2020 (see below).

Thomas Fox: thomas@highwoodemissions.com

Mozhou Gao: mozhou.gao@ucalgary.ca

Thomas Barchyn: tbarchyn@ucalgary.ca

Chris Hugenholtz: chhugenh@ucalgary.ca

## LDAR-Sim Licensing and Use
LDAR-Sim was invented by Thomas Fox, Mozhou Gao, Thomas Barchyn, and Chris Hugenholtz at the University of Calgary's Centre for Smart Emissions Sensing Technologies. 

LDAR-Sim is free software: you can redistribute it and/or modify it under the terms of the MIT License . LDAR-Sim is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose.

NOTE: This applies to all versions following Commit 69c27ec, Made on March 1st, 2021, Previous versions of LDAR-Sim were licensed under the GNU Affero General Public License. All redistributions or modifications made on LDAR-Sim versions created before Commit 69c27ec (March 1st, 2021) are required to be in compliance with version 3 of the GNU Affero General Public License.

## [Fox_etal_2020 Release](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020)
You are currently in the master branch, which is evolving dynamically and is not a stable release. The Fox et al. 2020 release is immortalized in a separate branch that can be found by [clicking here](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020).

The Fox et al., 2020 release contains the exact code and inputs used in [our LDAR-Sim synthesis paper](https://www.sciencedirect.com/science/article/pii/S0959652620352811). We recommend using this release, especially for first time users.

Citation for this release: Fox, Thomas A., Mozhou Gao, Thomas E. Barchyn, Yorwearth L. Jamin, and Chris H. Hugenholtz. "An agent-based model for estimating emissions reduction equivalence among leak detection and repair programs." Journal of Cleaner Production (2020): 125237.

### Getting started
This guide is intended to help interested parties reproduce the results from Fox et al 2020, which introduces LDAR-Sim and presents a case study demonstrating various hypothetical LDAR programs in Alberta, Canada.

#### Step 1: Before you begin
Read and understand the LDAR-Sim LICENSE (MIT License).
Read [Fox et al 2020](https://www.sciencedirect.com/science/article/pii/S0959652620352811) to familiarize yourself with LDAR-Sim fundamentals.

#### Step 2: Libraries and data
Install python 3.x. and ensure all required python modules/packages/libraries are available, as listed in the Pipfile.
The easiest way to prepare your python installation is to use [pipenv](https://pipenv.pypa.io/en/latest/) to manage a virtual environment that has the required packages. Navigate to the model_code directory and type: 

`pipenv install`


To make things easier, we have included windows binaries for the specific versions of cftime, GDAL, netCDF4, and pyproj. In the Pipfile, basemap is downloaded directly from [here](https://download.lfd.uci.edu/pythonlibs/s2jqpv5t/basemap-1.2.1-cp37-cp37m-win_amd64.whl). If this link breaks or the package is no longer available, this is not a problem for base operations of LDAR-Sim as basemap is only used in the live plotter demonstration.

#### Step 2 Alternative: Using Requirements.txt
An alternative approach to using the PIPfile and the prebuilt wheels is by using Conda (Conda-forge) and the requirements file included in the "install folder" Follow the directions included in the Setting Up LDAR Sim Dev Environment file. The requirements.txt file can also be used with PIP and pipenv, but Python and GDAL (versions listed in the requirements file) should be installed seperately.

#### Step 3: Reproduce OGI simulations
The ldar_sim_main file is currently configured for the OGI comparison case study presented in Fox et al 2020. Four different OGI-based LDAR programs are parameterized, which differ only according to weather and labour constraints.

Open and run ldar_sim_main.py - you may need to set your workding directory on line 32, but if you download the entire branch from Github, you should not need to. The working directory used in LDAR-Sim should contain all inputs (this is the case_study folder provided to you). If you are running LDAR-Sim for the first time, the weather data needs to be downloaded from our cloud data storage. Downloading the weather data requires credentials, and if you are planning to run the LDAR-Sim, please contact us for the required credentials. Also, you need to create **TWO** user variables in your system Environment Variables. For the first variable, please write **AWS_KEY** as the variable name and the provided ACCESS-Password as the variable value. For the second variable, please write **AWS_SEC** as the variable name and your provided SECRET-Password as the variable value. If all input files and program files are in your working directory, no other changes should be required to run the OGI scenarios from the case study. 

NOTE: As of Feb 10th, 2021: The Working Directory is set based on the location of ldar_sim_main.py and is independent of the users working directory. 

The only difference between these simulations and those in the Fox et al. 2020 study is that only 3 repeat simulations are run for each program in this demonstration, whereas in the paper, 25 simulations are run for each program to constrain uncertainty. Running 3 sets of simulations for each program over multiple years, rather than 25, will take much less time. Results should resemble Figures 2C and 2D in Fox et al 2020 but will not be exactly the same as the model is stochastic.

LDAR-Sim will automatically output a set of figures and spreadsheets comparing among programs and a folder for each program. The program-specific folders will each contain exhaustive data on leaks, facilities, inspection crews, and so on for each simulation that is run.

#### Step 4: Reproduce alt-LDAR simulations
To run the alternative programs from the case study, change the program list on line 34 of ldar_sim_main to read ['P_ref', 'P_1', 'P_2']. This will change to the appropriate input files, which are already in your working directory.

The main differences among programs are presented in Table 1 of Fox et al 2020. Both aircraft and MGL (truck) programs require a second method called OGI follow-up (OGI_FU) to diagnose individual leaks and perform repairs. The reference program will be the same as Step 3 above.

#### Step 5: Explore
Once familiar with the case study, users can explore different input configurations. Just as each simulation can compare multiple LDAR programs, so can each LDAR program consist of multiple different LDAR methods. We provide generic OGI, aircraft, and truck methods, but others can be devised using generic methods as templates. Users should explore different facility inputs, methods combinations and parameterizations, empirical emissions data, and so on.

## Other versions
Several LDAR-Sim advances are not publicly available at this time, including more advanced equivalence scenario modeling, specific method modules, and cost-effectiveness comparisons.

## Contributions and collaboration
The Included python code follows strict PEP8 Standards for formatting with the a modification to the Line Length rule, where lines cannot exceed 100 characters. Contributed code will be rejected if it does not meet this standard. We suggest using PEP8 autoformatters and Linting (Flake8 , Black) when making contributions.

The authors welcome all contributions and collaborations. Please reach out - we would love to hear from you and/or work with you!   
