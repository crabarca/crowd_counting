# Crowd counting con Wifi Probe Request

## Introducción
El uso y organización de espacios dentro de edificos, centros comerciales, estaciones y otros lugares de alta concurrencia siempre ha representado desafio para la gente que frecuenta y trabaja en estos lugares. 

En el contexto de la escuela, las salas de estudio representan un lugar importante dentro de la vida estudiantil dentro de la universidad. Si bien, la capacidad de las salas esta determinada al momento de su construcción, la disponibilidad de espacios disponibles durante el día varia considerablemente dependiendo de la hora. Es de conocimiento público que las salas se encuentran con alta disponibilidad en los primeros bloques de la mañana (bloque 1,2) para luego ir disminuyendo su disponibilidad durante las bloques 3-6 para luego aumentar su disponibilidad despúes del bloque 7.

La mayoria de los estudiantes ingresa a estas salas junto a su computador y celular para poder realizar su estudio. Por consiguiente, la red de WiFi de la sala se encuentra más saturada durante los periodos de alta demanda y viceversa.

Los dispositivos WiFi están constantemente haciendo *broadcast* de ciertos paquetes de administración de red (*management frames*) por lo que una antena de bajo costo que se encuentre pasivamente recolectando toda esta información puede ser utilizada para recolectar información de los usuarios que se encuentran en un área cercana. Si bien, este método no es nuevo, ha demostrado ser efectivo en determinar el seguimiento de personas, flujo por determinados lugares y estimación de densidad de personas en lugares determinados. 

El objetivo de este trabajo es determinar el nivel de uso de las salas de estudio y poder disponer de esta información en tiempo real y público para que los estudiantes puedan evitar o no ir a salas demasiado congestionadas o vacias (cada uno con sus preferencias).


## Extracción de información
Dentro de todo el trafico que se puede reconocer al usar el protocolo IEEE 802.11, los unicos fragmentos de información que nos interesan son los paquetes de Probe Request/Reponse. Estos paquetes son enviados constantemente por los dispositivos WiFi para anunciar su presencia dentro del entorno y poder asociarse a una red cercana.

Para la detección de estos paquetes no es necesario estar conectado a una determinada red, sino que se pueden recolectar pasivamente mediante el uso de una antena WiFi configurada en modo monitor.

La configuración para poder activar el modo monitor de la interfaz de red a usar se realizó mediante la herramienta [Airmon-ng](https://www.aircrack-ng.org/doku.php?id=airmon-ng) que es parte del conjunto de utilidades que provee [Aircrack-ng](https://www.aircrack-ng.org/).

- **Nota:** No todos las interfaces son compatibles con el modo monitor, para poder saber si la interfaz es compatible revisar el siguiente tutorial [Tutorial: Is My Wireless Card Compatible?](https://www.aircrack-ng.org/doku.php?id=compatible_cards) o la [wikidevi](https://wikidevi.com/wiki/Main_Page)

Una vez que la interfaz ha sido configurada en modo monitor se puede proceder a realizar la captura y filtrado de paquetes. 

Los paquetes son recolectados mediante la libreria [Scapy](https://scapy.net/) para `Python`. La decisión de utilizar esta libreria sobre otras herramientas se fundamenta en la simplicidad que se logra para poder acceder a todo el entorno de Python tanto para hacer manipulación y almacenamiento de datos. Por otro lado, la librería esta diseñada con la extensibilidad en mente. 

Otras herramientas disponibles para captura y filtro de paquetes (más populares):
- [Tcpdump](https://www.tcpdump.org/)
- [Wireshark](https://www.wireshark.org/)
- [Kismet](https://www.kismetwireless.net/)
- [Otras](https://www.google.com/search?client=ubuntu&channel=fs&q=packet+capturing+tools&ie=utf-8&oe=utf-8)

Los paquetes utiles para este problema son aquellos que presentan la capa *Dot11ProbeReq* (nombre utilizado por Scapy).

## Almacenamiento de la información
Una vez que los paquetes son capturados es de especial interes guardar la siguiente información:
- **Tiempo de captura:** Hora/fecha de la captura del paquete
- **Mac address:** Dirección MAC del dispositivo
- **Vendor:** Manufacturero de la interfaz de red
- **SSID:** Nombre de la red
- **RSSI:** Potencia de la señal del dispositivo 

Los únicos campos que siempre estarán presentes son **Tiempo de captura** y **Mac address*, el resto de los campos son opcionales y son utilizados para obtener estadísticas adicionales a las relacionadas con la densidad de personas. 

Cada vez que se detecta un nuevo paquete, la información de este es guardado instantaneamente en la base de datos. Actualmente la KEY de corresponde a la fecha/hora de captura, ya que es altamente improbable sino imposible (revisar) que dos paquetes se capturen exactamente al mismo tiempo.

Actualmente la información es almacenada en una base de datos [SQLite](https://www.sqlite.org/index.html), se decidio utilizar esta BD simplemente por comodidad dado que [Python](https://docs.python.org/3.5/library/sqlite3.html) la incluye dentro de su paquete estándar de librerias.


## Transformación de los datos
Explicar que operaciones de ETL se realizaron a los datos para poder pasar al proceso de análisis. 


## Análisis de los datos 
Análisis estadistico de los datos
- Contar cantidad de macs distintas en los ultimos X minutos ( sql query )
- Cantidad de registros promedio por minuto
- Porcentaje de dispositivos con vendor conocido vs desconocido. Investigar por las causas: 1.mac randomization, 2. la libreria no esta actualizada con los ultimos vendors

## Presentación de los datos
Explicar los gráficos y escalas utilizadas para poder determinar la utilización de las salas 

## Trabajo futuro
Implementar una estación de monitoreo permanente que detecte los paquetes de Probe Request mediante el procedimiento antes mencionado. Mediante la utilización de un *IoT Gateway* (important buzzword) es posible recolectar esta información y almacenarla en algún servidor predeterminado para luego ser consultado por un cliente web que disponga la información y las métricas con respecto al uso de espacios donde se ubican los dispositivos de medición. 