import psycopg2
import socket

connection = psycopg2.connect(host="localhost",
                            database="chirpstack_ns", 
                            user="chirpstack_ns", 
                            password="dbpassword")

cursor=connection.cursor()

selectdeveui= "select dev_eui from device"
cursor.execute(selectdeveui)
deveui = cursor.fetchall()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

f = open('devices.db', 'w')

for value in deveui:
    print("dev_eui = ", bytes(value[0]).hex())
    f.write (str(bytes(value[0]).hex()) + ' ' + '60' + 'IN' + 'A' + ip_address)
if connection:
    cursor.close()
    connection.close()





