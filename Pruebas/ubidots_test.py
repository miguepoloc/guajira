import time
import requests
import math

c = 0

while(1):
	c = c + 1
	payload = {'luz': round(20*math.cos(c),2)}
	r = requests.post('http://things.ubidots.com/api/v1.6/devices/Prueba/?token=xCkzXnlC2DAV4vH9nkvnqpwLBqElo2', data=payload)
	print (c)
	time.sleep(0.5)