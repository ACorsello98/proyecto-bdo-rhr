from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a la base de datos SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Cambia el nombre o ruta si querés

# Crear el engine de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la sesión local (la usaremos para inyectar la sesión en los endpoints)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para crear modelos con SQLAlchemy ORM
Base = declarative_base()

# Función para obtener la sesión DB, para usar en Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()