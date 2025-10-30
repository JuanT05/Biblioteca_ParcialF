from sqlalchemy import Column, Integer, String
from database import Base

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    pais_origen = Column(String)
    anio_nacimiento = Column(Integer)

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    anio_publicacion = Column(Integer)
    copias_disponibles = Column(Integer)
