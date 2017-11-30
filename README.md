# DoctorData: datos abiertos colaborativos usando OpenStreetMap

Uno de los principales problemas a los que se enfrenta un portal de datos abiertos es la cobertura y calidad de los datos que se encuentran en él. Éstos son generados por las propias administraciones públicas con gran esfuerzo y buscando entre la información que han ido almacenado a lo largo de los años en distintos formatos.

Ante estos hechos, nos surge una pregunta: ¿pueden los ciudadanos ayudar a las administraciones en la tarea de recolección de datos?

[OpenStreetMap](http://openstreetmap.org) (OSM) es un mapa colaborativo construido por ciudadanos de todo el mundo y cuyos datos son de uso libre y bajo licencia abierta.

DoctorData pretende mejorar la cantidad y calidad de los datos complementando los conjuntos de datos presentes en el portal con la información disponible disponible en la plataforma OSM. De esta forma se involucrará a la ciudadanía de forma *indirecta* en esta tarea.

Además, como recompensa a la labor de la gente, se pretende integrar algunos datasets del portal de datos abiertos en OSM.

__Promotor__

* Esteban González Guardia

__Colaborador__

* Raimundo Abril López

# DoctorData
Bueno, aquí os presentamos a nuestro Bot DoctorData. Hablad con él en Telegram!!

`@datamad_bot`

## ¿Qué es DoctorData?
DoctorData es un bot unido a una web propia que permite a los ciudadanos interactuar con sus datos públicos y mejorarlos.

## ¿Por qué DoctorData?
Porque creemos que es un acuerdo que beneficia a ambas partes, por un lado el Ayuntamiento obtiene información de gran calidad de forma muy sencilla y porque facilita a los ciudadanos interactuar con sus elementos urbanos.

## ¿Qué hemos hecho?
Hemos comparado datasets del Ayuntamiento con los disponibles en OpenStreetMap a través de su API.
Ahí hemos identificado elementos que o bien no están en la web del Ayuntamiento o bien presentan grandes desviaciones en su posición GPS.


## ¿Cómo funciona DoctorData?
Sólo lanza el script y contacta al bot por Telegram:

`python3 bot/doctordata_bot.py`

Este bot, usa los datos analizados previamente para proponer retos a los ciudadanos, a través de:

* Reto del día, es un reto predefinido y que busca responder rápido a alguna cuestión en particular.
* Localización, buscará retos cercanos al usuario.
* Al azar, busca de forma aleatoria retos por la ciudad.

La estructura de la carpeta es sencilla, por un lado tenemos nuestro script del bot y un `install_missing.sh`. Cuando comience a trabajar, creará ficheros json con información sobre la sesión, con todos los contactos, retos que ha lanzado y respuestas de la gente que ha participado con nosotros. También generará archivos temporarles csv con retos personalizados por usuario según la última ubicación.

Los datasets que usamos son principalmente mobiliario urbano:

* Fuentes de agua potable
* Bancos
* Papeleras
* Farolas, hemos elegido este dataset porque es un ejemplo de dataset no disponible a través de la web del Ayuntamiento.

## ¿Por qué una web?

Porque es una plataforma excelente para visualizar los conflictos encontrados de una forma rápida, encontrar zonas conflictivas o zonas donde los ciudadanos colaboran de forma más activa.

En este caso podéis acceder a través de:

[Web de DoctorData](https://medialab-prado.github.io/doctordata)

## API

En esta sección se encuentran los datos preparados en Json para ser servidos. Al igual que los usa nuestro Bot.

Los datos se descargan desde la web del Ayuntamiento y se registran en data con su fecha como podréis ver dentro de las carpetas. Se asegura que en `indice.csv` están contenidos todos los nombres de las columnas de forma correcta y se lanza el script `doctordata.py`. Por ejemplo:

`python3 api/data/doctordata.py 20171110-InventarioFuentes.csv`

Este fichero `indice.csv` es muy importante porque ayuda al script a reconocer qué se va a encontrar según el tipo de archivo. Esto permite una integración muy rápida de cualquier dataset nuevo que llegue!!

Esto nos creará archivos csv con las diferencias entre el fichero de fuentes el Ayuntamiento y la base de datos de OpenStreetMap. Este proceso está automatizado a través de la API de OpenStreetMap. A continuación ejecutamos:

`python3 api/translate_csv_to_json.py`

Para obtener así los ficheros `.json` que necesita el bot y la web.
