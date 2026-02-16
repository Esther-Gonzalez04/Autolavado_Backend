'''
    Rutas para la gestión de servicios 
'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.model_servicio, schemas.schema_servicio, crud.crud_servicio
from typing import List

servicio = APIRouter()

models.model_servicio.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    '''
    Función para obtener la sesión de la base de datos.
    '''
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@servicio.get("/servicios/", response_model=List[schemas.schema_servicio.ServicioBase], tags=["Servicio"])
async def read_servicio(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''
    Endpoint para obtener una lista de servicios con paginación.
    '''
    db_servicio = crud.crud_servicio.get_servicio(db=db, skip=skip, limit=limit)
    return db_servicio
 