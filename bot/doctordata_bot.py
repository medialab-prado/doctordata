import json
import requests
import time
import urllib
import os
import pandas as pd
import random
from geopy.distance import great_circle
import yaml

SESSION_ID = random.randint(0,1000000)
TOKEN = "ADD BOT TOKEN"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
DDURL = "https://medialab-prado.github.io/doctordata/telegram-map.html"

pwd = os.getcwd()
#pwd = '/Volumes/MacintoshHD/_GitHub/doctordata'
cwd = pwd + '/api/csv/'
jwd = pwd + '/api/json/'
bwd = pwd + '/bot/'
dwd = pwd + '/api/data/'

#bwd = '/Volumes/MacintoshHD/_GitHub/doctordata/bot/'
os.chdir(dwd)
indice = pd.read_csv('indice.csv',delimiter=';',index_col=0)
os.chdir(jwd)
filelist = [ f for f in os.listdir(jwd) if f.endswith(".json") and f!='indice.json']
datos = []

for fichero in filelist:
    with open(fichero,'r') as myfile:
        datos = datos + json.load(myfile)

tipo = []
dataset = []
node = []
latitude = []
longitude = []

for test in datos:
    dataset.append(test['dataset'])
    tipo.append(test['type'])
    node.append(test['node'])
    latitude.append(test['position']['latitude'])
    longitude.append(test['position']['longitude'])

print(set(dataset))

data = pd.DataFrame([tipo,dataset,node,latitude,longitude,list(zip(latitude,longitude))])
data = data.transpose()
data.columns=['type','dataset','node','latitude','longitude','coordinates']
data['latitude'] = data['latitude'].apply(lambda x: round(x,6))
data['longitude'] = data['longitude'].apply(lambda x: round(x,6))
data['coordinates'] = list(zip(data.latitude,data.longitude))
testList = datos

location = {}
os.chdir(bwd)
open('retos_{}.json'.format(SESSION_ID),'w')
open('scores_{}.json'.format(SESSION_ID),'w')
open('updates_{}.json'.format(SESSION_ID),'w')

print('Ready!')

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
            send_location([40.35,-3.78],chat)
        except Exception as e:
            print(e)

def send_location(test, chat_id, date):
    url = URL + "sendlocation?chat_id={}&latitude={}&longitude={}".format(chat_id, test['latitude'],test['longitude'])
    get_url(url)

    with open('retos_{}.json'.format(SESSION_ID),'a') as myfile:
        test['date'] = date
        test['chat_id'] = chat_id
        #Aquí hay un error
        stringJson = json.dumps(test)
        myfile.write(stringJson+'\n')
    myfile.close()

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def send_reto(test, chat_id):
    send_message(DDURL+'?dataset={}s&latitude={}&longitude={}&zoom=20&node={}'.format(test['dataset'],test['latitude'],test['longitude'],test['node']),chat_id)

def format_message(test):
    articulo_dict = {'fuente':'la','banco':'el','papelera':'la','farola':'la','monumento':'el'}
    final_dict ={'fuente':'a','banco':'','papelera':'a','farola':'a','monumento':''}
    indef_dict ={'fuente':'a','banco':'o','papelera':'a','farola':'a','monumento':'o'}

    if test['type'] == 'missing':
        text = 'Buscamos confirmar que hay un{} {} en esta ubicación. ¿Está ahí?'.format(final_dict[test['dataset']],test['dataset'])
    if test['type'] == 'edit':
        text = 'Parece que hay un conflicto, buscamos un{} {} en esta ubicación y saber si está desplazad{} de su posición. ¿Cuál es su posición correcta?'.format(final_dict[test['dataset']],test['dataset'],indef_dict[test['dataset']])

    return text


def set_score(chat, text, date):
    with open('retos_{}.json'.format(SESSION_ID),'r') as myfile:
        datos = myfile.readlines()

    i = 1
    boolLoop = True
    while boolLoop:
        reto = yaml.load(datos[-i])
        if yaml.load(datos[-i])['chat_id'] == chat:
            boolLoop = False
        i = i+1

    with open('scores_{}.json'.format(SESSION_ID),'a') as myfile:
        score = {'date':date, 'chat':chat, 'text':text, 'test':reto}
        stringJson = json.dumps(score)
        myfile.write(stringJson+'\n')
    myfile.close()

