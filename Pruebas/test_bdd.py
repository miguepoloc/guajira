# -*- coding: utf-8 -*-
import mysql.connector
import subprocess
import time


cnx = mysql.connector.connect(user='root', password='Contrasena1',
		host='127.0.0.1', database='riorancheria')
cursor = cnx.cursor()


def internet():
	"""Realiza un ping a google"""
	global net
	#while True:
	w = subprocess.Popen(["ping", "-c 1", "www.google.com"],
		stdout=subprocess.PIPE)
	w.wait()
	if w.poll():
		print ("No hay internet")
		time.sleep(2)
		net = False
	else:
		print ("Si hay internet")
		time.sleep(2)
		net = True


def hora_now():
	"""Función para entregar la hora al nodo con 20 sg de más"""
	#Obtiene la hora actual
	hora = time.strftime("%H:%M:%S")
	print ("La hora actual es: " + hora)
	#Obtiene la fecha actual
	fecha = time.strftime("%Y-%m-%d")
	print ("La fecha actual es: " + fecha)
	fecha_total = fecha + " " + hora
	print (("bdd " + fecha_total))
	return fecha_total


def consulta_bdd(fecha_menor, fecha_mayor):
	"""Función para entregar la hora al nodo con 20 sg de más"""
#	global net
	query = ("SELECT * FROM datos WHERE fecha BETWEEN %s AND %s;")
	datos = (fecha_menor, fecha_mayor)
	cursor.execute(query, datos)
	##cnx.commit()
	for (id, sensor, fecha, tipo, valor, bateria) in cursor:
		print(("id {}, sensor {}, fecha{}, tipo {}, valor {}, bateria {}".format(
			id, sensor, fecha, tipo, valor, bateria)))

try:
	internet()
	hora1 = hora_now()
	print (net)
	time.sleep(200)
	hora2 = hora_now()
	consulta_bdd(hora1, hora2)
finally:
	cursor.close()
	cnx.close()