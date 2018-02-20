# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
#Importamos la librería de tiempo
import time
import paho.mqtt.publish as publish
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
while 1:
	protocolo = serie.readline()
	if "+CMT" in protocolo:
		print ("primera parte")
		print (protocolo)
		mns = serie.readline()
		print ("mns parte")
		print (mns)
		separado = mns.split(' ')
		print (separado)
#		idx, bat, hum, nivel, hora, fecha = separado
#		print("Enviando mqtt...")
#		publish.single("01/bat", bat, hostname="127.0.0.1")
#		publish.single("01/hum", hum, hostname="127.0.0.1")