from sqlmodel import Session, select
from models import Autor
from typing import List

# Crear autor
def crear_autor(session: Session, autor: Autor) -> Autor:
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor

# Listar autores (opcional filtro por país)
def listar_autores(session: Session, pais: str = None) -> List[Autor]:
    query = select(Autor)
    if pais:
        query = query.where(Autor.pais_origen == pais)
    autores = session.exec(query).all()
    return autores
