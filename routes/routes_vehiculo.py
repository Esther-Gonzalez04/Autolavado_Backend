'''
    Rutas para la gestión de Vehiculos
'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.model_vehiculo, schemas.schema_vehiculo, crud.crud_vehiculo
from typing import List

vehiculo= APIRouter()

models.model_vehiculo.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    '''
    Función para obtener la sesión de la base de datos.
    '''
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@vehiculo.get("/vehiculo/", response_model=List[schemas.schema_vehiculo.VehiculoBase], tags=["Vehiculo"])
async def read_rol(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''
    Endpoint para obtener una lista de vehiculos con paginación.
    '''
    db_vehiculo = crud.crud_vehiculo.get_vehiculo(db=db, skip=skip, limit=limit)
    return db_vehiculo
