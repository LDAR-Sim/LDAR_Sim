# Weather Files

* [ERA5_concat](#weather-file-merger-era5concat)
* [ERA5_downloader](#weather-downloader-era5downloader)
* [ERA5_hourly_to_daily](#era5hourlytodaily)
* [weather_lookup](#weatherlookup--hourly)
* [weather_lookup_hourly](#weatherlookup--hourly)

## Weather file merger (ERA5_concat)

This file can be used to combine two different weather files

The two weather files ***MUST*** have the same ***time period*** for the program to run.

Set the following prarmaeters to use:

     folder (folder that contains all the files - default is the inputs folder)
     f1 (first file to concat)
     f2 (second file to concat)
     output (the output file name)

## Weather Downloader (ERA5_downloader)

NOTE - This can take a very long time to download data from the copernicus server,
expect to be in the queue for 1-3 hours regardless of file size be patient.

This script will download ERA reanalysis weather data. In order to run you have to:

### Setting up Copernicus

1) Setup a Copernicus account. Account setup instructions can be found at:
<https://cds.climate.copernicus.eu/#!/home>

2) Get UID and API key from account and put them in a .cdapirc file. See:
<https://cds.climate.copernicus.eu/api-how-to>

This code is based on:
<https://confluence.ecmwf.int/display/COPSRV/CDS+web+API+%28cdsapi%29+training>

### How to use ERA5_downloader

1) Follow the previous and set up Copernicus

2) Set the following inputs within the code:
    * start_year
    * end_year
    * region_name
    * facil_file
        * if no facility files are provided, you can instead use the bounding box and manually set the values.

    i) Enter facility template csv location, which must have a lat and lon column.
    File must be relative to the root folder.

    II) Fill in start year, end year, a region name (for output file tag), output resolution
   in degrees, and variable names to retrieve. Variable names  can be found at:
<https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation>

Script needs to run as long as it takes to obtain the data from the servers, but will automatically create a file in the following format: ERA5_{startyear}__{endyear}_{region}.nc

If the script ever terminates mid-download, you can still obtain the data directly from <https://cds.climate.copernicus.eu/#!/home> but the file name will not be formatted. You will need to be logged in, and the data will be under the ***Your requests*** tab.

## ERA5_hourly_to_daily

 This script is created for converting hourly ERA5 data from multiple NetCDF4 files
 into one daily ERA5 NetCDF file.

 It shows an example of combining and
 converting three hourly ERA5 NetCDF4 weather data of Alberta into one daily average
 ERA5 NetCDF4 weather data of Alberta.

## weather_lookup [ _hourly]

Reads in NetCDF files and returns the environment at a given place in time.
