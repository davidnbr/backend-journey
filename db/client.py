### MongoDB Client ###
# Descarga versión community: https://www.mongodb.com/try/download/
# Instalación: https://www.mongodb.com/docs/manual/tutorial
# Modulo conexión MongoDB: pip install pymongo
# Ejecución: "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="c:\data\db"
# Conexión: mongodb://localhost

from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local # Si no coloco ninguna url en los parámetros, se conecta a local por defecto

# Base de datos remota
db_client = MongoClient(
    "mongoURI").test
