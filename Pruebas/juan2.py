# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
#Importamos la librería de tiempo
import time
#Librería de MQTT para publicar
import paho.mqtt.publish as publish
#Conectar a la base de datos
import mysql.connector
#Importa la librería para modificaciones de tiempo
from datetime import date
#Librería para usar los pines GPIO
import RPi.GPIO as GPIO
#Importamos la librería de ascii para el control z
from curses import ascii
#Importamos la librería que nos permite manejar varios hilos
#import threading
import subprocess
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, False)

#Id de cada punto
id_estacion = ("01", "02")
id_nivel = ("03", "04", "05", "06", "07")
id_acequia = ("08", "09", "10", "11", "12", "13", "14", "15", "16", "17")
id_humedad = ("18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28",
	"29", "30", "31", "32", "33", "34", "35", "36", "37")

#Sensores de la estación
#bat hum    temp   vel    dir    plub   luz
s_estacion = ("hum", "temp", "vel", "dire", "plub", "luz")

#Inicia la comunicación serial por el puerto ttyS0 a 38400
#Con ls -l /dev puedo saber cuál es el puerto serial 0 o 1
#Se usa esta velocidad porque no falla el módulo
print ("Iniciando la comunicación con el serial")
serie = serial.Serial("/dev/ttyS0", 38400)


def inicio():
	"""Acomoda el módulo para recibir mensajes"""
	#Se cierra el puerto por si había otra comunicación
	serie.close()
	print ("Cerrando el puerto serial")
	#Se abre el puerto serial
	serie.open()
	print ("Abriendo el puerto serial")
	#Escribe AT para comprobar que se está comunicando con el SIM800L
	serie.write("AT\r\n")
	time.sleep(1)
	print("Colocando el módulo en modo SMS")
	#Pone el módulo en modo SMS
	serie.write("AT+CMGF=1\r\n")
	time.sleep(1)
	print("Escribiendo 2,2")
	#Muestra el mensaje por el puerto serial
	serie.write("AT+CNMI=2,2,0,0,0\r\n")
	time.sleep(1)


def conex():
	"""Determina si el módulo GSM esta funcionando
		Manda AT, si el módulo no responde ok cierra el ciclo infinito
		Y abre el ciclo infinito para todos los procesos, de no ser así vuelve a
		empieza a mandar el ok y empieza a contar hasta 3, si llega a 3 sin tener
		una respuesta de Ok, entonces me manda un correo"""
	#Variable que controla el ciclo infinito
	mal = True
	#Variable que cuenta los errores
	cnt = 0
	#Mientras que el sistema mande error al escribir AT
	while mal:
		#Escribe AT en el puerto serial
		serie.write("AT\r\n")
		print ("Escribiendo AT esperando un OK")
		time.sleep(0.5)
		#Lee la respuesta del puerto serial
		read = serie.readline()
		print ("////////////////////////////" + read)
		read = serie.readline()
		print ("////////////////////////////" + read)
		#Si la respuesta es OK
		if "OK" in read:
			#Controla la variable del ciclo infinito y la pone en falso
			mal = False
			#Pone el contador de errores en 0
			cnt = 0
			return True
		#Si la respuesta no es OK (sino error)
		else:
			#Coloca la variable que controla el ciclo infinito en True
			mal = True
			#Cuenta un error
			cnt = cnt + 1
			print (cnt)
			GPIO.output(18, 1)
			time.sleep(1)
			GPIO.output(18, 0)
			time.sleep(1)
			#Si el contador es igual a 3
			if (cnt == 5):
				pass
				cnt = 0
				#Mandar gmal
			return False


def primerx():
	"""Lee la primera línea del puerto serial
		Si llegó un SMS (+CMT) lee la segunda línea"""
	#Lee la línea del puerto serial
	primera = serie.readline()
	#Si está el comando +CMT en la línea
	if "+CMT" in primera:
		print ("------------------Iniciando la lectura del mensaje: -----------------\n")
		print ("Primera linea: ")
		#Imprime la línea leida
		print (primera)
		#Debe llegar algo similar a lo de abajo
		#Primera = '+CMT: "3003859853","","18/01/18,16:43:01-20"'
		#Se separa el mensaje por ",esto con el fin de obtener el número del sms
		separado = primera.split('"')
		print ('Mensaje separado por ": ')
		print (separado)
		#Guarda en cada variable su valor, así como número y fecha
		cmt, numero, coma1, nada, coma, fecha, fdl = separado
		print ("--------------------Llamando a la función segundx--------------------\n")
		#Llama a la función segundx
		segundx(numero)


