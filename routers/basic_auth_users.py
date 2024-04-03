from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# Ultimo modulo importado es para pasar el password y obtener el password

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login") # Para manejar el password

# Creación de la entidad User
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev":{
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mouredev.com",
        "disabled": False,
        "password": "123456"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "654321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # ** Especifico numero arbitrario de parametros

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)): # Depende de OAuth2
    user = search_user(token) # Paso el token con Auth/Bearer en Thunderclient
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas", 
            headers={"WWW-Authenticate": "Bearer"}) # Cabeceras son con estándar
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo")
    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): # Capturar parametro form, por defecto viene de Depends
    # Depends: funcion recibe datos pero no depende de nadie
    # Envio usuario y contraseña con un Form (con campo username y password)
    user_db = users_db.get(form.username) # Busca si usuario existe
    if not user_db: # Si usuario no existe
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"} # Retorna access token (es una string o texto encriptado que pasa el backend siempre que ya nos autenticamos)
    #                                                              y de tipo bearer (por estandar en OAuth2)

@router.get("/users/me")
async def me(user: User = Depends(current_user)): #Depends (criterio de dependencia)
    return user
