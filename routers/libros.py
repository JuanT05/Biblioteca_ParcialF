from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(prefix="/libros", tags=["Libros"])


# ==============================
# 🟢 Crear un libro
# ==============================
@router.post("/", response_model=schemas.LibroResponse, status_code=201)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo libro si no existe otro con el mismo ISBN.
    """
    # Verificar autor existente
    autor = db.query(models.Autor).filter(models.Autor.id == libro.autor_id).first()
    if not autor:
        raise HTTPException(status_code=404, detail="El autor asociado no existe.")

    # Verificar ISBN duplicado
    libro_existente = db.query(models.Libro).filter(models.Libro.isbn == libro.isbn).first()
    if libro_existente:
        raise HTTPException(status_code=409, detail="Ya existe un libro con ese ISBN.")

    nuevo_libro = models.Libro(**libro.dict())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro


# ==============================
# 🟢 Listar libros (con filtro por año)
# ==============================
@router.get("/", response_model=list[schemas.LibroResponse])
def listar_libros(
        anio: int = Query(None, description="Filtrar libros por año de publicación"),
        db: Session = Depends(get_db)
):
    """
    Lista todos los libros o los filtra por año si se indica.
    """
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
@router.get("/{libro_id}", response_model=schemas.LibroResponse)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un libro por su ID.
    """
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    return libro


# ==============================
# 🟡 Actualizar libro
# ==============================
@router.put("/{libro_id}", response_model=schemas.LibroResponse)
def actualizar_libro(libro_id: int, datos_actualizados: schemas.LibroCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un libro existente.
    """
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    # Evitar duplicar ISBN con otro libro
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
@router.delete("/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    """
    Elimina un libro por su ID.
    """
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")

    db.delete(libro)
    db.commit()
    return {"mensaje": "Libro eliminado correctamente."}
