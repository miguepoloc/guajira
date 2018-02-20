from ubidots import ApiClient

#Colocamos el Token, no el API
api = ApiClient(token='xCkzXnlC2DAV4vH9nkvnqpwLBqElo2')
#Id de la variable
my_variable = api.get_variable('5a6d34adc03f9709395ea9fe')
##Enviar un valor
new_value = my_variable.save_value({'value': 30})
##Enviar valor y gps
#new_value = my_variable.save_value({'value': 10,
	#'context': {'lat': 33.0822, 'lng': -117.24123}})
##Valor con hora
#new_value = my_variable.save_value({'value': 20, 'timestamp': 1376061804407})
##Guardar con una sola peticion varias variables
##api.save_collection([{'variable': '5a6d34adc03f9709395ea9fe', 'value': 90},
##	{'variable': '557f68747625426b97263cba', 'value':20}])
##Guardar varios valores en una misma variable con una sola peticion
#my_variable.save_values([
	#{'timestamp': 1380558972614, 'value': 20,
		#'context':{'lat': 33.0822, 'lng': -117.24123}},
	#{'timestamp': 1380558972915, 'value': 40},
	#{'timestamp': 1380558973516, 'value': 50},
	#{'timestamp': 1380558973617, 'value': 30}
#])

##Obtiene el ultimo valor de la variable
#last_value = my_variable.get_values(1)
#print last_value[0]['value']

##Toma decisiones en base al valor

#if last_value[0]['value']:
	#print "Switch is ON"
#else:
	#print "Switch is OFF"