def keyboard_missing(test):
    keyboard_missing = ['Sí, existe','Sí, pero no funciona','No, no existe','Otro al azar','Otro cercano','Salir']
    if test['type'] == 'missing':
        keyboard_missing = ['Sí, existe','Sí, pero no funciona','No, no existe','Otro al azar','Otro cercano','Salir']
    if test['type'] == 'edit':
        keyboard_missing = ['El correcto es el naranja','El correcto es el azul','Ninguno de los dos','Otro al azar','Otro cercano','Salir']
    return keyboard_missing

keyboard_wait = ['Comenzamos!','Reto del día','Más info','Salir']
keyboard_menu = ['Comenzamos!','Salir']
keyboard_go = ['Reto del día','Uno cercano a mi última ubicación','Uno al azar','Salir']
keyboard_answer = ['Otro cercano','Otro al azar','Salir']

def handle_updates(updates):
    for update in updates["result"]:
        with open('updates_{}.json'.format(SESSION_ID),'a') as myfile:
            stringJson = json.dumps(update)
            myfile.write(stringJson+'\n')
        myfile.close()
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            date = update["message"]["date"]
            first_name = update["message"]["from"]["first_name"]

            if text == "/start":
                keyboard = build_keyboard(keyboard_wait)
                send_message("Hola {}, soy DoctorData, tu bot colaborativo para mejorar entre todos los datos abiertos de la web del ayuntamiento de Madrid.".format(first_name), chat, keyboard)

            if text == "/doctordata":
                test = {'type':'missing', 'node':3232, 'dataset':'fuente', 'latitude': 40.32323, 'longitude': -3.7676}
                keyboard = build_keyboard(keyboard_missing(test))
                send_message(format_message(test),chat, keyboard)
                send_reto(test,chat)
                send_location(test, chat, date)

            if text == 'Hola' or text == 'hola':
                keyboard = build_keyboard(keyboard_wait)
                send_message('Hola, dime qué te apetece hoy.',chat, keyboard)
                send_message('Si haces click en Comenzamos! te enviaré retos aleatorios, si me envías tu ubicación mucho mejor, porque estarán cerca tuya..',chat, keyboard)
                send_message('Si por el contrario te apetece un buen reto, prueba el reto del día donde competirás con otros madrileños por ser el primero en responder.',chat, keyboard)


            if text != '':
                keyboard = build_keyboard(keyboard_wait)

            if text == 'Reto del día':
                test = {'type':'missing', 'node':3232, 'dataset':'fuente', 'latitude': 40.32323, 'longitude': -3.7676}
                keyboard = build_keyboard(keyboard_missing(test))
                send_message(format_message(test),chat, keyboard)
                send_reto(test,chat)
                send_location(test, chat, date)

            if text == 'Más info':
                keyboard = build_keyboard(keyboard_menu)
                send_message("Este bot forma parte de un proyecto presentado al concurso de Medialab Prado #Datamad2017.\nCon él pretendemos mejorar los datos disponibles en el portal de datos del Ayuntamiento y que todos colaboremos en mantenerlos al día.", chat, keyboard)
                send_message("Al responder a cada reto nos aportas información sobre elementos de tu ciudad, su estado de conservación, o simplemente si existen.", chat, keyboard)
                send_message("Con tu colaboración hacemos mejor la información pública de nuestra ciudad y ayudamos/exigimos a la administración a mejorar.", chat, keyboard)
                send_message("Ni que decir tiene que toda la información recopilada se trata de forma totalmente anónima y en cualquier momento puedes dirigirte a nosotros para borrarla o si quieres más info.", chat, keyboard)
                send_message("Rai y Esteban. Equipo de DoctorData", chat, keyboard)
                send_message("https://medialab-prado.github.io/doctordata/",chat, keyboard)

            if text == 'Exit' or text == 'Salir':
                keyboard = build_keyboard(keyboard_wait)
                send_message("Gracias por usar este servicio. Recuerda que estaré por aquí para cuando quieras jugar!", chat, keyboard)

            if text == 'Comenzamos!' or text == 'Comenzamos de nuevo!':
                #location_keyboard = keyboardbutton(text='Send location', request_location = True)
                #reply_keyboard = [[location_keyboard]]
                #custom_keyboard = [[location_keyboard]]

                keyboard = build_keyboard(keyboard_go)
                #keyboard = build_keyboard_location(['Enviar ubicación'])
                send_message("Necesito que me envíes tu ubicación. Así podré buscarte retos cercanos. Si no quieres compartir tu ubicación puedes elegir Uno al azar con los botones de abajo.", chat, keyboard)

            if text == 'Sí, existe' or text == 'Si' or text == 'Sí, pero no funciona' or text=='El correcto es el naranja' or text == 'El correcto es el azul' or text =='Ninguno de los dos':
                keyboard = build_keyboard(keyboard_answer)
                send_message("Genial! Muchas gracias por ayudar!", chat, keyboard)
                set_score(chat,text,date)


            if text == 'No, no existe' or text == 'No':
                keyboard = build_keyboard(keyboard_answer)
                send_message("Vale, estos son los errores que queremos corregir y gracias a tu ayuda lo haremos!", chat, keyboard)
                set_score(chat,text,date)

            if text == 'No sé!' or text == 'No lo sé' or text == 'No se' or text == 'Nose':
                keyboard = build_keyboard(keyboard_answer)
                send_message("Vaya... he metido la pata seguro...", chat, keyboard)
                set_score(chat,text,date)

            if text == 'Otro' or text =='Otro cercano' or text == 'Uno cercano a mi última ubicación':
                try:
                    with open('{}.csv'.format(chat),'r') as infile:
                        datos = infile.readlines()
                    infile.close()
                    numero = random.randint(0,len(datos))

                    test = yaml.load(datos[numero])
                    keyboard = build_keyboard(keyboard_missing(test))
                    send_message(format_message(test),chat, keyboard)
                    send_reto(test, chat)
                    send_location(test, chat, date)

                except:
                    keyboard = build_keyboard(keyboard_wait)
                    send_message("No tengo ninguna ubicación tuya aún.. ¿Te importa mandármela?",chat, keyboard)


            if text == 'Uno al azar' or text == 'Otro al azar':
                location_random = random.choice(testList)
                test = {'type':location_random['type'], 'node':location_random['node'], 'dataset':location_random['dataset'], 'latitude': location_random['position']['latitude'], 'longitude': location_random['position']['longitude']}
                keyboard = build_keyboard(keyboard_missing(test))
                send_message(format_message(test),chat, keyboard)
                send_reto(test, chat)
                send_location(test, chat, date)



        except Exception as e:
            print(e)
            try:
                location = update["message"]["location"]
                date = update["message"]["date"]
                chat = update["message"]["chat"]["id"]
                test = get_close_test(location, data, chat)
                keyboard = build_keyboard(keyboard_missing(test))
                send_message('Genial, un segundo que voy a buscarte un reto cercano.',chat, keyboard)
                send_message(format_message(test),chat, keyboard)
                send_reto(test, chat)
                send_location(test, chat, date)

            except Exception as e:
                print(e)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def build_keyboard_location(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True, "request_location":True}
    return json.dumps(reply_markup)

