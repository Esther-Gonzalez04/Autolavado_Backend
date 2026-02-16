'''
    Rutas para la gestión de Usuarios
'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.model_usuario, schemas.schema_usuario, crud.crud_usuario
from typing import List

usuario = APIRouter()

models.model_usuario.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    '''
    Función para obtener la sesión de la base de datos.
    '''
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@usuario.get("/usuario/", response_model=List[schemas.schema_usuario.Usuario], tags=["Usuario"])
async def read_usuario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''
    Endpoint para obtener una lista de usuarios con paginación.
    '''
    db_usuario = crud.crud_usuario.get_usuario(db=db, skip=skip, limit=limit)
    return db_usuario
