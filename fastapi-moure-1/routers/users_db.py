### Users DB API ###

from fastapi import APIRouter, HTTPException, status
from db.models.user import User # Importo instancia User que esta en fichero user.py
from db.schemas.user import user_schema, users_schema
from db.client import db_client # Importo instancia de Database creada por nosotros en client.py
from bson import ObjectId # Importo la clase donde se encuentra el objeto ObjectId que esta en MongoDB

router = APIRouter(prefix="/userdb", 
                   tags=["Users DB"], 
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

users_list = []

@router.get("/", response_model=list[User]) # Response model para colocar el tipo que da de respuesta
async def users():
    return users_schema(db_client.users.find()) # Devuelvo todos los usuarios

# PATH
@router.get("/{id}")
async def user(id: str): # Siempre tipado con FastAPI
    return search_user("_id", ObjectId(id))

# QUERY
@router.get("/")
async def user(id: str): # para la busqueda con query se coloca ?id=1 el tipado sirve para retornar el mensaje de error correcto
    return search_user("_id", ObjectId(id))

# Ingresa usuarios, se envia json con username e email
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email))==User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe") # Enviar codigo de error con raise y HTTPException

    user_dict = dict(user) # Transformo el usuario en un diccionario (en un json)
    del user_dict["id"] # Elimino el id del diccionario para que id lo genere MongoDB

    id = db_client.users.insert_one(user_dict).inserted_id # En base local, creo esquema users y guardo el usuario
    # Puedo ahora buscar el id ya creado
    new_user = user_schema(db_client.users.find_one({"_id": id})) # Busco el usuario con el id generado

    return User(**new_user)

@router.put("/", response_model=User)
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) # Devuelvo 204 si sale bien
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)}) # Busco el usuario con el id en base de datos
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else:
        return {"message": "Usuario eliminado"}

# Replace cambia el documento por completo, update actualiza un campo concreto

def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key}) # Busco el usuario con el email en base de datos
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}