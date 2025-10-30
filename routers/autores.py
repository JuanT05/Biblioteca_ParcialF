from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", response_model=schemas.Autor)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    return crud.crear_autor(db, autor)

@router.get("/", response_model=list[schemas.Autor])
def listar_autores(db: Session = Depends(get_db)):
    return crud.obtener_autores(db)

@router.get("/{autor_id}", response_model=schemas.Autor)
def obtener_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = crud.obtener_autor(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.put("/{autor_id}", response_model=schemas.Autor)
def actualizar_autor(autor_id: int, autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    return crud.actualizar_autor(db, autor_id, autor)

@router.delete("/{autor_id}")
def eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    return crud.eliminar_autor(db, autor_id)
