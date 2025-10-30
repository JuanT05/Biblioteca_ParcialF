from pydantic import BaseModel, Field, validator
from typing import Optional

# ==========================
# 📘 Esquemas para Autor
# ==========================
class AutorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del autor")
    pais: str = Field(..., min_length=2, max_length=50, description="País de origen del autor")


class AutorCreate(AutorBase):
    pass


class AutorResponse(AutorBase):
    id: int

    class Config:
        orm_mode = True


# ==========================
# 📗 Esquemas para Libro
# ==========================
class LibroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150, description="Título del libro")
    isbn: str = Field(..., min_length=10, max_length=13, description="Código ISBN del libro (10 o 13 dígitos)")
    anio_publicacion: int = Field(..., gt=0, lt=2100, description="Año de publicación del libro")
    copias_disponibles: int = Field(..., ge=0, description="Número de copias disponibles")
    autor_id: int = Field(..., gt=0, description="ID del autor asociado")

    # 🧩 Validador para ISBN (solo dígitos)
    @validator("isbn")
    def validar_isbn(cls, v):
        if not v.isdigit():
            raise ValueError("El ISBN solo puede contener números")
        if len(v) not in (10, 13):
            raise ValueError("El ISBN debe tener 10 o 13 dígitos")
        return v


class LibroCreate(LibroBase):
    pass


class LibroResponse(LibroBase):
    id: int
    class Config:
        orm_mode = True
