# -*- coding: utf-8 -*-
import time

import mysql.connector


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

cnx = mysql.connector.connect(user='root', password='Contrasena1',
	host='127.0.0.1', database='riorancheria')
cursor = cnx.cursor()

query = ("SELECT * FROM datos WHERE fecha BETWEEN %s AND %s;")
#query = ("SELECT * FROM datos WHERE 1;")
fecha_start = "2018-02-03 14:00:00"
fecha_end = hora_now()

datos = (fecha_start, fecha_end)

cursor.execute(query, datos)

##cnx.commit()

for (id, sensor, fecha, tipo, valor, bateria) in cursor:
	p = ("{} {} {} {} {} {}".format(id, sensor, fecha, tipo, valor, bateria))
	print (p)

cursor.close()
cnx.close()