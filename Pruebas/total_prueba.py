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
#import RPi.GPIO as GPIO

#GPIO.cleanup()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT)
#GPIO.output(18, False)

#Id de cada punto
estmet = (1, 2)
s_nivel = (3, 4, 5, 6, 7)
s_acequia = (8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
s_hum = (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
	29, 30, 31, 32, 33, 34, 35, 36, 37)

#Números de los nodos
nx = (3003859853, 3008158188, 3045410584)

#Inicia la comunicación seria por el puerto ttyS0 a 38400
#Se usa esta velocidad porque no falla el módulo
print ("Iniciando el serial")
serie = serial.Serial("/dev/ttyS0", 38400)


def primero():
	"""Lee la primera línea del puerto serial
		Si llegó un SMS (+CMT) lee la segunda línea"""
	#Lee la línea del puerto serial
	primera = serie.readline()
	#print ("Leyendo la primera linea")
	#Si está el comando +CMT en la línea
	if "+CMT" in primera:
		print ("Primera parte")
		print (primera)
		#Primera = '+CMT: "3003859853","","18/01/18,16:43:01-20"'
		separado = primera.split('"')
		print (separado)
		cmt, numero, coma1, nada, coma, fecha, fdl = separado
		#Llama a la función segundx
		numero = int(numero)
		if numero in nx:
			print ("Llamando a la segunda función")
			segundx()
		else:
			pass


def valor_s(idx, hum, nivel):
	"""Devuelve el tipo de sensor y el valor a guarda de cada punto según la id"""
	if idx in s_hum:
		print ("Es humedad")
		v_sensor = "Humedad"
		vx = hum
		return v_sensor, vx
	if idx in s_nivel:
		print ("Es nivel")
		v_sensor = "Nivel"
		vx = nivel
		return v_sensor, vx
	if idx in s_acequia:
		print ("Acequia")
		v_sensor = "Acequia"
		vx = nivel
		return v_sensor, vx
	if idx in estmet:
		v_sensor = "Estacion"
		vx = hum
		return v_sensor, vx


def segundx():
	"""Lee la segunda línea del puerto serial"""
	juan = True
	while juan:
		#segunda = serie.readline()
		segunda = "18 090 030 0000 13:40:30 24/01/2018\r\n"
		print ("Segunda parte")
		print (segunda)
		if "\r\n" in segunda:
			mejora(segunda)
			juan = False
		else:
			mejora(segunda)


def mejora(linea):
	"""Lee la segunda línea del puerto serial"""
	cantidad = len(linea)
	if cantidad > 5:
		separado = linea.split(' ')
		print ("Dividiendo por espacio")
		print (separado)
		#Guarda en cada variable su valor asignado
		idx, bat, hum, nivel, hora, fecha = separado
		#Arregla la fecha al formato de MySQL
		f_h = fecha_ok(fecha, hora)
		print ("Fecha buena")
		print (f_h)
		#Convierte a entero el id para poder compararlo
		idy = int(idx)
		#Guarda el valor y el tipo de sensor dependiendo del id si es humedad o nivel
		v_s, valor = valor_s(idy, hum, nivel)
		print ("Los valores buenos")
		#Guarda en la base de datos el id, cuál es, fecha, el tipo de sensor y valor
		bdd(idx, 'prueba', f_h, v_s, valor, bat)
		print("Enviando mqtt...")
		#Publica por MQTT
		topic = idx + "/" + v_s
		print (topic)
		publish.single(topic, valor, hostname="127.0.0.1")
	else:
		pass


def bdd(idx, sensor, fecha, tipo, valor, bateria):
	"""Lee la segunda línea del puerto serial"""
	print ("Guardando en la base de datos")
	datos = (idx, sensor, fecha, tipo, valor, bateria)
	agregar = ("INSERT INTO datos (id, sensor, fecha, tipo, valor, bateria)VALUES "
		"(%s, %s, %s, %s, %s, %s);")
	cursor.execute(agregar, datos)
	cnx.commit()


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


def inicio():
	"""Acomoda el módulo para recibir mensajes"""
	#Se cierra el puerto por si había otra comunicación
	serie.close()
	print ("Cerrando")
	#Se abre el puerto serial
	serie.open()
	print ("Abriendo")
	#Escribe AT para comprobar que se está comunicando con el SIM800L
	serie.write("AT\r\n")
	time.sleep(1)
	print("Escribiendo =1")
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
	mal = True
	cnt = 0
	while mal:
		serie.write("AT\r\n")
		time.sleep(1)
		x = serie.readline()
		if "OK" in x:
			mal = False
			cnt = 0
			return True
		else:
			mal = True
			cnt = cnt + 1
			#GPIO.output(18, True)
			#time.sleep(1)
			#GPIO.output(18, False)
			if (cnt == 3):
				pass
				#Mandar gmal
			#return False


try:
	print ("Llamando inicio")
	#inicio()
	#furula = conex()
	#print (("Furla? " + str(furula)))
	cnx = mysql.connector.connect(user='root', password='Contrasena1',
		host='127.0.0.1', database='riorancheria')
	cursor = cnx.cursor()
	#print ("Ciclo infinito")
	#while furula:
	#	primero()
	segundx()

except KeyboardInterrupt:
	serie.close()
	cursor.close()
	cnx.close()