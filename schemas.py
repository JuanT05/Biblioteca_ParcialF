from typing import Optional, List
from pydantic import BaseModel

# ----- AUTORES -----
class AutorBase(BaseModel):
    nombre: str
    pais_origen: str
    anio_nacimiento: int

class AutorCreate(AutorBase):
    pass

class Autor(AutorBase):
    id: int
    class Config:
        orm_mode = True


# ----- LIBROS -----
class LibroBase(BaseModel):
    titulo: str
    isbn: str
    anio_publicacion: int
    copias_disponibles: int
    autor_id: int  # 🔗 Relación con el autor

class LibroCreate(LibroBase):
    pass

class Libro(LibroBase):
    id: int
    autor: Optional[Autor] = None  # Para devolver los datos del autor
    class Config:
        orm_mode = True
