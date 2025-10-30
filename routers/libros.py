from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter(prefix="/libros", tags=["Libros"])

# Crear un libro
@router.post("/", response_model=schemas.Libro)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    return crud.crear_libro(db, libro)

# Listar todos los libros
@router.get("/", response_model=list[schemas.Libro])
def listar_libros(
    titulo: str | None = Query(None, description="Filtrar por título del libro"),
    isbn: str | None = Query(None, description="Filtrar por ISBN del libro"),
    anio_publicacion: int | None = Query(None, description="Filtrar por año de publicación"),
    db: Session = Depends(get_db)
):
    libros = crud.listar_libros(db)

    # Aplicar filtros si se envían parámetros
    if titulo:
        libros = [l for l in libros if titulo.lower() in l.titulo.lower()]
    if isbn:
        libros = [l for l in libros if isbn.lower() in l.isbn.lower()]
    if anio_publicacion:
        libros = [l for l in libros if l.anio_publicacion == anio_publicacion]

    return libros

# Obtener un libro por su ID
@router.get("/{libro_id}", response_model=schemas.Libro)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = crud.obtener_libro(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

# Actualizar un libro existente
@router.put("/{libro_id}", response_model=schemas.Libro)
def actualizar_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    libro_actualizado = crud.actualizar_libro(db, libro_id, libro)
    if not libro_actualizado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro_actualizado

# Eliminar un libro
@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = crud.eliminar_libro(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"ok": True, "mensaje": "Libro eliminado correctamente"}
