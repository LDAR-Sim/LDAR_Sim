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
    
server.retrieve({
    'stream'    : "oper",
    'levtype'   : "sfc",
    # Snow depth, Cloud cover, Temperature, Wind speed, Precipitation
    'param'     : "141.128/164.128/167.128/207.128/228.128",
    'dataset'   : "interim",
    'step'      : "0",
    'grid'      : "0.75/0.75",
    'time'      : "12",
    'date'      : "2003-01-01/to/2018-12-31",
    'type'      : "an",
    'class'     : "ei",
    # North/West/South/East
    'area'      : "60/-120/49/-110",
    'format'    : "netcdf",
    'target'    : "LDAR_SIM_2003_2018_AB.nc"
})

# Notes
# It may be that Precipitation variable requires a step
# If so, it may be that step and time cannot  both be specified?
# If so, may have to download instantaneous and time-integrated data separately
# Alternatively, could use a different measure of precip (e.g. rate)
# Not clear how coordinates translate to 360? Automatic?
# May want to also download errors at some point (type = "ae")