def get_close_test(location,data, chat_id):
    datas = data.copy()
    datas['close'] = datas['coordinates'].apply(lambda x: getDistance_meters(x, (location['latitude'],location['longitude'])))
    datas = datas.sort_values('close')
    datas = datas.reset_index(drop=True)
    tipo = datas['type'].head(1).values[0]
    dataset = datas['dataset'].head(1).values[0]
    latitud = datas['latitude'].head(1).values[0]
    longitud = datas['longitude'].head(1).values[0]
    nodo = datas['node'].head(1).values[0]

    test = {'type':tipo, 'node':nodo, 'dataset':dataset, 'latitude': latitud, 'longitude': longitud}
    with open('{}.csv'.format(chat_id),'w') as outfile:
        for i in range(25):
            tipo = datas['type'].loc[i]
            dataset = datas['dataset'].loc[i]
            latitud = datas['latitude'].loc[i]
            longitud = datas['longitude'].loc[i]
            nodo = datas['node'].loc[i]
            test_otro = {'type':tipo, 'node':nodo, 'dataset':dataset, 'latitude': latitud, 'longitude': longitud}
            stringJson = json.dumps(test_otro)
            outfile.writelines(stringJson+'\n')

    outfile.close()


    return test

def getDistance_meters(x,y):
    try:
        return great_circle(x, y).kilometers*1000.0
    except:
        return 0

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
