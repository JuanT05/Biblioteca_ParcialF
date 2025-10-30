from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from database import create_db_and_tables, get_session
from models import Autor
from schemas import AutorCreate, AutorRead
from crud import crear_autor, listar_autores
from typing import List

app = FastAPI(title="Sistema de Gestión de Biblioteca")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al Sistema de Gestión de Biblioteca 📚"}

from crud import obtener_autor, actualizar_autor, eliminar_autor

# Obtener autor y sus libros
@app.get("/autores/{autor_id}", response_model=AutorRead)
def obtener_autor_endpoint(autor_id: int, session: Session = Depends(get_session)):
    autor = obtener_autor(session, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


# Actualizar autor
@app.put("/autores/{autor_id}", response_model=AutorRead)
def actualizar_autor_endpoint(autor_id: int, datos: dict, session: Session = Depends(get_session)):
    autor = actualizar_autor(session, autor_id, datos)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


# Eliminar autor
@app.delete("/autores/{autor_id}")
def eliminar_autor_endpoint(autor_id: int, session: Session = Depends(get_session)):
    ok = eliminar_autor(session, autor_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return {"mensaje": "Autor eliminado correctamente"}



# -------------------------
# ENDPOINTS DE AUTORES
# -------------------------

@app.post("/autores/", response_model=AutorRead)
def crear_autor_endpoint(autor: AutorCreate, session: Session = Depends(get_session)):
    nuevo_autor = Autor.from_orm(autor)
    return crear_autor(session, nuevo_autor)


@app.get("/autores/", response_model=List[AutorRead])
def listar_autores_endpoint(pais: str | None = None, session: Session = Depends(get_session)):
    autores = listar_autores(session, pais)
    return autores

from models import Libro
from schemas import LibroCreate, LibroRead
from crud import crear_libro, listar_libros, obtener_libro, actualizar_libro, eliminar_libro

# -------------------------
# ENDPOINTS DE LIBROS
# -------------------------

@app.post("/libros/", response_model=LibroRead)
def crear_libro_endpoint(libro_data: LibroCreate, session: Session = Depends(get_session)):
    nuevo_libro = Libro(
        titulo=libro_data.titulo,
        isbn=libro_data.isbn,
        anio_publicacion=libro_data.anio_publicacion,
        copias_disponibles=libro_data.copias_disponibles
    )
    try:
        libro_creado = crear_libro(session, nuevo_libro, libro_data.autores_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return libro_creado


@app.get("/libros/", response_model=List[LibroRead])
def listar_libros_endpoint(anio: int | None = None, session: Session = Depends(get_session)):
    return listar_libros(session, anio)


@app.get("/libros/{libro_id}", response_model=LibroRead)
def obtener_libro_endpoint(libro_id: int, session: Session = Depends(get_session)):
    libro = obtener_libro(session, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@app.put("/libros/{libro_id}", response_model=LibroRead)
def actualizar_libro_endpoint(libro_id: int, datos: dict, session: Session = Depends(get_session)):
    try:
        libro = actualizar_libro(session, libro_id, datos)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/libros/{libro_id}")
def eliminar_libro_endpoint(libro_id: int, session: Session = Depends(get_session)):
    ok = eliminar_libro(session, libro_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"mensaje": "Libro eliminado correctamente"}
