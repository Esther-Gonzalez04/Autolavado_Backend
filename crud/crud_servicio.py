'''
    Crud para el modelo de Servicio.
'''
import models.model_servicio
import schemas.schema_servicio
from sqlalchemy.orm import Session

def get_servicio(db: Session, skip: int = 0, limit: int = 10):
    '''
    Obtiene una lista de servicios con paginación.
    '''
    return db.query(models.model_servicio.Servicio).offset(skip).limit(limit).all()
    