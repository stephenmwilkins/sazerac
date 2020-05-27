
import requests

import numpy as np
from astropy.io import ascii

import json
from urllib.request import urlopen

def get_gender(name):

    try:
        name = name.split(' ')[-1]
        url = "https://api.genderize.io/?name="+name
        response = urlopen(url)
        decoded = response.read().decode('utf-8')
        d = json.loads(decoded)
        print(name, d['gender'],d['probability'])
        if not d['gender']:
            d['gender'] = 'unknown'
            d['probability'] = 1
        return(d['gender'], float(d['probability']))
    except:
        print(name, 'unknown')
        return('unknown', 1)






a = {}
a['SOC'] = {'male': 7, 'unknown': 0, 'female': 6}
a['SOC']['total'] =  a['SOC']['male'] + a['SOC']['female'] + a['SOC']['unknown']


url = {}

url['Registered'] = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFJ9Rl-4lZ1gwFdV6KGmL7p7XT1KS84o5gd4njT0S5KhHk-zEW8dgESj6F2zQu-qopYqAsJ5GAkUIH/pub?gid=1488898563&single=true&output=csv'

url['ECRs'] = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTvdVJ_JdLkM3dxWsSiQqQEMeotAGMiyS5ap2SxXpCSK7nq0cbQQvv8dS88SpfBAyHh7Snln0O-y3Kc/pub?gid=0&single=true&output=csv'




for k in ['Registered','ECRs']:

    a[k] = {'male': 0., 'unknown': 0., 'female': 0.}

    req = requests.get(url[k])

    data = ascii.read(req.text, format='csv', fast_reader=False)

    FirstNames = np.array(data['First Name'])

    Genders = np.array([get_gender(name) for name in FirstNames])

    for g in Genders:

        if g[0] == 'male':
            a[k]['male'] += float(g[1])
            a[k]['female'] += 1-float(g[1])
        if g[0] == 'female':
            a[k]['female'] += float(g[1])
            a[k]['male'] += 1-float(g[1])
        if g[0] == 'unknown':
            a[k]['unknown'] += 1

    a[k]['total'] =  a[k]['male'] + a[k]['female'] + a[k]['unknown']



import matplotlib.pyplot as plt
import matplotlib.cm as cm
import flares_1.analysis.plt as fplt

width = 0.5

labels = ['SOC', 'Registered', 'ECRs']

running = np.zeros(len(labels))

fig = plt.figure(figsize = (5, 3))

left  = 0.15
bottom = 0.15
width = 0.5
height = 0.8

ax = fig.add_axes((left, bottom, width, height))



for i, g in enumerate(['male','unknown','female']):

    c = cm.coolwarm(i/2)

    values = 100*np.array([a[label][g]/a[label]['total'] for label in labels])

    ax.bar(labels, values, width, bottom=running, label=g, color=c)

    running += values


ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize = 8)
ax.set_ylabel('Percentage')
fig.savefig('gender.pdf')
