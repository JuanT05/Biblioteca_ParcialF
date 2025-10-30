from typing import List, Optional
from sqlmodel import SQLModel

# -------------------------
# Schemas para Autor
# -------------------------
class AutorBase(SQLModel):
    nombre: str
    pais_origen: str
    anio_nacimiento: int


class AutorCreate(AutorBase):
    pass


class AutorRead(AutorBase):
    id: int
    class Config:
        orm_mode = True


# -------------------------
# Schemas para Libro
# -------------------------
class LibroBase(SQLModel):
    titulo: str
    isbn: str
    anio_publicacion: int
    copias_disponibles: int


class LibroCreate(LibroBase):
    autores_ids: Optional[List[int]] = []  # lista de IDs de autores


class LibroRead(LibroBase):
    id: int
    class Config:
        orm_mode = True
