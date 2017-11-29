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

## api
En esta sección se pueden encontrar los ficheros de procesamiento y almacenamiento de datos. Los datos se descargan desde la web del Ayuntamiento y se registran en data con su fecha como están aquí. Se asegura que en `indice.csv` contiene los nombres de las columnas de forma correcta y se lanza el script `doctordata.py`. Por ejemplo:

----
python doctordata.py 20171110-InventarioFuentes.csv
----

Esto nos creará archivos csv con las diferencias entre el fichero de fuentes el Ayuntamiento y la base de datos de OpenStreetMap. Este proceso está automatizado a través de la API de OpenStreetMap. A continuación ejecutamos

----
translate_csv_to_json.py
----

Para obtener así los ficheros `.json` que necesita el bot y la web.

## bot
