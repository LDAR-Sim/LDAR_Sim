from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib import ticker
from mpl_toolkits.basemap import Basemap
import pandas as pd
import os

# Output folder with two programs to compare
input_directory = 'C:/Users/tarca/PycharmProjects/LDAR_Sim/Github/LDAR_Sim/inputs_template/outputs/'


def livemap(input_directory):
    os.chdir(input_directory)
    ref_sites = pd.read_csv(input_directory + '/P_ref/sites_output_0.csv')
    alt_sites = pd.read_csv(input_directory + '/P_alt/sites_output_0.csv')
    ref_costs = pd.read_csv(input_directory + '/P_ref/timeseries_output_0.csv')
    alt_costs = pd.read_csv(input_directory + '/P_alt/timeseries_output_0.csv')
    em_ts = pd.read_csv(input_directory + 'mean_emissions.csv')
    al_ts = pd.read_csv(input_directory + 'mean_active_leaks.csv')

    os.chdir("..")
    weather = Dataset('an_2003_2018_AB.nc', 'r')
    os.chdir(input_directory)

    lat_ref = np.array(ref_sites['lat'])  # [ref_samples]
    lon_ref = np.array(ref_sites['lon'])  # [ref_samples]
    lat_alt = np.array(alt_sites['lat'])  # [alt_samples]
    lon_alt = np.array(alt_sites['lon'])  # [alt_samples]

    # Get grid positions
    nc_lat = weather.variables['latitude'][:]
    nc_lon = []
    lon_360 = weather.variables['longitude'][:]
    for ele in lon_360:
        a = (ele + 180) % 360 - 180
        nc_lon.append(a)

    plt.ion()

    dates = pd.to_datetime((ref_costs.datetime))
    n_sims = len(ref_costs)
    day_list = []
    date_form = DateFormatter("%e %b %Y")

    fig = plt.figure(figsize=(15, 20))

    # Figure 1: Map
    ax1 = fig.add_subplot(121)
    map = Basemap(
        epsg=3401, llcrnrlon=-121, llcrnrlat=48.5,
        urcrnrlon=-107, urcrnrlat=60.5, resolution='i',
        area_thresh=10000.)
    map.fillcontinents(color='#272626', alpha=0.7)
    map.drawcountries(color='white', linewidth=1)
    map.drawstates(color='white', linewidth=1)
    map.drawparallels(np.arange(49., 60., 3.), color="white", labels=[
                      1, 0, 0, 0], fontsize=10, linewidth=0.2)
    map.drawmeridians(np.arange(-120., -110., 3.), color="white",
                      labels=[0, 0, 0, 1], fontsize=10, linewidth=0.2)

    # Build grid for raster
    m_lon, m_lat = np.meshgrid(nc_lon, nc_lat)
    xi, yi = map(m_lon, m_lat)

    # Add O&G facilities to map
    x1, y1 = map(lon_alt, lat_alt)
    x2, y2 = map(lon_ref, lat_ref)
    x1 = np.append(x1, x2)
    y1 = np.append(y1, y2)
    vals = ['Regulatory Program'] * int(len(x1) / 2) + ['Alternative Program'] * int(len(x1) / 2)
    df = pd.DataFrame(dict(x1=x1, y1=y1, vals=vals))
    groups = df.groupby('vals')
    colors = {'Regulatory Program': '#b87a02', 'Alternative Program': '#396dc5'}
    for name, group in groups:
        map.plot(group.x1, group.y1, marker='o', linestyle='', ms=4, label=name, c=colors[name],
                 markeredgecolor='black', markeredgewidth=0.8)
    ax1.legend(markerscale=4, prop={'size': 15}, loc=9)

    # Figure 2: Emissions
    ref_emissions = np.array(em_ts['mean'][0:(n_sims-1)])
    alt_emissions = np.array(em_ts['mean'][-(n_sims-1):])
    ES1 = []
    ES2 = []
    ax2 = fig.add_subplot(322)
    # ax2.set_xlim([0, 1000])
    # ax2.set_ylim([0, 15])
    ax2.xaxis.set_major_formatter(date_form)
    ax2.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax2.set_xlabel('')
    ax2.set_ylabel('Average emission rate \n(kg/day/facility)', fontsize=13)

    # Figure 3: Active Leaks
    ref_leaks = np.array(al_ts['mean'][0:(n_sims-1)])
    alt_leaks = np.array(al_ts['mean'][-(n_sims-1):])
    AL1 = []
    AL2 = []
    ax3 = fig.add_subplot(324)
    # ax3.set_xlim([0, 1000])
    # ax3.set_ylim([0, 650])
    ax3.xaxis.set_major_formatter(date_form)
    ax3.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax3.set_xlabel('')
    ax3.set_ylabel('Total active leaks \n(all facilities)', fontsize=13)

    # Figure 4: Cost
    ref_costs = np.array(ref_costs['OGI_cost']) / 500
    alt_costs = (np.array(alt_costs['aircraft_cost']) + np.array(alt_costs['OGI_FU_cost'])) / 500
    C1 = []
    C2 = []
    ax4 = fig.add_subplot(326)
    # ax4.set_xlim([dates[0], dates[len(dates) - 1]])
    ax4.xaxis.set_major_formatter(date_form)
    ax4.xaxis.set_major_locator(ticker.MaxNLocator(5))
    ax4.set_ylabel('Estimated program cost \n(USD/facility/year)', fontsize=13)

    # Plotting loops
    pi = 20  # Plotting interval
    mi = 60  # Mapping interval (must be a multiple of the plotting interval)
    for t in range(int(n_sims/pi)):
        day_list.append(dates[int(t*pi)])

        if int(t*pi) > 120:
            date_form = DateFormatter("%b %Y")
            ax2.xaxis.set_major_formatter(date_form)
            ax3.xaxis.set_major_formatter(date_form)
            ax4.xaxis.set_major_formatter(date_form)

        # Figure 1: Map
        if ((t*pi)/mi).is_integer():
            if (t*pi)/mi >= 2:
                pass
                # cbar.remove()
                # cs.remove()
            tm = weather.variables['t2m'][int(t*pi), :, :] - 273.15
            cs = map.pcolor(xi, yi, np.squeeze(tm), alpha=0.8,
                            ax=ax1, vmin=-20, vmax=20, cmap='jet')
            cbar = map.colorbar(cs, location='bottom', pad="5%", ax=ax1)
            cbar.set_alpha(1)
            cbar.draw_all()
            cbar.set_label('Temperature (' + u'\N{DEGREE SIGN}' + 'C)', fontsize=12)
        ann = ax1.annotate(dates[int(t * pi)].strftime("%b %Y"), xy=(0.38, 0.83),
                           xycoords='axes fraction', fontsize=17, color='white')

        # Figure 2: Emissions
        ES1.append(ref_emissions[int(t*pi)])
        ES2.append(alt_emissions[int(t*pi)])
        ax2.plot(day_list, ES1, color='#b87a02')
        ax2.plot(day_list, ES2, color='#396dc5')

        # Figure 3: Active leaks
        AL1.append(ref_leaks[int(t*pi)])
        AL2.append(alt_leaks[int(t*pi)])
        ax3.plot(day_list, AL1, color='#b87a02')
        ax3.plot(day_list, AL2, color='#396dc5')

        # Figure 4: Costs
        C1.append(sum(ref_costs[0:t*pi]) * 365/((t+1)*pi))
        C2.append(sum(alt_costs[0:t*pi]) * 365/((t+1)*pi))
        ax4.plot(day_list, C1, color='#b87a02')
        ax4.plot(day_list, C2, color='#396dc5')

        plt.pause(0.2)
        ann.remove()

        # if int(t*pi) != ref_costs.shape[0] - 1:
        #     cbar.remove()

    weather.close()


livemap(input_directory)
