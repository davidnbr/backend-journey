from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter() # Para crear router (incluir en main para que se pueda acceder al iniciar uvicorn con main)

# Iniciar servidor uvicorn users:app --reload

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Brais", surname="Moure", url="https://moure.dev", age=35),
         User(id=2,name="Moure", surname="Dev", url="https://mouredev.com", age=35),
         User(id=3,name="Haakon", surname="Dahlberg", url="https://haakon.com", age=33)]

@router.get("/usersjson")
async def usersjson():
    return [{"name": "Brais", "surname":"Moure", "url": "https://moure.dev","age": 35},
            {"name": "Moure", "surname":"Dev", "url": "https://mouredev.com","age": 35},
            {"name": "Haakon", "surname":"Dahlberg", "url": "https://haakon.com","age": 33}]

@router.get("/users")
async def users():
    return users_list

# PATH
@router.get("/user/{id}")
async def user(id: int): # Siempre tipado con FastAPI
    return search_user(id)

# QUERY
@router.get("/user/")
async def user(id: int): # para la busqueda con query se coloca ?id=1 el tipado sirve para retornar el mensaje de error correcto
    return search_user(id)


@router.post("/user/",response_model=User, status_code=201) #status_code colocamos que por defecto devuelva un 201
async def user(user: User): # como ya fue definido el objeto user, se puede pasar un json y fastapi entiende
    if type(search_user(user.id))==User:
        raise HTTPException(status_code=204, detail="El usuario ya existe") # Enviar codigo de error con raise y HTTPException
    else:
        users_list.append(user)
        return user

@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
        
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user, {"message": "Usuario actualizado"}

@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    else:
        return {"message": "Usuario eliminado"}

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}