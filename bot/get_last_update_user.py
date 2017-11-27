import json
import os
import yaml
import pandas as pd
import random

bwd = '/Volumes/MacintoshHD/_GitHub/doctordata/bot/'
os.chdir(bwd)
chat = 446512413
datos = pd.read_csv(str(chat)+'.csv')
datos.count()['id_OSM']
random.randint(0,100)
test = datos.loc[random.randint(0, datos.count()['id_OSM']-1)]
location = {'latitude':test['latitude'],'longitude':test['longitude']}
location
with open('updates.json','r') as myfile:
    datos = myfile.readlines()

ids = 446512413
i = len(datos)-1
exitLoop = True

while exitLoop:
    if ids == yaml.load(datos[i][:-1])['message']['chat']['id']:
        print(ids)
        try:
            location = yaml.load(datos[i][:-1])['message']['location']
            print(location)
            exitLoop = False
        except:
            pass
    else:
        i = i-1

ids == yaml.load(datos[i][:-1])['message']['chat']['id']
datos
