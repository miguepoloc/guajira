#!/usr/bin/python
# -*- coding: utf-8 -*-
#Librería para mandar un correo
import smtplib


def send_email(tx, passtx, rx, protocolo, asunto, cuerpo):
	"""Envia un correo electrónico"""
	#Persona que envía el mensaje
	tx = tx
	passtx = passtx
	#Persona que recibe el mensaje
	rx = rx
	#Asunto del mensaje
	asunto = asunto
	#Cuerpo del mensaje
	cuerpo = cuerpo
	#Protocolo del envío del correo
	email = protocolo % (tx, rx, asunto, cuerpo)
	#Entrando al servidor de gmail
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	#Entra a la cuenta del tx
	server.login(tx, passtx)
	#Envía el correo
	server.sendmail(tx, rx, email)
	#Cierra la cuenta
	server.quit()

pr_email = """From: %s
To: %s
MIME-Version: 1.0
Content-type: text/html
Subject: %s

%s
"""

send_email(
	tx='miguepoloc@gmail.com', passtx='MI2008gue',
	rx='miguelpolo.energesis@gmail.com',
	protocolo=pr_email,
	asunto="E-mal enviado desde Python",
	cuerpo="""Hola!<br/> <br/>
	Este es un <b>e-mail</b> enviando desde <b>Python</b>
	""")
