from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter(prefix="/autores", tags=["Autores"])

# Crear un autor
@router.post("/", response_model=schemas.Autor)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    return crud.crear_autor(db, autor)


# 📍 Listar autores con filtros opcionales
@router.get("/", response_model=list[schemas.Autor])
def listar_autores(
    nombre: str | None = Query(None, description="Filtrar por nombre del autor"),
    pais_origen: str | None = Query(None, description="Filtrar por país de origen"),
    anio_nacimiento: int | None = Query(None, description="Filtrar por año de nacimiento"),
    db: Session = Depends(get_db)
):
    autores = crud.listar_autores(db)

    # Aplicamos filtros si el usuario los envía
    if nombre:
        autores = [a for a in autores if nombre.lower() in a.nombre.lower()]
    if pais_origen:
        autores = [a for a in autores if pais_origen.lower() in a.pais_origen.lower()]
    if anio_nacimiento:
        autores = [a for a in autores if a.anio_nacimiento == anio_nacimiento]

    return autores


# Obtener autor por ID
@router.get("/{autor_id}", response_model=schemas.Autor)
def obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = crud.obtener_autor(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


# Actualizar autor
@router.put("/{autor_id}", response_model=schemas.Autor)
def actualizar_autor(autor_id: int, autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    autor_actualizado = crud.actualizar_autor(db, autor_id, autor)
    if not autor_actualizado:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor_actualizado


# Eliminar autor
@router.delete("/{autor_id}")
def eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = crud.eliminar_autor(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return {"ok": True, "mensaje": "Autor eliminado correctamente"}