def segundx(numero):
	"""Lee la segunda línea del puerto serial dependiendo del mensaje hará cosas"""
	#Variable de control del ciclo infinito
	qap = True
	#Inicia un ciclo infinito para leer varias veces el puerto serial
	while qap:
		#Lee el puerto serial
		segunda = serie.readline()
		#segunda = "18 090 090 0000 24/01/2018 13:40:30\n"
		#segunda = "01 012 067.89 012.34 912.34 056.78 0123.45 1234.56 11/02/2018 19:00:19\n"
		#segunda = "fecha"
		print ("Segunda linea: ")
		#Imprime lo leido
		print (segunda)
		idy = segunda[0:2]
		if idy in id_estacion:
			print ("-------Es una estación meteorológica, llamando a la mejora-------\n")
			mejora_estacion(segunda)
		elif (idy in id_nivel) or (idy in id_acequia) or (idy in id_humedad):
			print ("----------------Es un nodo, llamando a la mejora-----------------\n")
			mejora(segunda)
		elif "\r\n" in segunda:
			if "fecha" in segunda:
				print ("------------------Me está pidiendo la fecha------------------\n")
				print ("Determinando la hora actual y agregándole 20 segundos")
				#Ejecuta la función hora_20
				#Encargada de dar la fecha y hora actual + 20 segundos
				ho, fe = hora_20()
				#Guarda el mensaje en el formato adecuado
				ms = "f:" + fe + " h:" + ho
				print (("El mensaje enviado es: " + ms))
				#Manda el mensaje de texto con la hora actual + 20 sg
				sendmensaje("+57" + numero, ms)
				#Cierra el ciclo infinito
				print ("---------------------Fin del ciclo Fecha---------------------\n")
				qap = False
			else:
				print ("------------------Fin del ciclo otra razón-------------------\n")
				qap = False
		h_con, h_sin, hay = internet()
		print ("Conexión a internet: " + str(hay))
		consulta_bdd(h_sin, h_con)


def internet():
	"""Realiza un ping a google"""
	global net
	global hora_con
	global hora_sin
	w = subprocess.Popen(["ping", "-c 1", "www.google.com"], stdout=subprocess.PIPE)
	w.wait()
	if w.poll():
		#print ("No hay internet")
		hay = False
		time.sleep(1)
		if net == "si":
			hora_sin = hora_now()
			print ("Hora sin internet: " + hora_sin)
		net = "no"
	else:
		#print ("Si hay internet")
		hay = True
		time.sleep(1)
		if net == "no":
			hora_con = hora_now()
			print ("Hora con internet: " + hora_con)
		net = "si"
	return hora_con, hora_sin, hay


def consulta_bdd(fecha_menor, fecha_mayor):
	"""Consulta la base de datos entre un intérvalo de fechas"""
	global hora_con
	try:
		if fecha_mayor > fecha_menor:
			print ("Mandando los datos entre " + fecha_mayor + "y " + fecha_menor)
			query = ("SELECT * FROM datos WHERE fecha BETWEEN %s AND %s;")
			datos = (fecha_menor, fecha_mayor)
			cursor.execute(query, datos)
			for (id, sensor, fecha, tipo, valor, bateria) in cursor:
				consulta = ("{} {} {} {} {} {}".format(id, sensor, fecha, tipo, valor, bateria))
				print (consulta)
				adecuacion(consulta)
			hora_con = "0000-00-00 00:00:00"
			publish.single("net", "Se fue el net pero ya regresó", hostname="127.0.0.1")
	except UnboundLocalError:
		print ("No hay nada en la base de datos")


def adecuacion(linea):
	"""Procesa la información que llega en la línea del mensaje"""
	#linea = "1 prueba 2018-02-03 15:50:34 Estacion 100 91"
	#Se separa por espacio la línea, ese es el protocolo
	separado = linea.split(' ')
	print ("Dividiendo el mensaje por espacios")
	print (separado)
	#Guarda en cada variable su valor asignado
	idx, sensor, fecha, hora, tipo, valor, bat = separado
	#Convierte a entero el id para poder compararlo
	print("Enviando mqtt...")
	#Arregla el topic dependiendo del id y el tipo de sensor
	topic = idx + "/" + tipo
	print ("Topic: " + topic)
	print ("Valor: " + valor)
	#Publica por MQTT el valor de del sensor en el topic indicado
	publish.single(topic, valor, hostname="127.0.0.1")


