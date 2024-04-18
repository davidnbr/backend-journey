# For remote connection to Railway
# install mysql-connector-python == 8.0.29
"""import mysql.connector

database = mysql.connector.connect(
    host="viaduct.proxy.rlwy.net",
    port=58214,
    user="root",
    password="uEdDoyhBohALDxWuMLJRnXgURbLIUnFu",
    database="railway"
)"""

import mysql.connector

__cnx = None

def get_sql_connection():

    global __cnx

    if __cnx is None:
        __cnx = mysql.connector.connect(
                user='root',
                password='root',
                host='localhost',
                database='grocery_store'
            )
    
    return __cnx