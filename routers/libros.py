from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=schemas.Libro)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    return crud.crear_libro(db, libro)

@router.get("/", response_model=list[schemas.Libro])
def listar_libros(db: Session = Depends(get_db)):
    return crud.obtener_libros(db)

@router.get("/{libro_id}", response_model=schemas.Libro)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = crud.obtener_libro(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.put("/{libro_id}", response_model=schemas.Libro)
def actualizar_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    return crud.actualizar_libro(db, libro_id, libro)

@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    return crud.eliminar_libro(db, libro_id)
