from fastapi import FastAPI
from routers import autores, libros
from database import Base, engine

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Biblioteca",
    version="0.1.0",
    description="API para gestionar autores y libros"
)

# Rutas principales
app.include_router(autores.router)
app.include_router(libros.router)

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al sistema de gestión de biblioteca"}
