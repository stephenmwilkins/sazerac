from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
import requests
# import pandas

from astropy.io import ascii

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


cmap = plt.get_cmap('BuPu')
new_cmap = truncate_colormap(cmap, 0.4, 1.0)



url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFJ9Rl-4lZ1gwFdV6KGmL7p7XT1KS84o5gd4njT0S5KhHk-zEW8dgESj6F2zQu-qopYqAsJ5GAkUIH/pub?gid=1488898563&single=true&output=csv'

req = requests.get(url)
data = ascii.read(req.text, format='csv', fast_reader=False)
country = np.array(data['Country'])

print(len(set(country)))


left  = 0.0
bottom = 0.0
width = 0.775
height = 1.0

fig = plt.figure(figsize = (20/width,10))

ax = fig.add_axes((left, bottom, width, height))

# fig.patch.set_visible(False)
ax.axis('off')

map = Basemap(projection='cyl')

map.readshapefile('Longitude_Graticules_and_World_Countries_Boundaries-shp/world', 'world', drawbounds = False)

map.drawcoastlines(linewidth = 0.0, color = (0.5,0.5,0.5))





patches = []
empty_patches = []
N = []

# print len(map.Areas_info)

for info, shape in zip(map.world_info, map.world):

    n = len(country[country==info['CNTRY_NAME']])

    if n>0:
        N.append(np.log10(n))
        patches.append( Polygon(np.array(shape), True) )
    else:
        empty_patches.append( Polygon(np.array(shape), True) )



# p = PatchCollection(patches, facecolor= face_colours, edgecolor=(0.5,0.5,0.5), linewidths=0.5, zorder=2)
p = PatchCollection(patches, cmap=new_cmap, zorder=2)
p.set_array(np.array(N))
ax.add_collection(p)

from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="2%", pad=1)

cbar = plt.colorbar(p, cax=cax, ticks=[0,0.3,0.7,1,1.3,1.7,2])
cbar.ax.set_yticklabels(['1','2','5','10','20','50','100'])  # vertically oriented colorbar)
# cbar.ax.set_ylabel(r'$\rm log_{10}(N)$', fontsize=30)
cbar.ax.tick_params(labelsize=20)


# fig.colorbar(p)

p = PatchCollection(empty_patches, facecolor=(0.9,0.9,0.9), zorder=2)
ax.add_collection(p)





plt.savefig('figures/geo.png')
