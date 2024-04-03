from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError # Importo jwt (capaz de encriptar y desencriptar) y JWTError para manejar errores
from passlib.context import CryptContext
from datetime import datetime, timedelta # Para usar fecha del sistema y calculos con fechas

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # 1 minuto de duracion para access token
SECRET = "0956770dfa7db4ae805f853cc5c25ee2bcdf4d24b3ddd64d72546057d4524bb9"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"]) # Algoritmo de encriptacion usado

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
        "password": "$2a$12$XCzOU4vzcmVTEeb3.2sRvenLdxruXAnV8eCFNuYKF8seD0zGc3o0q"
    },
    "mouredev2":{
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mouredev.com",
        "disabled": True,
        "password": "$2a$12$eDx6eDFKv7WGLX00Hn1PvuYL3bCfRwXShCjsQE6i6kjfcVWtlDUQ."
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)): # Depende de OAuth2
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticación inválidas", 
                            headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub") # Decodifica token
        if username is None: # Si obtiene usuario y esta vacio genera error
            raise exception
        
    except JWTError: # Maneja error de decodificar
        raise exception
    
    return search_user(username) # Retorna usuario decodificado
    
async def current_user(user: User = Depends(auth_user)): # Depende de auth_user
    # Aqui ya se pasa el usuario decodificado con auth_user
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autenticación inválidas", 
            headers={"WWW-Authenticate": "Bearer"}) # Cabeceras son con estándar
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password): # Verifica contraseña ingresada y contraseña guardada encriptada
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)} # Informacion del token (en este caso usado username y tiempo de expiracion)
                    # obtiene tiempo de sistema y suma delta de un minuto

    return {"access_token": jwt.encode(access_token, SECRET,algorithm=ALGORITHM), "token_type": "bearer"} # Retorna token y tipo de token

@router.get("/users/me") # Cuando se haga el get, solo debe pasar el Auth, no la FORM. Eso genera error
async def me(user: User = Depends(current_user)):
    return user