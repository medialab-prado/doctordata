"""
    This is the main function.
"""
print('Importing libraries...')
import json
import os
import pandas as pd
from difflib import SequenceMatcher
import jellyfish
from geopy.geocoders import Nominatim
geolocator = Nominatim()
from geopy.distance import great_circle
import folium
from folium.plugins import MarkerCluster
from convertbng.util import convert_bng, convert_lonlat, convert_etrs89_to_lonlat
import overpass
import sys

first_arg = sys.argv[1]
#Center coordinates
SF_COORDINATES = (40.4168, -3.7038)

# for speed purposes
MAX_RECORDS = 10

#pwd = '/Volumes/MacintoshHD/_GitHub/doctordata'
pwd = os.getcwd()
cwd = pwd + '/api/csv/'
jwd = pwd + '/api/json/'
bwd = pwd + '/bot/'
dwd = pwd + '/api/data/'

# Functions to work
print('Defining functions...')
def get_id(x):
    try:
        for i in range(len(ids)):
            point = [lat[i],lon[i]]
            if getDistance_meters(x,point) <results[fichero]['distance_SAME']:
                ayu[i] = x
                return ids[i]
        return 'No match'
    except:
        return 'No match'

def get_close(x):
    try:
        for i in range(len(ids)):
            point = [lat[i],lon[i]]
            if getDistance_meters(x,point) <results[fichero]['distance_CLOSE']:
                ayu[i] = x
                return ids[i]
        return 'No match'
    except:
        return 'No match'

def get_lat(x):
    try:
        ind = ids.index(x)
        return lat[ind]
    except:
        return None

def get_lon(x):
    try:
        ind = ids.index(x)
        return lon[ind]
    except:
        return None

def get_name(x):
    try:
        ind = ids.index(x)
        return name[ind]
    except:
        return None

def get_score(x):
    return getDistance_meters([x.lat_OSM, x.lon_OSM],[x.LATITUD, x.LONGITUD])

def getDistance_meters(x,y):
    try:
        return great_circle(x, y).kilometers*1000.0
    except:
        return 0

print('Opening files and ensuring naming convention...')
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

