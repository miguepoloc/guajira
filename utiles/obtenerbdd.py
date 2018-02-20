import datetime
import mysql.connector

cnx = mysql.connector.connect(user='root', password='Contrasena1',
                              host='127.0.0.1',
                              database='riorancheria')

cursor = cnx.cursor()

query = ("SELECT * FROM datos;")

hire_start = datetime.date(1999, 1, 1)
hire_end = datetime.date(1999, 12, 31)

cursor.execute(query)

for (sensor, fecha, tipo, valor) in cursor:
  print("sensor {}, fecha {:%d %b %Y}, tipo {}, valor {}".format(
    sensor, fecha, tipo, valor))

cursor.close()
cnx.close()