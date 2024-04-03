from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db # Importo las rutas de los ficheros que creamos
from fastapi.staticfiles import StaticFiles # Para exponer (poder acceder desde navegador) recursos estaticos como imagenes

# Crear instancia de FastAPI
app = FastAPI()

# Routers
app.include_router(products.router) # Añade las otras rutas de los ficheros que creamos
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


app.mount("/static",StaticFiles(directory="static"),name="static") # Para exponer recursos estaticos

# Iniciar servidor: uvicorn main:app --reload
# Ruta root 127.0.0.1:8000
# Documentación Swagger: http://127.0.0.1:8000/docs
# Documentación Redocly: http://127.0.0.1:8000/redoc

# Define ruta raiz
@app.get("/")
async def root():
    return "¡Hola FastAPI!"

# Define ruta /url
@app.get("/url")
async def url():
    return {"url": "https://fastapi.tiangolo.com"}