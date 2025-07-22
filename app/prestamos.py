from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas, models, database, auth

router = APIRouter(
    prefix="/prestamos",
    tags=["prestamos"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.PrestamoOut])
def read_prestamos(skip: int = 0, limit: int = 10,
                   db: Session = Depends(get_db),
                   current_user: models.Usuario = Depends(auth.get_current_user)):
    prestamos = db.query(models.Prestamo).offset(skip).limit(limit).all()
    return prestamos

@router.post("/", response_model=schemas.PrestamoOut)
def create_prestamo(prestamo: schemas.PrestamoCreate,
                    db: Session = Depends(get_db),
                    current_user: models.Usuario = Depends(auth.get_current_user)):
    # Verificar que el libro exista y esté disponible
    libro = db.query(models.Libro).filter(models.Libro.id == prestamo.libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not libro.disponible:
        raise HTTPException(status_code=400, detail="Libro no disponible")

    # Crear préstamo y marcar libro como no disponible
    nuevo_prestamo = models.Prestamo(
        usuario_id=current_user.id,
        libro_id=prestamo.libro_id
    )
    libro.disponible = False

    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)

    return nuevo_prestamo

@router.put("/{prestamo_id}/devolver", response_model=schemas.PrestamoOut)
def devolver_prestamo(prestamo_id: int,
                      db: Session = Depends(get_db),
                      current_user: models.Usuario = Depends(auth.get_current_user)):
    prestamo = db.query(models.Prestamo).filter(models.Prestamo.id == prestamo_id,
                                               models.Prestamo.usuario_id == current_user.id).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if prestamo.fecha_devolucion is not None:
        raise HTTPException(status_code=400, detail="El libro ya fue devuelto")

    prestamo.fecha_devolucion = datetime.utcnow()

    # Marcar el libro como disponible nuevamente
    libro = db.query(models.Libro).filter(models.Libro.id == prestamo.libro_id).first()
    libro.disponible = True

    db.commit()
    db.refresh(prestamo)

    return prestamo