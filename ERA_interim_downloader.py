#------------------------------------------------------------------------------
# Name:         ERA Interim Downloader
#
# Purpose:      Downloads ERA Interim data
#
# Authors:      Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:      2019-Jun-14
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
from ecmwfapi import ECMWFDataServer

#------------------------------------------------------------------------------

server = ECMWFDataServer()
    
# Download environmental analysis data
server.retrieve({
    'stream'    : "oper",
    'levtype'   : "sfc",
    # Snow depth, Cloud cover, Temperature, Wind components 
    'param'     : "141.128/164.128/165.128/166.128/167.128",
    'dataset'   : "interim",
    'step'      : "0",
    'grid'      : "0.5/0.5",
    'time'      : "12",
    'date'      : "2003-01-01/to/2018-12-31", # Up to 2018-12-31
    'type'      : "an",
    'class'     : "ei",
    # North/West/South/East
    'area'      : "60/240/49/250",
    'format'    : "netcdf",
    'target'    : "an_2003_2018_AB.nc"
})

# Download time-integrated environmental data
server.retrieve({
    'stream'    : "oper",
    'levtype'   : "sfc",
    # Precipitation 
    'param'     : "228.128",
    'dataset'   : "interim",
    'step'      : "6",
    'grid'      : "0.5/0.5",
    'time'      : "12",
    'date'      : "2003-01-01/to/2018-12-31", # Up to 2018-12-31
    'type'      : "fc",
    'class'     : "ei",
    # North/West/South/East
    'area'      : "60/240/49/250",
    'format'    : "netcdf",
    'target'    : "fc_2003_2018_AB.nc"
})