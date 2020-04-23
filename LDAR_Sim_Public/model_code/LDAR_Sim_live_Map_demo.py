import netCDF4 as nc 
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.basemap import Basemap
import pandas as pd 
from random import random 


def livemap (weather,df,lat,lon,nc_lat,nc_lon):
    plt.ion()
    ES = [0]
    ES_daily = 0 
    day_list = [0]
    day = 0 
    fig = plt.figure(figsize=(10,10))
    ax1 = fig.add_subplot(121)
    # I used basemap package to plot map, you can use backgrounds like arcgisimage, detail can be found in https://basemaptutorial.readthedocs.io/en/latest/backgrounds.html
    m = Basemap(llcrnrlon=-120, llcrnrlat = 49.,urcrnrlon=-110,urcrnrlat =60,ax=ax1)
    m_lon, m_lat = np.meshgrid(nc_lon, nc_lat)
    xi, yi = m(m_lon,m_lat)
    # Add O&G sites
    x,y = m(lon,lat)
    m.plot(x,y,"*",color='black',markersize=8,label ="O&G sites")
    ax1.legend()
    # Add Boundaries
    m.drawcountries()
    m.drawstates(color='black')

    # Add Grid Lines
    m.drawparallels(np.arange(49., 60., 3.), labels=[1,0,0,0], fontsize=10,linewidth=0.2)
    m.drawmeridians(np.arange(-120., -110., 3.), labels=[0,0,0,1], fontsize=10,linewidth=0.2)
    

    ax2 = fig.add_subplot(122)
    ax2.set_xlim([0,20])
    ax2.set_ylim([0,12])
    ax2.set_xlabel('time')
    ax2.set_ylabel('emission size(g/s)')

    for index,row in df.iterrows():
        # fig 1 
        ax1.set_title("Map")
        tm = weather.variables['t2m'][day,:,:] -273.15
        cs = m.pcolor(xi,yi,np.squeeze(tm),alpha=0.5) # alpha represents the transparency of temperature
        
        cbar = m.colorbar(cs, location='bottom', pad="5%")
        cbar.set_label('celsius degree',fontsize =12)
        
        # current location: you can change this to the input of the livemap function, 
        # update current location of ldar team based on progress of LDAR SIM
        p_lat = row['lat']
        p_lon = row['lon']
        x2,y2 =m(p_lon,p_lat)
        m.plot(x2,y2,"*",color ='red',markersize=8,label ="location of LDAR team")
        
        # fig 2
        ax2.set_title("emissionsize vs time")
        # update the emission size 
        ES_daily = ES_daily + random() # I used random number in this demo. You also can change this to the input call function at the end of each time step 
        ES.append(ES_daily)
        #update the time 
        day = day + 1 
        day_list.append(day)
        ax2.plot(day_list,ES)
        
        plt.pause(0.4)
        
        if index!=df.shape[0]-1:
            cbar.remove()
        
    weather.close()

df = pd.read_excel('test.xlsx')
weather= nc.Dataset('an_2003_2018_AB.nc','r')
lat = np.array(df.lat)
lon = np.array(df.lon)
lon_360 = weather.variables['longitude'][:]
nc_lat = weather.variables['latitude'][:]
nc_lon =[]
for ele in lon_360: 
    a = (ele + 180) % 360 - 180
    nc_lon.append(a)
    
livemap(weather,df,lat,lon,nc_lat,nc_lon)