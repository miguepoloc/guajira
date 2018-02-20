# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
#Importamos la librería de tiempo
import time
#Importamos la librería de MQTT para publicar
import paho.mqtt.publish as publish
print("Abriendo puerto serie")

#Se abre el puerto serial /dev/ttyS0 a 38400 baudios, ya que, a esa velocidad no molesta el sim 900
serie = serial.Serial('/dev/ttyS0', 38400)
serie.close()
serie.open()
print("#escribiendo =1")
#Se coloca el sim en modo SMS
serie.write("AT+CMGF=1\r\n")
time.sleep(1)
print("Escribiendo 2,2")
#Nos permite visualizar los mensajes en pantalla
serie.write("AT+CNMI=2,2,0,0,0\r\n")
time.sleep(1)
print("Ciclo infinito")

#mensaje = ('+CMT: "3003859853","","18/01/18,16:43:01-20\n"Hola mundo')
while 1:
	primera = serie.readline()
	if "+CMT" in primera:
		print ("Primera parte")
		print (primera)
		segunda = serie.readline()
		print ("Segunda parte")
		print (segunda)
		separado = primera.split('"')
		print (separado)
		cmt, numero, coma1, espacio, coma2, fechat, salto = separado
		print ("El numero es: ", numero)
		fecha = fechat[22:30]
		hora = fechat[31:39]
		print ("La fecha es: ", fecha)
		print ("La hora es: ", hora)
		print("Enviando primera parte...")
		publish.single("primera", primera, hostname="127.0.0.1")
		print("Enviando segunda parte...")
		publish.single("segunda", segunda, hostname="127.0.0.1")
