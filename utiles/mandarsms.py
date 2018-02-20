import serial   #Importamos la librería serial
from curses import ascii    #Importamos la librería de ascii para el control z
import time     #Importamos la librería de tiempo
 
serie = serial.Serial('/dev/ttyS0', 9600)   #Abrimos el puerto serie ttyS0 a 9600 baudrate
#serie.open()
try:
    serie.close()
    serie.open()
    serie.write(b"AT\n")            #Escribimos el comando AT esperando la respuesta de Ok
    #print (serie.readline())
    time.sleep(1)                   #Damos una espera de 1s
    #r = serie.read(size=10)
    #print(r)
    
    serie.write(b"AT+CMGF=1\r\n")   #Le ponemos en modo para SMS
    time.sleep(1)                   #Damos una espera de 1s
    #print (serie.readline())
    serie.write(b"AT+CMGS=\"+573003859853\"\r\n")   #Le pasamos el numero al que vamos ha mandar el SMS
    time.sleep(1)                   #Damos una espera de 1s
    #print (serie.readline())
    serie.write(b"Hola desde la raspberry prueba")  #Le pasamos el mensaje a enviar
    time.sleep(1)                   #Damos una espera de 1s
    #print (serie.readline())
    serie.write(ascii.ctrl("z").encode('UTF-8'))    #Termina el menzaje con Ctrl+z
    time.sleep(1)                   #Damos una espera de 1s
    #print (serie.readline())
    serie.write(b"\r\n")            #Le pasamos un fin de linea
    time.sleep(1)                   #Damos una espera de 1s
    #print (serie.readline())
 
except ValueError:
    print ("Oops! se ha producido un error ...")
