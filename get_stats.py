#------------------------------------------------------------------------------
# Name:         LDAR-Sim Get Stats
#
# Purpose:      Get outputs statistics averaged over multiple simulations.
#               
#               
#
# Authors:      Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:      2019-08-26
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#1 Propotion sites available - 'timeseries'
#--- load each file, remove spin-up, average in file, average among files

#2 Sites surveyed (close-range/screening) - per day - 'timeseries'
#3 Flagged sites - per day - 'timeseries'
#4 Tagged leaks - per site per year - 'timeseries'
#5 Emissions (kg) - per site per day - 'timeseries'

# For variables 2, 3, 5:
# 1) load each timeseries file
# 2) remove spin-up
# 3) sum all entries
# 4) divide by number sites
# 5) divide by number of days
# 6) average across simulations

# For variable 4, first must calculate number new tags = (D3-D2) + (F3-F2)
import os
import pandas as pd
import numpy as np

OD = "D:/OneDrive - University of Calgary/Documents/Thomas/PhD/Thesis/LDAR_Sim/manuscript1/figures_tables/demonstration/OGI_batch_manuscript_25/"

program_name = 'P_W_L'
screening = False
method = 'OGI'
path = OD + program_name
os.chdir(path)
spin_up = 365
n_sites = 1169



# For each folder, build a dataframe combining all necessary files
file_list = []

for j in os.listdir(path):
    if os.path.isfile(os.path.join(path,j)) and 'timeseries' in j:
        file_list.append(j)

# Read csv files to lists
all_data = []

for file in file_list:
    file_path = path + '/' + file
    all_data.append(pd.read_csv(file_path))

###############################################################################           
# EMISSIONS
df = []
for i in all_data:
    df.append(i["daily_emissions_kg"])      
df = pd.concat(df, axis = 1, keys = [i for i in range(len(all_data))]) 
    
# Axe spinup
df = df.drop(df.index[0:spin_up])

# Divide each entry by the number of sites, then average entire matrix
df = df / n_sites
mean_emissions = df.stack().mean()
std_emissions = df.stack().std()

print (program_name + ' mean daily site emissions = ' + str(mean_emissions) + ' ± ' + str(std_emissions) + ' kg/site/day')

###############################################################################           
# FLAGGED SITES
if screening == True:
    df = []
    for i in all_data:
        df.append(i[method + '_eff_flags'])      
    df = pd.concat(df, axis = 1, keys = [i for i in range(len(all_data))]) 
        
    # Axe spinup
    df = df.drop(df.index[0:spin_up])
    
    # Average matrix
    mean_flags = df.stack().mean()
    std_flags = df.stack().std()
    
    print (program_name + ' mean daily flags = ' + str(mean_flags) + ' ± ' + str(std_flags))

###############################################################################           
# SITES SURVEYED
df = []
for i in all_data:
    df.append(i[method + '_sites_visited'])      
df = pd.concat(df, axis = 1, keys = [i for i in range(len(all_data))]) 
    
# Axe spinup
df = df.drop(df.index[0:spin_up])

# Divide each entry by the number of sites, then average entire matrix
mean_visits = df.stack().mean()
std_visits = df.stack().std()
    
print (program_name + ' mean daily visits = ' + str(mean_visits) + ' ± ' + str(std_visits))
    
if screening == True:
    df = []
    for i in all_data:
        df.append(i['OGI_FU_sites_visited'])      
    df = pd.concat(df, axis = 1, keys = [i for i in range(len(all_data))]) 
        
    # Axe spinup
    df = df.drop(df.index[0:spin_up])
    
    # Divide each entry by the number of sites, then average entire matrix
    mean_visits = df.stack().mean()
    std_visits = df.stack().std()
        
    print (program_name + ' mean daily follow-up visits = ' + str(mean_visits) + ' ± ' + str(std_visits))
    
###############################################################################           
# PROPORTION SITES AVAILABLE
df = []
for i in all_data:
    df.append(i[method + '_prop_sites_avail'])      
df = pd.concat(df, axis = 1, keys = [i for i in range(len(all_data))]) 
    
# Axe spinup
df = df.drop(df.index[0:spin_up])

# Average matrix
mean_prop_avail = df.stack().mean()
std_prop_avail = df.stack().std()

print (program_name + ' mean proportion of sites available = ' + str(mean_prop_avail) + ' ± ' + str(std_prop_avail))

if screening == True:
    df = []
    for i in all_data:
        df.append(i['OGI_FU_prop_sites_avail'])      
    df = pd.concat(df, axis = 1, keys = [i for i in range(len(all_data))]) 
        
    # Axe spinup
    df = df.drop(df.index[0:spin_up])
    
    # Average matrix
    mean_prop_avail = df.stack().mean()
    std_prop_avail = df.stack().std()
    
    print (program_name + ' follow-up mean proportion of sites available = ' + str(mean_prop_avail) + ' ± ' + str(std_prop_avail))
    

###############################################################################           
# TAGGED LEAKS
n_tags = []
cum_repaired_leaks = []

for i in all_data:
    n_tags.append(i['n_tags']) 
    cum_repaired_leaks.append(i['cum_repaired_leaks'])    
    
n_tags = pd.concat(n_tags, axis = 1, keys = [i for i in range(len(all_data))]) 
cum_repaired_leaks = pd.concat(cum_repaired_leaks, axis = 1, keys = [i for i in range(len(all_data))]) 

zero_data = np.zeros(shape=(n_tags.shape[0],n_tags.shape[1]))
df = pd.DataFrame(zero_data)
    
for i in range(1, df.shape[0]):
    for j in range(df.shape[1]):
        df.iloc[i][j] = (n_tags.iloc[i][j] - n_tags.iloc[i-1][j]) + (cum_repaired_leaks.iloc[i][j] - cum_repaired_leaks.iloc[i-1][j])
    
# Axe spinup
df = df.drop(df.index[0:spin_up])

# Average matrix
mean_prop_avail = df.stack().mean()
std_prop_avail = df.stack().std()

print (program_name + ' mean tagged leaks per day = ' + str(mean_prop_avail) + ' ± ' + str(std_prop_avail))    
