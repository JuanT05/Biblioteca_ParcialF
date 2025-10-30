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


from models import Libro, Autor, AutorLibro
from sqlmodel import select
from typing import List, Optional

# --------------------------
# CRUD DE LIBROS
# --------------------------

# Crear libro (con autores)
def crear_libro(session: Session, libro: Libro, autores_ids: Optional[List[int]] = None) -> Libro:
    # Validar que el ISBN sea único
    existe = session.exec(select(Libro).where(Libro.isbn == libro.isbn)).first()
    if existe:
        raise ValueError("Ya existe un libro con ese ISBN.")

    session.add(libro)
    session.commit()
    session.refresh(libro)

    # Asignar autores si se envían IDs
    if autores_ids:
        for autor_id in autores_ids:
            autor = session.get(Autor, autor_id)
            if autor:
                relacion = AutorLibro(autor_id=autor.id, libro_id=libro.id)
                session.add(relacion)
        session.commit()

    session.refresh(libro)
    return libro


# Listar libros (opcional filtro por año)
def listar_libros(session: Session, anio: int = None) -> List[Libro]:
    query = select(Libro)
    if anio:
        query = query.where(Libro.anio_publicacion == anio)
    return session.exec(query).all()


# Obtener libro con sus autores
def obtener_libro(session: Session, libro_id: int) -> Optional[Libro]:
    return session.get(Libro, libro_id)


# Actualizar libro
def actualizar_libro(session: Session, libro_id: int, datos: dict) -> Optional[Libro]:
    libro = session.get(Libro, libro_id)
    if not libro:
        return None

    for clave, valor in datos.items():
        setattr(libro, clave, valor)

    # Validar que las copias no sean negativas
    if libro.copias_disponibles < 0:
        raise ValueError("El número de copias no puede ser negativo.")

    session.add(libro)
    session.commit()
    session.refresh(libro)
    return libro


# Eliminar libro
def eliminar_libro(session: Session, libro_id: int) -> bool:
    libro = session.get(Libro, libro_id)
    if not libro:
        return False
    session.delete(libro)
    session.commit()
    return True