def mejora_estacion(linea):
	"""Procesa la información que llega en la línea del mensaje"""
	#linea = "xx xxx xxx.xx xxx.xx xxx.xx xxx.xx xxx.xx xxx.xx xx/xx/xxxx xx:xx:xx\n"
	#linea = "id bat hum    temp   vel    dir    plub   luz    d/m/a      h:m:s"
	#Se separa por espacio la línea, ese es el protocolo
	separado = linea.split(' ')
	print ("Dividiendo el mensaje por espacios")
	print (separado)
	#Guarda en cada variable su valor asignado
	idx, bat, hum, temp, vel, dire, plub, luz, fecha, hora = separado
	dic = {"hum": hum, "temp": temp, "vel": vel, "dire": dire, "plub": plub, "luz": luz}
	#Arregla la fecha al formato de MySQL
	f_h = fecha_ok(fecha, hora)
	print (("La fecha para MySQL es: " + f_h))
	for abc in s_estacion:
		print (("Enviando por MQTT: " + abc))
		topic = (idx + "/" + abc)
		print (("Topic: " + topic))
		print (("Valor: " + dic[abc]))
		#Publica por MQTT el valor de del sensor en el topic indicado
		publish.single(topic, dic[abc], hostname="127.0.0.1")
		#Guarda en la base de datos el id, cuál es, fecha, el tipo de sensor y valor
		print ("Guardando en base de datos")
		bdd(idx, 'prueba', f_h, abc, dic[abc], bat)
	print ("---------------------------Fin de la estación----------------------------\n")


def hora_20():
	"""Función para entregar la hora al nodo con 20 sg de más"""
	#Obtiene la hora actual
	hh = time.strftime("%H:%M:%S")
	print ("La hora actual es: " + hh)
	#Separa la hora por :
	horx = hh.split(':')
	hora, minuto, segundo = horx
	#Convierte a entero la hora, minuto y segundo
	hora = int(hora)
	minuto = int(minuto)
	segundo = int(segundo)
	#Le agrega 20 segundos a los segundos
	nw_sg = segundo + 20
	#Si hay más de 60 segundos corrige toda la hora
	if nw_sg >= 60:
		nw_sg = nw_sg - 60
		minuto = minuto + 1
		if minuto >= 60:
			minuto = minuto - 60
			hora = hora + 1
	#Convierte a string la hora, minuto y segundo
	segundo = str(nw_sg)
	minuto = str(minuto)
	hora = str(hora)
	#Guarda en hh la hora de nuevo
	hh = hora + ":" + minuto + ":" + segundo
	#Obtiene la fecha actual
	yy = time.strftime("%d/%m/%Y")
	print ("La fecha actual es: " + yy)
	print (("La hora actual sumándole 20 segundos es: " + hh))
	return hh, yy


def sendmensaje(receptor, mns=""):
	"""Función para enviar el mensaje"""
	serie.write('AT\r\n')
	time.sleep(1)
	#Le ponemos en modo para SMS
	serie.write('AT+CMGF=1\r\n')
	time.sleep(1)
	#Comando para enviar el mensaje, se pasa el valor del número
	serie.write('AT+CMGS=\"' + receptor + '\"\r\n')
	time.sleep(1)
	#Se escribe el mensaje
	serie.write(mns)
	time.sleep(3)
	#Termina el menzaje con Ctrl+z
	serie.write(ascii.ctrl("z"))
	time.sleep(3)
	#Le pasamos un fin de linea
	serie.write('\r\n')
	print ("Mensaje enviado\n")


def mejora(linea):
	"""Procesa la información que llega en la línea del mensaje"""
	#linea = "18 090 090 0000 24/01/2018 13:40:30\n"
	#Se separa por espacio la línea, ese es el protocolo
	separado = linea.split(' ')
	print ("Dividiendo el mensaje por espacios")
	print (separado)
	#Guarda en cada variable su valor asignado
	idx, bat, hum, nivel, fecha, hora = separado
	#Arregla la fecha al formato de MySQL
	f_h = fecha_ok(fecha, hora)
	print ("La fecha para MySQL es: " + f_h)
	#Convierte a entero el id para poder compararlo
	#Guarda el valor y el tipo de sensor dependiendo del id si es humedad o nivel
	tipo_sensor, valor = valor_s(idx, hum, nivel)
	print("Enviando mqtt...")
	#Arregla el topic dependiendo del id y el tipo de sensor
	topic = idx + "/" + tipo_sensor
	print ("Topic: " + topic)
	print ("Valor: " + valor)
	#Publica por MQTT el valor de del sensor en el topic indicado
	publish.single(topic, valor, hostname="127.0.0.1")
	#Guarda en la base de datos el id, cuál es, fecha, el tipo de sensor y valor
	print ("Guardando en base de datos")
	bdd(idx, 'prueba', f_h, tipo_sensor, valor, bat)
	print ("---------------------------Fin del nodo----------------------------------\n")


