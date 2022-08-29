'''
A script for visualizing packet delays as a function of location.

Expecation is that you have GPS data points with associated packet delays attaced to them.

map.png should be the map area that the GPS coordinates reside
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.ticker import FormatStrFormatter

GnYlRd = cm.get_cmap('RdYlGn_r')

font = {'family' : 'Times New Roman',
        'weight' : 'bold',
        'size'   : 12}
plt.rc('font', **font)

print("Flight No Hop")
df = pd.read_csv("./flight_no_hop.csv")
df.head()
df.Longitude = df.Longitude.apply(lambda x: round(x, 5))
df.Latitude = df.Latitude.apply(lambda x: round(x, 5))
BBox = [df.Longitude.min(),   df.Longitude.max(),
         df.Latitude.min(), df.Latitude.max()]

ruh_m = plt.imread('./map.png')

delays = df.TimeLag
quantiles = df.TimeLag.quantile([0.25, 0.5, 0.75])
adj_delays = delays - min(delays) + 0.88 # normalizing then adding the mean delay back in
adj_quant = quantiles - min(adj_delays)
mean_delays = sum(adj_delays)/len(adj_delays)

print(adj_delays.describe(percentiles=[.25, .5, .75]))
# print(f"Differential delay stats (mean/med/1stQ/3rdQ): {mean_delays}, {adj_quant[0.5]}, {adj_quant[0.25]}, {adj_quant[0.75]}")
total_packet_loss = sum([(df.time[i+1] - df.time[i])/1000000000 - 1 for i in range(len(df.time)-1) if df.time[i] + 1000000000 != df.time[i+1]])
total_expected_packets = (df.time[len(df.time) - 1] - df.time[0])/1000000000
packet_drop_rate = total_packet_loss / total_expected_packets

print(f"Packet stats (total packet loss/drop rate): {total_packet_loss}, {packet_drop_rate}")

fig, axs = plt.subplots(nrows=1, ncols=2, figsize = (8,7))
fig = plt.figure()
axs = ImageGrid(fig, 111, nrows_ncols = (1,2),
        axes_pad = 0.25, cbar_location="right", 
        cbar_mode = "single", cbar_size="5%",
        cbar_pad = 0.05)

pcm = axs[0].scatter(df.Longitude, df.Latitude, zorder=1, alpha= 0.5,  c=adj_delays, cmap=GnYlRd, vmin=0.1, vmax=12, s=10) #, norm=matplotlib.colors.LogNorm())
axs[0].set_title('Single Node Network')
axs[0].set_xlim(BBox[0],BBox[1])
axs[0].set_ylim(BBox[2],BBox[3])
axs[0].set_xlabel("Latitude")
axs[0].set_ylabel("Longitude")
axs[0].set_xticklabels(axs[0].get_xticks(), rotation=45)
axs[0].xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
axs[0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
axs[0].xaxis.set_ticks(np.arange(BBox[0], BBox[1], 0.002))
axs[0].imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')


print("Flight One Hop")
df = pd.read_csv("./flight_one_hop.csv")
df.head()
df.Longitude = df.Longitude.apply(lambda x: round(x, 5))
df.Latitude = df.Latitude.apply(lambda x: round(x, 5))
BBox = [df.Longitude.min(),   df.Longitude.max(),
         df.Latitude.min(), df.Latitude.max()]

delays = df.TimeLag
quantiles = df.TimeLag.quantile([0.25, 0.5, 0.75])
adj_delays = delays - min(delays) + 0.88 # normalizing then adding the mean delay back in
adj_quant = quantiles - min(adj_delays)
mean_delays = sum(adj_delays)/len(adj_delays)
print(adj_delays.describe(percentiles=[.25, .5, .75]))
# print(f"Differential delay stats (mean/med/1stQ/3rdQ): {mean_delays}, {adj_quant[0.5]}, {adj_quant[0.25]}, {adj_quant[0.75]}")

total_packet_loss = sum([(df.time[i+1] - df.time[i])/1000000000 - 1 for i in range(len(df.time)-1) if df.time[i] + 1000000000 != df.time[i+1]])
total_expected_packets = (df.time[len(df.time) - 1] - df.time[0])/1000000000
packet_drop_rate = total_packet_loss / total_expected_packets

print(f"Packet stats (total packet loss/drop rate): {total_packet_loss}, {packet_drop_rate}")

axs[1].scatter(df.Longitude, df.Latitude, zorder=1, alpha=0.5, c=adj_delays, cmap=GnYlRd, s=10, vmin=0.1, vmax=12) #, norm=matplotlib.colors.LogNorm())
axs[1].set_title('Two Node Network')
axs[1].set_xlim(BBox[0],BBox[1])
axs[1].set_ylim(BBox[2],BBox[3])
axs[1].set_xlabel("Latitude")
axs[1].set_ylabel("Longitude")
axs[1].set_xticklabels(axs[1].get_xticks(), rotation=45)
axs[1].xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
axs[1].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
axs[1].xaxis.set_ticks(np.arange(BBox[0], BBox[1], 0.002))
axs[1].imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')

cbar = fig.colorbar(pcm, cax=axs.cbar_axes[0], ax=axs[0])
cbar.set_label("Delay (s)")

# plt.show()
plt.savefig('mapped_colors.png')
