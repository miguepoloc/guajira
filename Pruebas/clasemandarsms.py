# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
import time
#Importamos la librería de ascii para el control z
from curses import ascii


#Creamos la clase Enviarsms
class Enviarsms:
	"""Clase para enviar un sms"""
	def __init__(self, receptor=""):
		"""Almacena las variables de la clase, el receptor"""
		self.receptor = receptor

	def conectar(self):
		"""Funcion para conectar el puerto"""
		#Abrimos el puerto serie ttyS0 a 38400 baudios
		self.serie = serial.Serial('/dev/ttyS0', 38400)
		time.sleep(1)

	def sendmensaje(self, mns=""):
		"""Función para enviar el mensaje"""
		self.serie.write(b'AT\r\n')
		time.sleep(1)
		#Le ponemos en modo para SMS
		self.serie.write(b'AT+CMGF=1\r\n')
		time.sleep(1)
		#encode('UTF-8') codificada a byte el mensaje
		#Comando para enviar el mensaje, se pasa el valor del número
		self.serie.write(b'AT+CMGS=\"' + self.receptor.encode('UTF-8') + b'\"\r\n')
		time.sleep(0.5)
		#Se escribe el mensaje
		self.serie.write(mns.encode('UTF-8'))
		time.sleep(0.5)
		#Termina el menzaje con Ctrl+z
		self.serie.write(ascii.ctrl("z").encode('UTF-8'))
		time.sleep(0.5)
		#Le pasamos un fin de linea
		self.serie.write(b'\r\n')
		print ("Mensaje enviado")
		self.serie.write("AT+CMGF=1\r\n")
		time.sleep(1)
		print("Escribiendo 2,2")
		#Muestra el mensaje por el puerto serial
		self.serie.write("AT+CNMI=2,2,0,0,0\r\n")
		time.sleep(1)
		while True:
			res = self.serie.readline()
			print (res)

	def desconectar(self):
		"""Función para cerrar el puerto"""
		self.serie.close()

#Cambiar el número de teléfono por el del destinatario y el mensaje
#Creamos el objeto sms
sms = Enviarsms("+573003859853")
#Abre el puerto serie
sms.conectar()
#Prepara el objeto para mandar el mensaje
sms.sendmensaje("f:26/01/2018 h:16:37:40")
#sms.desconectar()