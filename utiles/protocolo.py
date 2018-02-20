# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
#Importamos la librería de tiempo
import time
import paho.mqtt.publish as publish
import mysql.connector
from datetime import date

print("Abriendo puerto serie")
serie = serial.Serial('/dev/ttyS0', 38400)
serie.close()
serie.open()
serie.write("AT\r\n")
time.sleep(1)
print("#escribiendo =1")
serie.write("AT+CMGF=1\r\n")
time.sleep(1)
print("Escribiendo 2,2")
serie.write("AT+CNMI=2,2,0,0,0\r\n")
time.sleep(1)
print("Ciclo infinito")

cnx = mysql.connector.connect(user='root', password='Contrasena1',
	host='127.0.0.1', database='riorancheria')

cursor = cnx.cursor()


try:
	while 1:
		primera = serie.readline()
		if "+CMT" in primera:
			print ("Primera parte")
			print (primera)
			segunda = serie.readline()
			print ("Segunda parte")
			print (segunda)
			#segunda = "01 090 001 0000 11:49:39 23/01/2018"
			separado = segunda.split(' ')
			print (separado)
			idx, bat, hum, nivel, hora, fecha1 = separado
			print("Enviando mqtt...")
			publish.single(idx + "/bat", bat, hostname="127.0.0.1")
			publish.single(idx + "/hum", hum, hostname="127.0.0.1")
			fecha2 = fecha1.split('/')
			dia1, mes1, anio1 = fecha2
			dia = int(dia1)
			mes = int(mes1)
			anio = int(anio1)
			fecha = date(anio, mes, dia)
			fh = str(fecha) + " " + hora
			print (fh)
			print ("Guardando en la base de datos")
			datos = (fh, hum)
			agregar = ("INSERT INTO datos (sensor, fecha, tipo, valor)VALUES ('prueba',"
				"%s, 'tipo', %s);")
			cursor.execute(agregar, datos)
			cnx.commit()


except KeyboardInterrupt:
	serie.close()
	cursor.close()
	cnx.close()