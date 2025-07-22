from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas, models, database, auth

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Leer libros
@router.get("/", response_model=List[schemas.LibroOut])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    books = db.query(models.Libro).offset(skip).limit(limit).all()
    return books

# Crear libro
@router.post("/", response_model=schemas.LibroOut)
def create_book(book: schemas.LibroCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    db_book = models.Libro(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Actualizar libro
@router.put("/{book_id}", response_model=schemas.LibroOut)
def update_book(book_id: int, book: schemas.LibroCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    db_book = db.query(models.Libro).filter(models.Libro.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    db_book.titulo = book.titulo
    db_book.autor = book.autor
    db.commit()
    db.refresh(db_book)
    return db_book

# Eliminar libro
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    db_book = db.query(models.Libro).filter(models.Libro.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")
    db.delete(db_book)
    db.commit()
    return