def fecha_ok(fecha, hora):
	"""Acomoda la fecha y hora para ser guardada en MySQL"""
	#Separa los valores de la fecha por /
	fecha = fecha.split('/')
	#Guarda en una variable el día, mes y año
	dia, mes, anio = fecha
	#Convierte a entero la variable que es un string
	dia = int(dia)
	mes = int(mes)
	anio = int(anio)
	#Con date convierte el día, mes y año al formato de MySQL
	fecha = date(anio, mes, dia)
	#Une la fecha y hora para ser guardada en MySQL
	f_h = str(fecha) + " " + hora
	return f_h


def valor_s(idx, hum, nivel):
	"""Devuelve el tipo de sensor y el valor a guarda de cada punto según la id"""
	#Si el id está dentro del grupo de sensores de humedad
	if idx in id_humedad:
		print ("Es un sensor de humedad")
		#Guarda como tipo de sensor "Humedad"
		tipo_sensor = "Humedad"
		#Guarda como valor del sensor el valor de la humedad
		vx = hum
		return tipo_sensor, vx
	if idx in id_nivel:
		print ("Es un sensor de nivel de agua en río")
		#Guarda como tipo de sensor "Nivel"
		tipo_sensor = "Nivel"
		#Guarda como valor del sensor el valor del nivel
		vx = nivel
		return tipo_sensor, vx
	if idx in id_acequia:
		print ("Es un sensor de nivel de agua en Acequia")
		#Guarda como tipo de sensor "Acequia"
		tipo_sensor = "Acequia"
		#Guarda como valor del sensor el valor del nivel
		vx = nivel
		return tipo_sensor, vx


def bdd(idx, sensor, fecha, tipo, valor, bateria):
	"""Función para guardar en la base de datos"""
	datos = (idx, sensor, fecha, tipo, valor, bateria)
	agregar = ("INSERT INTO datos (id, sensor, fecha, tipo, valor, bateria)VALUES "
		"(%s, %s, %s, %s, %s, %s);")
	#Ejecuta el comando agregar con los valores datos en MySQL
	cursor.execute(agregar, datos)
	#Es necesario ejecutar commit para que funcione
	cnx.commit()


def hora_now():
	"""Función para entregar la hora actual"""
	#Obtiene la hora actual
	hora = time.strftime("%H:%M:%S")
	#Obtiene la fecha actual
	fecha = time.strftime("%Y-%m-%d")
	fecha_total = fecha + " " + hora
	return fecha_total


global net
net = "si"
global hora_con
global hora_sin
hora_con = "0000-00-00 00:00:00"
hora_sin = "0000-00-00 00:00:00"
#Inicia el ciclo infinito del proyecto
while True:
	#Trata de realizar todo el proyecto
	try:
		#h = threading.Thread(target=internet)
		#h.start()
		print ("Llamando a la función de inicio")
		#Llama a la función de inicio
		inicio()
		#Si el sim800L funciona y responde con OK
		furula = conex()
		print (("La respuesta del SIM800L es: " + str(furula)))
		#Crea la conexión con MySQL
		cnx = mysql.connector.connect(user='root', password='Contrasena1',
			host='127.0.0.1', database='riorancheria')
		#Crea la variable cursor
		cursor = cnx.cursor()
		print ("Iniciando el ciclo infinito")
		#Inicia el ciclo infinito si el sim responde ok
		while furula:
			#Ejecuta la función primerx
			primerx()
	#Si hay un error de nombre de variable o no se puede dividir algún mensaje
	except mysql.connector.Error as err:
		print("Something went wrong: {}".format(err))
	except (ValueError, NameError, AttributeError):
		print ("Hay un error al separar o en una variable o un atributo")
		serie.close()
		cursor.close()
		cnx.close()
		print ("Fin del proceso")
	#Si interrumpo con ctrl c
	except KeyboardInterrupt:
		GPIO.cleanup()
		break
		serie.close()
		cursor.close()
		cnx.close()
		print ("Fin del proceso")
	#Cuando finalice el ciclo try
	finally:
		GPIO.cleanup()
		print ("Fin del try")
		serie.close()
		cursor.close()
		cnx.close()