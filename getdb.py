import psycopg2

conexion1 = psycopg2.connect(database="chirpstack_ns", user="chirpstack_ns", password="dbpassword")

cursor1=conexion1.cursor()

cursor1.execute("select dev_eui from device")

for value in cursor1:
    print(value)

conexion1.close() 