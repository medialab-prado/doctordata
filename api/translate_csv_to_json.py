import json
import pandas as pd
import os
import sys

pwd = os.getcwd()
pwd = '/Volumes/MacintoshHD/_GitHub/doctordata'
cwd = pwd + '/api/csv/'
jwd = pwd + '/api/json/'
dwd = pwd + '/api/data/'

os.chdir(cwd)
filelist = [ f for f in os.listdir() if f.endswith(".csv") ]
edit = []
missing = []

os.chdir(dwd)
indice = pd.read_csv('indice.csv',encoding='latin-1',delimiter=';',index_col=0)

results = {}
for key, df_gb in indice.groupby(indice.index):
    results[str(key)] = df_gb.to_dict('list')

for key in results.keys():
    results[key]['SEARCH'] = results[key]['SEARCH'][0][1:-1]
    results[key]['distance_CLOSE'] = results[key]['distance_CLOSE'][0]
    results[key]['distance_SAME'] = results[key]['distance_SAME'][0]
    results[key]['palabra'] = results[key]['palabra'][0]
    results[key]['bot'] = results[key]['bot'][0]

os.chdir(cwd)

for key in results.keys():
    files = []
    for fichero in filelist:
        if fichero.split('-')[1] == results[key]['palabra']:
            files.append(fichero)

    conflictList = []
    node = 0

    for fichero in files:
        data = pd.read_csv(fichero)

        if fichero.endswith('-missing_AYU.csv'):
            for i in range(max(data.count())):
                conflictList.append(dict({"dataset":results[key]['bot'],"type":fichero.split('-')[2].split('_')[0],"conflicts":[[{"latitude": round(data.loc[i]['lat_OSM'],7), "source": "OSM"},{"latitude": None, "source": "MAD"}],[{"longitude": round(data.loc[i]['lon_OSM'],7),"source": "OSM"},{"longitude": None,"source": "MAD"}]],"node":node+i,"position":{"latitude":round(data.loc[i]['lat_OSM'],7),"longitude":round(data.loc[i]['lon_OSM'],7)}}))
            node = node + i
        if fichero.endswith('-edit.csv'):
            for i in range(max(data.count())):
                conflictList.append(dict({"dataset":results[key]['bot'],"type":fichero.split('-')[2].split('.')[0],"conflicts":[[{"latitude": round(data.loc[i]['lat_OSM'],7), "source": "OSM"},{"latitude": round(data.loc[i]['LATITUD'],7), "source": "MAD"}],[{"longitude": round(data.loc[i]['lon_OSM'],7),"source": "OSM"},{"longitude": round(data.loc[i]['LONGITUD'],7),"source": "MAD"}]],"node":i+node,"position":{"latitude":round(data.loc[i]['LATITUD'],7),"longitude":round(data.loc[i]['LONGITUD'],7)}}))
            node = node + i

    os.chdir(jwd)
    with open(results[key]['bot']+'.json','w') as myfile:
        json.dump(conflictList, myfile, indent=4)
        myfile.close()
        os.chdir(cwd)
