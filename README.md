# The LDAR Simulator V2.0

See changelog [here](changelog.md)

## About LDAR-Sim
The Leak Detection and Repair Simulator (LDAR-Sim) is an open-source modeling framework for exploring the effectiveness of methane leak detection programs. The purpose of LDAR-Sim is to enable transparent, collaborative, flexible, and intuitive investigation of emerging LDAR technologies, methods, work practices, regulations, and deployment strategies.

LDAR-Sim has many potential uses, including: 
  1) Test emissions reduction equivalence among distinct LDAR programs
  2) Evaluate performance and cost of methane sensing technologies and work practices
  3) Predict the emissions mitigation of proposed or existing fugitive methane policies
  4) Inform the development and niche of technologies and work practices

To learn more about LDAR-Sim, you can:
  1) User manual [manual](USER_MANUAL.md)
  2) Read our [story map](https://arcg.is/1rXeX10) (less technical introduction).
  3) Read [Fox et al., 2020](https://www.sciencedirect.com/science/article/pii/S0959652620352811).

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
The Fox et al. 2020 release is immortalized in a separate branch that can be found by [clicking here](https://github.com/tarcadius/LDAR_Sim/tree/Fox_etal_2020).

The Fox et al., 2020 release contains the exact code and inputs used in [our LDAR-Sim synthesis paper](https://www.sciencedirect.com/science/article/pii/S0959652620352811). We recommend using this release, especially for first time users.

Citation for this release: Fox, Thomas A., Mozhou Gao, Thomas E. Barchyn, Yorwearth L. Jamin, and Chris H. Hugenholtz. "An agent-based model for estimating emissions reduction equivalence among leak detection and repair programs." Journal of Cleaner Production (2020): 125237.

### Getting started
This guide is intended to get a user running with LDAR-Sim, **note** that even though we have supplied default variables, these should be used with caution, as many are not fully understood, are dependent on specific company workpractices, and very by geographical region.

#### Step 1: Before you begin
Read and understand the LDAR-Sim LICENSE (MIT License).
Read the user manual [manual](USER_MANUAL.md)
Read [Fox et al 2020](https://www.sciencedirect.com/science/article/pii/S0959652620352811) to familiarize yourself with LDAR-Sim fundamentals.

#### Step 2: Libraries and data
Install python 3.x. and ensure all required python modules/packages/libraries are available, as listed in the Pipfile.
The easiest way to prepare your python installation is to use [pipenv](https://pipenv.pypa.io/en/latest/) to manage a virtual environment that has the required packages. Navigate to the src directory and type: 

`pipenv install`

To make things easier, we have included windows binaries for the specific versions of cftime, GDAL, netCDF4, and pyproj. In the Pipfile, basemap is downloaded directly from [here](https://download.lfd.uci.edu/pythonlibs/r4tycu3t/basemap-1.2.2-cp37-cp37m-win_amd64.whl). If this link breaks or the package is no longer available, this is not a problem for base operations of LDAR-Sim as basemap is only used in the live plotter demonstration.

#### Step 2 Alternative: Using Requirements.txt
An alternative approach to using the PIPfile and the prebuilt wheels is by using Conda (Conda-forge) and the requirements file included in the "install folder" Follow the directions included in the Setting Up LDAR Sim Dev Environment file. The requirements.txt file can also be used with PIP and pipenv, but Python and GDAL (versions listed in the requirements file) should be installed seperately.

#### Step 3: Get Weather and Facilitity Data

The application requires both facility and weather data to run. We have included sample facilities and weather data for Alberta as an example. Checkout the [user manual](USER_MANUAL.md) for more information on formating of facility data. Weather data can either be downloaded directly or through IM3S's s3 database. ERA5 data can be downloaded directly from copernicus using the /module_code/weather/ERA5_downloader.py module (see file for instructions). Note the output data is in hourly format, therefore the flag weather_is_hourly should be set to True. Multiple ERA nc files can be concatinated with ERA5_concat.py. 

#### Step 4: Populate the simulation folder with Programs and associated methods

Checkout the [user manual](USER_MANUAL.md) for more info.

#### Step 5: Run the program

The main program is a python script called LDAR_Sim_main.py. Within the virtual environent (or where all py packages are installed) run:<br>
 ```Python LDAR_Sim_main.py {G_XXX} {P_XXX} {M_XXX} {M_YYY}``` <br> where each arguement is a path too a global, program, or method input parameter file. for example:<br>
 ```Python LDAR_Sim_main.py ./simulations/G_.yaml ./simulations/P_air.yaml ./simulations/M_aircraft.yaml ./simulations/M_OGI_FU.yaml```<br>alternatively, an entire directory can be passed using the "-P", "--in_dir" flags where all files within the directory are added to the program. for example:<br>
 ```Python LDAR_Sim_main.py --in_dir ./simulations.py``` <br> will load all files in the simulations folder into the program. <br><br>
 Output files, including maps, charts and csv files will be generated and placed in the output folder. <br><br>
 **Note**: that you can use absolute references or relative, where the the root folder is this folder.

## Other versions
Several LDAR-Sim advances are not publicly available at this time, including more advanced equivalence scenario modeling, specific method modules, and cost-effectiveness comparisons.

## Contributions and collaboration
The Included python code follows strict PEP8 Standards for formatting with the a modification to the Line Length rule, where lines cannot exceed 100 characters. Contributed code will be rejected if it does not meet this standard. We suggest using PEP8 autoformatters and Linting (Flake8 , Black) when making contributions.

The authors welcome all contributions and collaborations. Please reach out - we would love to hear from you and/or work with you!   
