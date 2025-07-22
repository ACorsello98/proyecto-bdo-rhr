from fastapi import FastAPI
from . import models
from .database import engine
from . import auth
from . import books
from . import prestamos  # Importar el módulo prestamos

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(prestamos.router)  # Incluir el router de préstamos

@app.get("/")
def leer_root():
    return {"mensaje": "api ok"}