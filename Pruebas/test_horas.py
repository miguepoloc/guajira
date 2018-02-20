# -*- coding: utf-8 -*-
import time


def hora_now():
	"""Función para entregar la hora al nodo con 20 sg de más"""
	#Obtiene la hora actual
	hora = time.strftime("%H:%M:%S")
	#Obtiene la fecha actual
	fecha = time.strftime("%Y-%m-%d")
	fecha_total = fecha + " " + hora
	return fecha_total

hora_sin = hora_now()
time.sleep(3)
hora_con = hora_now()
if hora_con > hora_sin:
	print ("Si")