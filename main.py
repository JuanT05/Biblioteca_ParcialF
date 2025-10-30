from fastapi import FastAPI
from database import create_db_and_tables

app = FastAPI(title="Sistema de Gestión de Biblioteca")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al Sistema de Gestión de Biblioteca 📚"}
