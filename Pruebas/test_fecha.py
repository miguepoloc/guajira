# -*- coding: utf-8 -*-
import time


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

hora_now()