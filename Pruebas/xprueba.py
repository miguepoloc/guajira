# -*- coding: utf-8 -*-
#Importamos la librería serial
import serial
#Importamos la librería de tiempo
import time

print ("Abriendo el puerto serie")
serie = serial.Serial('/dev/ttyS0', 9600)
serie.close()
serie.open()
print ("Mandado el =1")
serie.write("AT+CMGF=1\r\n")
time.sleep(1)
print ("mandando el 2,2")
serie.write("AT+CNMI=2,2,0,0,0\r\n")
time.sleep(1)

while 1:
    respuesta = serie.readline()
    if "+CMT" in respuesta:
        print (respuesta)
        r = serie.readline()
        print (r)
