from fastapi import FastAPI
from database import engine, Base
from routers import autores, libros

app = FastAPI(title="Sistema de Gestión de Biblioteca")

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(autores.router)
app.include_router(libros.router)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al sistema de biblioteca"}
