from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
    responses={404: {"description": "No encontrado"}}
)


# ==============================
# 🟢 Crear un autor
# ==============================
@router.post(
    "/",
    response_model=schemas.AutorResponse,
    status_code=201,
    summary="Crear un nuevo autor",
    description="Crea un autor nuevo si no existe otro con el mismo nombre."
)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    """
    ### Descripción:
    - Crea un nuevo autor en la base de datos.
    - Valida que el nombre no esté repetido.

    ### Parámetros:
    - **nombre**: nombre completo del autor
    - **pais**: país de origen

    ### Respuestas:
    - **201**: Autor creado correctamente
    - **409**: Ya existe un autor con ese nombre
    """
    autor_existente = db.query(models.Autor).filter(models.Autor.nombre == autor.nombre).first()
    if autor_existente:
        raise HTTPException(status_code=409, detail="Ya existe un autor con ese nombre.")

    nuevo_autor = models.Autor(**autor.dict())
    db.add(nuevo_autor)
    db.commit()
    db.refresh(nuevo_autor)
    return nuevo_autor


# ==============================
# 🟢 Listar autores
# ==============================
@router.get(
    "/",
    response_model=list[schemas.AutorResponse],
    summary="Listar autores",
    description="Muestra todos los autores registrados o filtra por país si se indica."
)
def listar_autores(
        pais: str = Query(None, description="Filtrar autores por país"),
        db: Session = Depends(get_db)
):
    """
    ### Descripción:
    - Lista todos los autores disponibles.
    - Si se pasa el parámetro `pais`, filtra solo los autores de ese país.

    ### Parámetros opcionales:
    - **pais**: nombre del país para filtrar

    ### Respuestas:
    - **200**: Lista de autores
    - **404**: No se encontraron autores
    """
    if pais:
        autores = db.query(models.Autor).filter(models.Autor.pais == pais).all()
    else:
        autores = db.query(models.Autor).all()

    if not autores:
        raise HTTPException(status_code=404, detail="No se encontraron autores.")
    return autores


# ==============================
# 🟢 Obtener autor por ID
# ==============================
@router.get(
    "/{autor_id}",
    response_model=schemas.AutorResponse,
    summary="Obtener un autor por su ID",
    description="Consulta los datos de un autor específico según su identificador único."
)
def obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado.")
    return autor


# ==============================
# 🟡 Actualizar autor
# ==============================
@router.put(
    "/{autor_id}",
    response_model=schemas.AutorResponse,
    summary="Actualizar un autor existente",
    description="Permite modificar los datos de un autor ya registrado."
)
def actualizar_autor(autor_id: int, datos_actualizados: schemas.AutorCreate, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado.")

    for clave, valor in datos_actualizados.dict().items():
        setattr(autor, clave, valor)

    db.commit()
    db.refresh(autor)
    return autor


# ==============================
# 🔴 Eliminar autor
# ==============================
@router.delete(
    "/{autor_id}",
    status_code=400,
    summary="Eliminar un autor",
    description="Elimina un autor **solo si no tiene libros asociados**."
)
def eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado.")

    libros_asociados = db.query(models.Libro).filter(models.Libro.autor_id == autor_id).count()
    if libros_asociados > 0:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede eliminar el autor '{autor.nombre}' porque tiene {libros_asociados} libro(s) asociado(s)."
        )

    db.delete(autor)
    db.commit()
    return {"mensaje": "Autor eliminado correctamente."}
