'''
    Rutas para la gestión de roles.
'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.model_rols, schemas.schema_rol, crud.crud_rol
from typing import List

rol = APIRouter()

models.model_rols.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    '''
    Función para obtener la sesión de la base de datos.
    '''
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@rol.get("/rol/", response_model=List[schemas.schema_rol.Rol], tags=["Rol"])
async def read_rol(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''
    Endpoint para obtener una lista de roles con paginación.
    '''
    db_rol = crud.crud_rol.get_rol(db=db, skip=skip, limit=limit)
    return db_rol
 