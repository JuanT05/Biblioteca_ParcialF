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
