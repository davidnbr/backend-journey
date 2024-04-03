def user_schema(user) -> dict: # Estoy tipando la salida de la funcion, declaro que quiero un diccionario
    return {
        "id": str(user["_id"]), # Busco los campos del json obtenido de MongoDB
        "username": user["username"],
        "email": user["email"]
    }

def users_schema(users) -> list: # Estoy tipando la salida de la funcion, declaro que quiero una lista
    return [user_schema(user) for user in users] # Recorro los usuarios en el listado para generar el dict