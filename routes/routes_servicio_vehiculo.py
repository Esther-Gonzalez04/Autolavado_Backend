'''
    Rutas para la gestión de los servicios de vehiculos
'''

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import config.db, models.model_servicio_vehiculo, schemas.schema_servicio_vehiculo,crud.crud_servicio_vehiculo
from typing import List

servicios_vehiculo = APIRouter()

models.model_servicio_vehiculo.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    '''
    Función para obtener la sesión de la base de datos.
    '''
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@servicios_vehiculo.get("/servicios-vehiculo/", response_model=List[schemas.schema_servicio_vehiculo.ServicioVehiculoBase], tags=["ServicioVehiculo"])
async def read_servicio_vehiculo(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    '''
    Endpoint para obtener una lista de servicios de vehículo con paginación.
    '''
    db_servicio_vehiculo = crud.crud_servicio_vehiculo.get_servicio_vehiculo(db=db, skip=skip, limit=limit)
    return db_servicio_vehiculo
 