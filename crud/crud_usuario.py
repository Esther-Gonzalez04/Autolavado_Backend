'''
    Crud para el modelo de Usuario.
'''
import models.model_usuario
import schemas.schema_usuario
from sqlalchemy.orm import Session

def get_usuario(db: Session, skip: int = 0, limit: int = 10):
    '''
    Obtiene una lista de usuarios con paginación.
    '''
    return db.query(models.model_usuario.Usuario).offset(skip).limit(limit).all()
    