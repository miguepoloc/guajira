# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
#Importamos la librería de tiempo
import time

serie = serial.Serial("/dev/ttyS0", 38400)
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
print("Escribiendo 1,0")
#Muestra el mensaje por el puerto serial
serie.write("AT+CNMI=1,0,0,0,0\r\n")
time.sleep(1)


def primerx():
	"""Lee la primera línea del puerto serial
		Si llegó un SMS (+CMT) lee la segunda línea"""
	serie.write('AT+CMGL="ALL"\r\n')
	serie.reset_input_buffer()
	control = True
	while control:
		#+CMGL: 9,"REC READ","3003859853","","18/02/19,11:42:55-20"
		#Prueba x
		linea = serie.readline()
		if linea.startswith("+CMGL:") is True:
			cm, r, c1, numero, c2, n, c3, fecha, n2 = linea.split('"')
			cmg, nada = cm.split(",")
			cmgl, id_sms = cmg.split(" ")
			print (id_sms)
			print (numero)
			print (fecha)
		if "OK" in linea:
			control = False
		print ("-----------------------------------------------------------")
	print ("FIN")

primerx()
#for item in lista:
	##print item
	#if item.startswith("+CMGL:") is False:
		#if item != "OK":
			#msg.append(item)
			#print (msg)