#AYU_fichero = '20171110-InventarioFuentes.csv'
#first_arg = 'street_lamp'
try:
    if (first_arg != '-f'):
        AYU_fichero = first_arg

    if (first_arg == 'street_lamp'):
        palabra = 'street_lamp'
        fichero = []

        for key in results.keys():
            if palabra == results[key]['palabra']:
                fichero = key

        search = 'area["name"="Madrid"];node(area)['+results[fichero]['SEARCH']+'];'
        api = overpass.API()
        OSM = api.Get(search)

        ids = [OSM['features'][i]['id'] for i in range(len(OSM['features']))]
        lat = [OSM['features'][i]['geometry']['coordinates'][1] for i in range(len(OSM['features']))]
        lon = [OSM['features'][i]['geometry']['coordinates'][0] for i in range(len(OSM['features']))]
        ayu = ids[:]
        print('Creating {} dataframe'.format(palabra))
        print('Found {} entities in OSM.'.format(str(len(ids))))

        AYU_MISSING = []
        for i in range(len(ids)):
            AYU_MISSING.append((ids[i],lat[i],lon[i]))
        AYU_MISSING = pd.DataFrame(AYU_MISSING)

        AYU_MISSING.columns = ['id_OSM','lat_OSM','lon_OSM']

        AYU_MISSING = AYU_MISSING.set_index('id_OSM')
        AYU_MISSING['coord'] = list(zip(AYU_MISSING.lat_OSM.values, AYU_MISSING.lon_OSM.values))
        os.chdir(cwd)
        print('Saving to csv')
        AYU_MISSING.to_csv('20171122-'+palabra+'-missing_AYU.csv')

    else:
        fichero = []
        for key in results.keys():
            if AYU_fichero.split('-')[1][:-4] == results[key]['palabra']:
                fichero = key
        search = 'area["name"="Madrid"];node(area)['+results[fichero]['SEARCH']+'];'

        api = overpass.API()
        OSM = api.Get(search)

        #OSM['features'][0]


        # Create searching arrays

        ids = [OSM['features'][i]['id'] for i in range(len(OSM['features']))]
        lat = [OSM['features'][i]['geometry']['coordinates'][1] for i in range(len(OSM['features']))]
        lon = [OSM['features'][i]['geometry']['coordinates'][0] for i in range(len(OSM['features']))]
        #name = [OSM['features'][i]['properties']['name'] for i in range(len(OSM['features']))]
        ayu = ids[:]

        print('Creating {} dataframe'.format(first_arg))
        print('Found {} entities in OSM.'.format(str(len(ids))))

        # Add ayuntamiento data
        #results[fichero]['DOCTORDATA'][1:]
        try:
            AYU = pd.read_csv(AYU_fichero, encoding='latin-1', delimiter=';',index_col=0, decimal='.')
            AYU.columns = [x.upper() for x in AYU.columns.values]
            print('Total MAD entities found: ', str(AYU.count().max()))
            if AYU_fichero == '20171110-InventarioFuentes.csv':
                AYU.columns = results[fichero]['DOCTORDATA'][1:]

        except:
            AYU = pd.DataFrame()


        try:
            AYU = AYU[AYU.LATITUD != 'Error']
            AYU = AYU[AYU.LONGITUD != 'Error']
        except:
            print('No errors!')

        AYU = AYU.sort_values('LATITUD')
        AYU['id_OSM'] = pd.Series()
        AYU['lat_OSM'] = pd.Series()
        AYU['lon_OSM'] = pd.Series()
        AYU['coord_OSM'] = pd.Series()
        AYU['name_OSM'] = pd.Series()
        AYU['score_OSM'] = pd.Series()
        #AYU['X_ETRS89'] = AYU['X_ETRS89'].apply(lambda x: float(x.replace(',','.')))
        #AYU['Y_ETRS89'] = AYU['Y_ETRS89'].apply(lambda x: float(x.replace(',','.')))
        #AYU = AYU[:200]
        AYU['LATITUD'] = AYU['LATITUD'].apply(lambda x: round(float(x),7))
        AYU['LONGITUD'] = AYU['LONGITUD'].apply(lambda x: round(float(x),7))
        AYU['coord'] = list(zip(AYU.LATITUD, AYU.LONGITUD))

        print('Get id matching....')
        AYU.id_OSM = AYU.coord.apply(lambda x: get_id(x))
        AYU_NO = AYU[AYU.id_OSM == 'No match']
        AYU_OK = AYU[AYU.id_OSM != 'No match']
        AYU_CLOSE = AYU_NO.copy()

        print('Get close entities...')
        AYU_CLOSE.id_OSM = AYU_NO.coord.apply(lambda x: get_close(x))
        AYU_NO = AYU_CLOSE[AYU_CLOSE.id_OSM == 'No match']
        AYU_CLOSE = AYU_CLOSE[AYU_CLOSE.id_OSM != 'No match']

        AYU = pd.concat([AYU_OK, AYU_CLOSE, AYU_NO])

        print('Geolocating from OSM...')
        AYU.lat_OSM = AYU.id_OSM.apply(lambda x: get_lat(x))
        AYU.lon_OSM = AYU.id_OSM.apply(lambda x: get_lon(x))
        AYU.score_OSM = AYU.apply(lambda x: round(get_score(x),3), axis=1)
        AYU['lat_OSM'] = AYU['lat_OSM'].apply(lambda x: round(float(x),7))
        AYU['lon_OSM'] = AYU['lon_OSM'].apply(lambda x: round(float(x),7))
        AYU['coord_OSM'] = list(zip(AYU.lat_OSM, AYU.lon_OSM))

        try:
            print('Creating close DataFrame')
            AYU_CLOSE.lat_OSM = AYU_CLOSE.id_OSM.apply(lambda x: get_lat(x))
            AYU_CLOSE.lon_OSM = AYU_CLOSE.id_OSM.apply(lambda x: get_lon(x))
            AYU_CLOSE.score_OSM = AYU_CLOSE.apply(lambda x: round(get_score(x),3), axis=1)
            AYU_CLOSE['coord_OSM'] = list(zip(AYU_CLOSE.lat_OSM, AYU_CLOSE.lon_OSM))
        except:
            print('No close')

        print('Create missing OSM DataFrame')
        AYU_NO.lat_OSM = AYU_NO.id_OSM.apply(lambda x: get_lat(x))
        AYU_NO.lon_OSM = AYU_NO.id_OSM.apply(lambda x: get_lon(x))
        AYU_NO.score_OSM = AYU_NO.apply(lambda x: round(get_score(x),3)06, axis=1)
        AYU_NO['coord_OSM'] = list(zip(AYU_NO.lat_OSM, AYU_NO.lon_OSM))

        AYU = AYU.sort_values('score_OSM')
        #AYU.name_OSM = AYU.id_OSM.apply(lambda x: get_name(x))

        print('Creating missing AYU Dataframe...')
        AYU_MISSING = []
        for i in range(len(ids)):
            AYU_MISSING.append((ids[i],lat[i],lon[i]))

        AYU_MISSING = pd.DataFrame(AYU_MISSING)
        AYU_MISSING.columns = ['id_OSM','lat_OSM','lon_OSM']

        AYU_MISSING = AYU_MISSING.set_index('id_OSM')
        AYU_MISSING['coord_OSM'] = list(zip(AYU_MISSING.lat_OSM.values, AYU_MISSING.lon_OSM.values))

        os.chdir(cwd)
        print('Saving to files...')
        AYU_CLOSE.to_csv(AYU_fichero[:-4]+'-edit.csv')
        AYU_NO.to_csv(AYU_fichero[:-4]+'-missing_OSM.csv')
        AYU_MISSING.to_csv(AYU_fichero[:-4]+'-missing_AYU.csv')
except:
    print(Exception)
