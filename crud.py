from sqlalchemy.orm import Session
import models, schemas

# ----- AUTORES -----
def crear_autor(db: Session, autor: schemas.AutorCreate):
    db_autor = models.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

def listar_autores(db: Session):
    return db.query(models.Autor).all()

def obtener_autor(db: Session, autor_id: int):
    return db.query(models.Autor).filter(models.Autor.id == autor_id).first()

def actualizar_autor(db: Session, autor_id: int, autor_data: schemas.AutorCreate):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if autor:
        for key, value in autor_data.dict().items():
            setattr(autor, key, value)
        db.commit()
        db.refresh(autor)
    return autor

def eliminar_autor(db: Session, autor_id: int):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if autor:
        db.delete(autor)
        db.commit()
    return autor


# ----- LIBROS -----
def crear_libro(db: Session, libro: schemas.LibroCreate):
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def listar_libros(db: Session):
    return db.query(models.Libro).all()

def obtener_libro(db: Session, libro_id: int):
    return db.query(models.Libro).filter(models.Libro.id == libro_id).first()

def actualizar_libro(db: Session, libro_id: int, libro_data: schemas.LibroCreate):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if libro:
        for key, value in libro_data.dict().items():
            setattr(libro, key, value)
        db.commit()
        db.refresh(libro)
    return libro

def eliminar_libro(db: Session, libro_id: int):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if libro:
        db.delete(libro)
        db.commit()
    return libro
