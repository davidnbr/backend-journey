from pydantic import BaseModel # Libreria pydantic permite gestionar modelos

# str | None: Indica que puede ser un entero o un nulo, es decir, opcional puede que no nos llegue

class User(BaseModel):
    id: str = None
    username: str
    email: str