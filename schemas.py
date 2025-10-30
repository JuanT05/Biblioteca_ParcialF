from typing import Optional
from pydantic import BaseModel

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

class LibroBase(BaseModel):
    titulo: str
    isbn: str
    anio_publicacion: int
    copias_disponibles: int

class LibroCreate(LibroBase):
    pass

class Libro(LibroBase):
    id: int
    class Config:
        orm_mode = True
