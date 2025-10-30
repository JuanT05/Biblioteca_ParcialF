from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ------------------------
# Tabla intermedia N:N
# ------------------------
class AutorLibro(SQLModel, table=True):
    autor_id: Optional[int] = Field(default=None, foreign_key="autor.id", primary_key=True)
    libro_id: Optional[int] = Field(default=None, foreign_key="libro.id", primary_key=True)


# ------------------------
# Tabla Autor
# ------------------------
class Autor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais_origen: str
    anio_nacimiento: int

    libros: List["Libro"] = Relationship(back_populates="autores", link_model=AutorLibro)


# ------------------------
# Tabla Libro
# ------------------------
class Libro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    isbn: str = Field(unique=True, index=True)
    anio_publicacion: int
    copias_disponibles: int

    autores: List[Autor] = Relationship(back_populates="libros", link_model=AutorLibro)
