from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/autores", tags=["Autores"])


# ==============================
# 🟢 Crear un autor
# ==============================
@router.post("/", response_model=schemas.AutorResponse, status_code=201)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo autor si no existe otro con el mismo nombre.
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
# 🟢 Listar autores (con filtro por país)
# ==============================
@router.get("/", response_model=list[schemas.AutorResponse])
def listar_autores(
        pais: str = Query(None, description="Filtrar autores por país"),
        db: Session = Depends(get_db)
):
    """
    Lista todos los autores o filtra por país si se pasa como parámetro.
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
@router.get("/{autor_id}", response_model=schemas.AutorResponse)
def obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un autor por su ID.
    """
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado.")
    return autor


# ==============================
# 🟡 Actualizar autor
# ==============================
@router.put("/{autor_id}", response_model=schemas.AutorResponse)
def actualizar_autor(autor_id: int, datos_actualizados: schemas.AutorCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un autor existente.
    """
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado.")

    for clave, valor in datos_actualizados.dict().items():
        setattr(autor, clave, valor)

    db.commit()
    db.refresh(autor)
    return autor


# ==============================
# 🔴 Eliminar autor (con lógica de negocio)
# ==============================
@router.delete("/{autor_id}", status_code=400)
def eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    """
    Elimina un autor si no tiene libros asociados.
    """
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
