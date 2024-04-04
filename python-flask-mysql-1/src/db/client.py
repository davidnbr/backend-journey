# install mysql-connector-python == 8.0.29
import mysql.connector

database = mysql.connector.connect(
    host="host",
    port=0000,
    user="user",
    password="pass",
    database="db"
)
