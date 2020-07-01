

import requests
import numpy as np
from astropy.io import ascii

import json
from urllib.request import urlopen

import pickle


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







url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQFJ9Rl-4lZ1gwFdV6KGmL7p7XT1KS84o5gd4njT0S5KhHk-zEW8dgESj6F2zQu-qopYqAsJ5GAkUIH/pub?gid=1488898563&single=true&output=csv'


gender = {}
req = requests.get(url)

data = ascii.read(req.text, format='csv', fast_reader=False)
FirstNames = data['First Name']

print(len(FirstNames))
print(len(set(FirstNames)))


gender = pickle.load(open('gender.pck','rb'))

for name in FirstNames:
    if name not in list(gender.keys()):
        gender[name] = get_gender(name)


pickle.dump(gender, open('gender.pck','wb'))
