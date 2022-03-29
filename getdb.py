from multiprocessing import connection
import psycopg2

connection = psycopg2.connect(host="localhost", 
                            database="chirpstack_ns", 
                            user="chirpstack_ns", 
                            password="dbpassword")

cursor=connection.cursor()

selectdeveui= "select dev_eui from device"
cursor.execute("selectdeveui")
mobile_records = cursor.fetchall()

for value in cursor:
    print(value)

if connection:
    cursor.close()
    connection.close()