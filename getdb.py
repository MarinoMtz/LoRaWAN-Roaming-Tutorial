import ctypes
import psycopg2

connection = psycopg2.connect(host="localhost", 
                            database="chirpstack_ns", 
                            user="chirpstack_ns", 
                            password="dbpassword")

cursor=connection.cursor()

selectdeveui= "select dev_eui from device"
cursor.execute(selectdeveui)
deveui = cursor.fetchall()

for value in deveui:
    print(type(value), value[0])
    address = id(value[0])
    print(ctypes.cast(address, ctypes.py_object).value)

if connection:
    cursor.close()
    connection.close()