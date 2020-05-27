
import requests

import numpy as np
from astropy.io import ascii

import json
from urllib.request import urlopen

def get_gender(name):
    url = "https://api.genderize.io/?name="+name
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    data = json.loads(decoded)
    return(data['gender'],data['probability'])
    # return(data['gender'])


print(get_gender('Xiangcheng'))
print(get_gender('Harley'))
print(get_gender('Santosh'))

# import gender_guesser.detector as gender
# d = gender.Detector()
#
# def get_gender(name):
#     return d.get_gender(name)



# a = {}
# a['SOC'] = {'male': 7/13,'mostly_male': 0,'unknown': 0,'andy': 0,'mostly_female': 0,'female': 6/13}
#
#
#
# url = {}
#
# url['Registered'] = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFJ9Rl-4lZ1gwFdV6KGmL7p7XT1KS84o5gd4njT0S5KhHk-zEW8dgESj6F2zQu-qopYqAsJ5GAkUIH/pub?gid=1488898563&single=true&output=csv'
#
# url['ECRs'] = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTvdVJ_JdLkM3dxWsSiQqQEMeotAGMiyS5ap2SxXpCSK7nq0cbQQvv8dS88SpfBAyHh7Snln0O-y3Kc/pub?gid=0&single=true&output=csv'
#
#
# for k in ['Registered','ECRs']:
#
#     a[k] = {}
#
#     req = requests.get(url[k])
#
#     data = ascii.read(req.text, format='csv', fast_reader=False)
#
#     FirstNames = np.array(data['First Name'])
#
#     genders = np.array([get_gender(name) for name in FirstNames])
#
#
#
#
#
#     for name, g in zip(FirstNames, genders):
#         print(name, g)
#
#
#     for g in ['male','mostly_male','unknown','andy','mostly_female','female']:
#
#         a[k][g] = len(genders[genders==g])/len(genders)
#
#
#
#
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import flares_1.analysis.plt as fplt
#
# width = 0.5
#
# labels = ['SOC','Registered', 'ECRs']
#
# running = np.zeros(len(labels))
#
# fig = plt.figure(figsize = (5, 3))
#
# left  = 0.15
# bottom = 0.15
# width = 0.5
# height = 0.8
#
# ax = fig.add_axes((left, bottom, width, height))
#
#
# for i, g in enumerate(['male','mostly_male','unknown','andy','mostly_female','female']):
#
#     c = cm.Spectral(i/6)
#
#     values = 100*np.array([a[label][g] for label in labels])
#
#     ax.bar(labels, values, width, bottom=running, label=g, color=c)
#
#     running += values
#
#
# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize = 8)
# ax.set_ylabel('Percentage')
# fig.savefig('gender.pdf')
