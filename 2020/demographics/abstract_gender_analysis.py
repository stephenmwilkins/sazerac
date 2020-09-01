
import requests

import numpy as np
from astropy.io import ascii

import pickle

r = pickle.load(open('name_abstract.pck','rb'))



import matplotlib.pyplot as plt
import matplotlib.cm as cm
import flares_1.analysis.plt as fplt



fig = plt.figure(figsize = (4, 4))

left  = 0.15
bottom = 0.15
width = 0.8
height = 0.8

ax = fig.add_axes((left, bottom, width, height))

ax.scatter(r['name'],r['abstract'], alpha=0.1)

from scipy import stats

slope, intercept, r_value, p_value, std_err = stats.linregress(r['name'],r['abstract'])
print(slope)
print(intercept)

ax.plot([0,1],[0,1],c='k',alpha=0.2,lw=2)
ax.plot([0,1],slope*np.array([0,1])+intercept,c='k',alpha=1,lw=1)


plt.xticks([0,1], ['M','F'])


ax.set_xlabel('Name')
ax.set_ylabel('Abstract')
ax.set_xlim([0,1])
ax.set_ylim([0,1])


plt.xticks([0,1], ['M','F'])
plt.yticks([0,1], ['M','F'])

fig.savefig('abstract_gender.pdf')
# fig.savefig('position.png')
