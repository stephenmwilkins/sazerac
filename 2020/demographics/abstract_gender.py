
import requests

import numpy as np
from astropy.io import ascii
import pickle

import json
from urllib.request import urlopen

gender_dict = pickle.load(open('gender.pck','rb'))
gender_dict['Ciaran'] = ('male', 1.)

import string



def get_abstract_gender(abstract):


    printable = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    filter(lambda x: x in printable, abstract)
    s = ''.join(filter(lambda x: x in printable, abstract))
    s.replace(' ','+')

    url = "https://api.textgain.com/gender?q="+s+"&key=5ecfac24627bb41809a2e334"
    response = urlopen(url)
    decoded = response.read().decode('utf-8')
    d = json.loads(decoded)
    return d






url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS4MXIrWOQ3jwUhJz2jwgbwDs5iBY8Rz6p-VZeTzlLfJ8Fpu6Ud0lmTG0dJS5jw3NRbkPTPpnHWr0Px/pub?gid=0&single=true&output=csv'

req = requests.get(url)
data = ascii.read(req.text, format='csv', fast_reader=False)
FirstNames = np.array(data['First Name'])
Abstracts = np.array(data['Abstract'])


r = {'name':[],'abstract':[]}

for name,abstract in zip(FirstNames, Abstracts):

    ng = gender_dict[name]

    if ng[0]=='male':
        nval = 1 - ng[1]
    elif ng[0]=='female':
        nval = ng[1]
    else:
        nval = 0.5

    r['name'].append(nval)

    d = get_abstract_gender(abstract)

    if d['gender']=='m':
        aval = 1 - d['confidence']
    elif d['gender']=='f':
        aval = d['confidence']
    else:
        aval = 0.5

    r['abstract'].append(aval)

    print(name, nval, aval)

pickle.dump(r, open('name_abstract.pck','wb'))
