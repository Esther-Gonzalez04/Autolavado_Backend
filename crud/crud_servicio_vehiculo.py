'''
    Crud para el modelo de ServicioVehiculo.
'''
import models.model_servicio_vehiculo
import schemas.schema_servicio_vehiculo
from sqlalchemy.orm import Session

def get_servicio_vehiculo(db: Session, skip: int = 0, limit: int = 10):
    '''
    Obtiene una lista de servicios de vehiculo con paginación.
    '''
    return db.query(models.model_servicio_vehiculo.ServicioVehiculo).offset(skip).limit(limit).all()
    