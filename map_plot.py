'''
A script for visualizing packet delays as a function of location.

Expecation is that you have GPS data points with associated packet delays attaced to them.

map.png should be the map area that the GPS coordinates reside
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib

GnYlRd = cm.get_cmap('RdYlGn_r')

print("Flight No Hop")
df = pd.read_csv("./flight_no_hop.csv")
df.head()
BBox = [df.Longitude.min(),   df.Longitude.max(),
         df.Latitude.min(), df.Latitude.max()]

ruh_m = plt.imread('./map.png')

delays = df.TimeLag
quantiles = df.TimeLag.quantile([0.25, 0.5, 0.75])
adj_quant = quantiles - min(delays)
adj_delays = delays - min(delays)
mean_delays = sum(adj_delays)/len(adj_delays)

print(f"Differential delay stats (mean/med/1stQ/3rdQ): {mean_delays}, {adj_quant[0.5]}, {adj_quant[0.25]}, {adj_quant[0.75]}")

total_packet_loss = sum([(df.time[i+1] - df.time[i])/1000000000 - 1 for i in range(len(df.time)-1) if df.time[i] + 1000000000 != df.time[i+1]])
total_expected_packets = (df.time[len(df.time) - 1] - df.time[0])/1000000000
packet_drop_rate = total_packet_loss / total_expected_packets

print(f"Packet stats (total packet loss/drop rate): {total_packet_loss}, {packet_drop_rate}")

fig, axs = plt.subplots(nrows=1, ncols=2, figsize = (8,7))
axs[0].scatter(df.Longitude, df.Latitude, zorder=1, alpha= 0.5,  c=adj_delays, cmap=GnYlRd, vmin=0.1, vmax=12, s=10, norm=matplotlib.colors.LogNorm())
axs[0].set_title('No Hop')
axs[0].set_xlim(BBox[0],BBox[1])
axs[0].set_ylim(BBox[2],BBox[3])
axs[0].imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')


print("Flight One Hop")
df = pd.read_csv("./flight_one_hop.csv")
df.head()
BBox = [df.Longitude.min(),   df.Longitude.max(),
         df.Latitude.min(), df.Latitude.max()]

delays = df.TimeLag
quantiles = df.TimeLag.quantile([0.25, 0.5, 0.75])
adj_quant = quantiles - min(delays)
adj_delays = delays - min(delays)
mean_delays = sum(adj_delays)/len(adj_delays)
print(f"Differential delay stats (mean/med/1stQ/3rdQ): {mean_delays}, {adj_quant[0.5]}, {adj_quant[0.25]}, {adj_quant[0.75]}")

total_packet_loss = sum([(df.time[i+1] - df.time[i])/1000000000 - 1 for i in range(len(df.time)-1) if df.time[i] + 1000000000 != df.time[i+1]])
total_expected_packets = (df.time[len(df.time) - 1] - df.time[0])/1000000000
packet_drop_rate = total_packet_loss / total_expected_packets

print(f"Packet stats (total packet loss/drop rate): {total_packet_loss}, {packet_drop_rate}")

axs[1].scatter(df.Longitude, df.Latitude, zorder=1, alpha= 0.5, c=adj_delays, cmap=GnYlRd, s=10, vmin=0.1, vmax=12, norm=matplotlib.colors.LogNorm())
axs[1].set_title('One Hop')
axs[1].set_xlim(BBox[0],BBox[1])
axs[1].set_ylim(BBox[2],BBox[3])
axs[1].imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')

# fig.colorbar(mappable=cm.ScalarMappable(cmap=cm.RdYlGn), ax=axs[1])
fig.tight_layout()
# plt.show()
plt.savefig('mapped_colors.png')
