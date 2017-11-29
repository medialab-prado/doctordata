import json
import os
import yaml
import pandas as pd
import random
from geopy.distance import great_circle

pwd = '/Volumes/MacintoshHD/_GitHub/doctordata'
bwd = '/Volumes/MacintoshHD/_GitHub/doctordata/bot/'
cwd = '/Volumes/MacintoshHD/_GitHub/doctordata/api/csv'
dwd = '/Volumes/MacintoshHD/_GitHub/doctordata/api/data'
os.chdir(bwd)
chat = 432214082
datos = pd.read_csv(str(chat)+'.csv')
datos.count()['id_OSM']
random.randint(0,100)
test = datos.loc[random.randint(0, datos.count()['id_OSM']-1)]
location = {'latitude':test['latitude'],'longitude':test['longitude']}
location

with open('retos.json','r') as myfile:
    datos = myfile.readlines()

updates = []

for i in range(len(datos)):
    updates.append(yaml.load(datos[i]))

len(updates)
i = 1
boolLoop = True
while boolLoop:
    if updates[-i]['chat'] == chat:
        boolLoop = False
    i = i+1

updates[-i+1]

updates[-2]['message']['chat']['id'] != chat
updates[-1]

cwd = pwd + '/api/csv/'
bwd = pwd + '/bot/'
#bwd = '/Volumes/MacintoshHD/_GitHub/doctordata/bot/'
os.chdir(dwd)
os.listdir()
indice = pd.read_csv('indice.csv',delimiter=';',index_col=0)
indice.columns
os.chdir(cwd)
os.listdir()
filelist = [ f for f in os.listdir(cwd) if f.endswith("-missing_AYU.csv") ]
filelist[0].split('-')[1]
datalist = []
indice[indice['palabra']==filelist[0].split('-')[1]]['bot'].values[0]
for fichero in filelist:
    print(fichero)
    data = pd.read_csv(fichero)
    data['bot'] = indice[indice['palabra']==fichero.split('-')[1]]['bot'].values[0]
    datalist.append(data)
data = pd.concat(datalist)
data.columns = ['id_OSM','latitude','longitude','coordinates','bot']
data
testList = data.to_dict(orient='records')

get_close_test(location,data,chat)

def get_close_test(location,data, chat_id,random_opt = False):
    datas = data.copy()
    datas['close'] = datas['coordinates'].apply(lambda x: getDistance_meters(x, (location['latitude'],location['longitude'])))
    datas = datas.sort_values('close')
    if random_opt:
        location['latitude'] = data.loc[random.choice(range(10))]['latitude']
        location['longitude'] = data.loc[random.choice(range(10))]['longitude']

    location['latitude'] = data.head(1)['latitude'].values[0]
    location['longitude'] = data.head(1)['longitude'].values[0]
    datas.set_index('id_OSM',inplace=True)
    datas.head(100).to_csv(str(chat_id)+'.csv')
    return location
location

def getDistance_meters(x,y):
    try:
        return great_circle(x, y).kilometers*1000.0
    except:
        return 0
get_close_test(location,data,chat)

getDistance_meters([40.34,-3.76],[40.3443,-3.76786])

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
