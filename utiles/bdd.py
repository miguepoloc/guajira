import mysql.connector

cnx = mysql.connector.connect(user='root', password='Contrasena1',
	host='127.0.0.1', database='riorancheria')

cursor = cnx.cursor()

agregar = ("INSERT INTO datos (sensor, fecha, tipo, valor)VALUES ('prueba',"
	"'2018-01-20 05:23:32', 'tipo', '33');")

cursor.execute(agregar)

cnx.commit()
cursor.close()
cnx.close()