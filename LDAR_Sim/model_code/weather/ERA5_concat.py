import os
import xarray
from pathlib import Path

'''
Concatenate two weather netcdf files on the time column. Keep Lat Long coordinates the same
'''

# Inputs
folder = 'inputs_template'
f1 = "ERA5_2017_2018_AB.nc"
f2 = "ERA5_2019_2020_AB.nc"
output = "ERA5_2017_2020_AB.nc"


root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent.parent
os.chdir(root_dir/folder)
ds = xarray.open_mfdataset([f1, f2], combine='by_coords', concat_dim="time", decode_times=False)
ds.to_netcdf(output)
