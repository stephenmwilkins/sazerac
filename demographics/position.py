
import requests

import numpy as np
from astropy.io import ascii

import pickle

gender_dict = pickle.load(open('gender.pck','rb'))

gender_dict['Ciaran'] = ('male', 1.)

a = {}
a['SOC'] = {'male': 7, 'unknown': 0, 'female': 6}
a['SOC']['total'] =  a['SOC']['male'] + a['SOC']['female'] + a['SOC']['unknown']




url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFJ9Rl-4lZ1gwFdV6KGmL7p7XT1KS84o5gd4njT0S5KhHk-zEW8dgESj6F2zQu-qopYqAsJ5GAkUIH/pub?gid=1488898563&single=true&output=csv'

req = requests.get(url)
data = ascii.read(req.text, format='csv', fast_reader=False)
FirstNames = np.array(data['First Name'])
Position = np.array(data['Current Position'])

# positions = set(np.array(data['Current Position']))

positions = ['Undergraduate or MSc student', 'Penultimate or final year PhD student', 'Junior post-doc (<3 years experience)', 'Junior PhD student', 'Faculty/Staff', 'Senior post-doc or research fellow']


for k in positions:
    a[k] = {'male': 0., 'unknown': 0., 'female': 0.}
    Genders = np.array([gender_dict[name] for name in FirstNames[Position==k]])
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




k = 'all registrants'
a[k] = {'male': 0., 'unknown': 0., 'female': 0.}
Genders = np.array([gender_dict[name] for name in FirstNames])
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





url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS4MXIrWOQ3jwUhJz2jwgbwDs5iBY8Rz6p-VZeTzlLfJ8Fpu6Ud0lmTG0dJS5jw3NRbkPTPpnHWr0Px/pub?gid=0&single=true&output=csv'

req = requests.get(url)
data = ascii.read(req.text, format='csv', fast_reader=False)
FirstNames = np.array(data['First Name'])


k = 'Eligible for live talk'

a[k] = {'male': 0., 'unknown': 0., 'female': 0.}
Genders = np.array([gender_dict[name] for name in FirstNames])
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


# ---------------------------


k = 'Selected for live talk'

a[k] = {'male': 0., 'unknown': 0., 'female': 0.}
Genders = np.array([gender_dict[name] for name in FirstNames[:60]])
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



# --------------------------- plot



import matplotlib.pyplot as plt
import matplotlib.cm as cm
import flares_1.analysis.plt as fplt

bar_width = 1.0

positions = ['SOC', 'Undergraduate or MSc student', 'Junior PhD student', 'Penultimate or final year PhD student', 'Junior post-doc (<3 years experience)', 'Senior post-doc or research fellow', 'Faculty/Staff', 'all registrants']


labels = ['SOC', 'Undergraduate/MSc', 'Junior PhD', 'Senior PhD ', 'Junior post-doc', 'Senior post-doc/fellow', 'Faculty/Staff','all registrants']


running = np.zeros(len(positions))

fig = plt.figure(figsize = (6, 3))

left  = 0.075
bottom = 0.35
width = 0.7
height = 0.3

ax = fig.add_axes((left, bottom, width, height))

for i, g in enumerate(['male','unknown','female']):

    c = cm.coolwarm(i/2)

    values = 100*np.array([a[label][g]/a[label]['total'] for label in positions])

    ax.bar(labels, values, bar_width, bottom=running, label=g, color=c)

    if g=='male' or g=='female':
        for i,v in enumerate(values):
            ax.text(i, v/2+running[i], np.round(v,1), va='center', fontsize=5, ha='center', c='1', alpha=0.5)

    running += values

ax.axhline(50, c='1', alpha=0.2, lw=1)
ax.axvline(0.5, c='k', alpha=1, lw=1)

ax.set_xlim([-bar_width/2, len(positions)-1 + bar_width/2])
ax.set_ylim([0, 99.99])

plt.xticks(rotation=-45, ha='left')

left  = 0.075
bottom = 0.65
width = 0.7
height = 0.3

ax2 = fig.add_axes((left, bottom, width, height))

values = np.array([a[label]['total'] for label in positions])

ax2.bar(labels, values, bar_width, color='0.7')

for i,v in enumerate(values):
    ax2.text(i, v+10, int(v), va='bottom', fontsize=5, ha='center', c='k', alpha=0.5)


ax2.set_xlim([-bar_width/2, len(positions)-1 + bar_width/2])

ax2.set_xticks([])
ax2.axvline(0.5, c='k', alpha=1, lw=1)
ax2.set_ylim([0, 499.99])

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize = 8)
ax.set_ylabel('Percentage')
ax2.set_ylabel('N')
fig.savefig('figures/position.pdf')
fig.savefig('figures/position.png')
