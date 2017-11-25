import json
import pandas as pd
import os
import sys

pwd = os.getcwd()
pwd = '/Volumes/MacintoshHD/_GitHub/doctordata'
dwd = pwd + '/api/csv/'
jwd = pwd + '/api/json/'
pwd
os.chdir(dwd)
files = os.listdir()
edit = []
missing = []

for fichero in files:
    if fichero.endswith('-edit.csv'):
        edit.append(fichero)
        data = pd.read_csv(fichero)
    if fichero.endswith('-missing_AYU.csv'):
        missing.append(fichero)

for fichero in edit:
    data = pd.read_csv(fichero)
    conflictList = []
    for i in range(max(data.count())):
        conflictList.append(dict({"conflicts":[[{"latitude": data.loc[i]['lat_OSM'], "source": "OSM"},{"latitude": data.loc[i]['LATITUD'], "source": "MAD"}],[{"longitude": data.loc[i]['lon_OSM'],"source": "OSM"},{"longitude": data.loc[i]['LONGITUD'],"source": "MAD"}]],"node":i,"position":{"latitude":data.loc[i]['LATITUD'],"longitude":data.loc[i]['LONGITUD']}}))
    os.chdir(jwd)
    with open(fichero[:-4]+'.json','w') as myfile:
        json.dump(conflictList, myfile, indent=4)
    myfile.close()
    os.chdir(dwd)
