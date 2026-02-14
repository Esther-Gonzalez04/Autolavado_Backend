'''
   Crud para el modelo de Vehiculo.
'''
import models.model_vehiculo
import schemas.schema_vehiculo
from sqlalchemy.orm import Session

def get_vehiculo(db: Session, skip: int = 0, limit: int = 10):
    '''
    Obtiene una lista de vehiculos con paginación.
    '''
    return db.query(models.model_vehiculo.Vehiculo).offset(skip).limit(limit).all()
    