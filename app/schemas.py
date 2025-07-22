from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Usuario - Para crear usuario
class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str

# Usuario - Para devolver usuario (sin password)
class UsuarioOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # si usas Pydantic v2 (sino: orm_mode = True)

# Libro - base para creación y uso común
class LibroBase(BaseModel):
    titulo: str
    autor: str

# Libro - creación
class LibroCreate(LibroBase):
    pass

# Libro - respuesta con id y estado disponibilidad
class LibroOut(LibroBase):
    id: int
    disponible: bool

    class Config:
        from_attributes = True

# Prestamo - para crear préstamo (solo libro_id necesario)
class PrestamoCreate(BaseModel):
    libro_id: int

# Prestamo - para mostrar préstamo completo
class PrestamoOut(BaseModel):
    id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: datetime
    fecha_devolucion: Optional[datetime] = None

    class Config:
        from_attributes = True