from fastapi import APIRouter

router = APIRouter(prefix="/products", # Ruta predeterminada de todo el fichero
                   tags=["products"], # Etiquetas para la documentación
                   responses={404: {"message":"No encontrado"}}) # Si hay algun problema enviar un 404 con un mensaje

products_list = ["Producto 1", "Producto 2", "Producto 3","Producto 4","Producto 5"]

@router.get("/") # Quiere decir que va a /products/
async def products():
    return products_list

@router.get("/{id}") # Quiere decir que va a /products/{id}
async def products(id: int):
    return products_list[id]