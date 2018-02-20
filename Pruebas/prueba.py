# -*- coding: utf-8 -*-
mensaje = ('+CMT: "3003859853","","18/01/18,16:43:01-20\n"Hola mundo')
print (mensaje)
separado = mensaje.split('"')
print (separado)
cmt, numero, coma1, espacio1, coma2, fecha, sms = separado

if "+CMT" in mensaje:
	print ("El número es: ", numero)
	print ("La fecha es: ", fecha)
	print ("El mensaje es: ", sms)
	idx = sms[0:2]
	print(idx)
