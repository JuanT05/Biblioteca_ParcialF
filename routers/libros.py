from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    responses={404: {"description": "No encontrado"}}
)


# ==============================
# 🟢 Crear un libro
# ==============================
@router.post(
    "/",
    response_model=schemas.LibroResponse,
    status_code=201,
    summary="Crear un nuevo libro",
    description="Registra un nuevo libro en la base de datos. Valida que el ISBN no esté repetido."
)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    """
    ### Descripción:
    - Crea un nuevo libro asociado a un autor existente.
    - Evita duplicados mediante validación de ISBN.

    ### Parámetros:
    - **titulo**: título del libro
    - **isbn**: código único de identificación
    - **anio_publicacion**: año en que se publicó
    - **autor_id**: ID del autor
    - **copias_disponibles**: cantidad de ejemplares disponibles

    ### Respuestas:
    - **201**: Libro creado correctamente
    - **404**: Autor no encontrado
    - **409**: ISBN duplicado
    """
    autor = db.query(models.Autor).filter(models.Autor.id == libro.autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="El autor asociado no existe.")

    libro_existente = db.query(models.Libro).filter(models.Libro.isbn == libro.isbn).first()
    if libro_existente:
        raise HTTPException(status_code=409, detail="Ya existe un libro con ese ISBN.")

    nuevo_libro = models.Libro(**libro.dict())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro


# ==============================
# 🟢 Listar libros
# ==============================
@router.get(
    "/",
    response_model=list[schemas.LibroResponse],
    summary="Listar libros",
    description="Lista todos los libros o los filtra por año de publicación si se indica."
)
def listar_libros(
        anio: int = Query(None, description="Filtrar libros por año de publicación"),
        db: Session = Depends(get_db)
):
    if anio:
        libros = db.query(models.Libro).filter(models.Libro.anio_publicacion == anio).all()
    else:
        libros = db.query(models.Libro).all()

    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros.")
    return libros


# ==============================
# 🟢 Obtener libro por ID
# ==============================
@router.get(
    "/{libro_id}",
    response_model=schemas.LibroResponse,
    summary="Obtener libro por ID",
    description="Consulta la información detallada de un libro específico."
)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    return libro


# ==============================
# 🟡 Actualizar libro
# ==============================
@router.put(
    "/{libro_id}",
    response_model=schemas.LibroResponse,
    summary="Actualizar libro",
    description="Permite editar los datos de un libro ya registrado."
)
def actualizar_libro(libro_id: int, datos_actualizados: schemas.LibroCreate, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    if datos_actualizados.isbn != libro.isbn:
        libro_existente = db.query(models.Libro).filter(models.Libro.isbn == datos_actualizados.isbn).first()
        if libro_existente:
            raise HTTPException(status_code=409, detail="El nuevo ISBN ya está en uso.")

    for clave, valor in datos_actualizados.dict().items():
        setattr(libro, clave, valor)

    db.commit()
    db.refresh(libro)
    return libro


# ==============================
# 🔴 Eliminar libro
# ==============================
@router.delete(
    "/{libro_id}",
    status_code=204,
    summary="Eliminar libro",
    description="Elimina un libro por su identificador único."
)
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado correctamente."}
