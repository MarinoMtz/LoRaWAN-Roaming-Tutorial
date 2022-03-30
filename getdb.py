import ctypes
import psycopg2

connection = psycopg2.connect(host="localhost", 
                            database="chirpstack_ns", 
                            user="chirpstack_ns", 
                            password="dbpassword")

cursor=connection.cursor()

selectdeveui= "select * from device"
cursor.execute(selectdeveui)
deveui = cursor.fetchall()

for row in deveui:
    print("dev_eui = ", row[0], )
    print("created_at = ", row[1])
    print("updated_at  = ", row[2], "\n")

if connection:
    cursor.close()
    connection.close()