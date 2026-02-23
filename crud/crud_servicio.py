"""
Módulo CRUD para la gestión del modelo de Servicio.
Contiene las operaciones de base de datos para crear, leer,
actualizar y eliminar servicios en el catálogo del autolavado.
"""

from sqlalchemy.orm import Session

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from models import model_servicio
from schemas import schema_servicio
# pylint: enable=import-error


def get_servicio(db: Session, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista paginada de servicios desde la base de datos.
    """
    return db.query(model_servicio.Servicio).offset(skip).limit(limit).all()


def get_servicio_by_id(db: Session, se_id: int):
    """
    Busca y retorna un servicio específico por su ID.
    """
    return db.query(model_servicio.Servicio).filter(
        model_servicio.Servicio.se_id == se_id
    ).first()


def get_servicio_by_nombre(db: Session, se_nombre: str):
    """
    Busca y retorna un servicio por su nombre exacto.
    """
    return db.query(model_servicio.Servicio).filter(
        model_servicio.Servicio.se_nombre == se_nombre
    ).first()


def create_servicio(db: Session, servicio_in: schema_servicio.ServicioCreate):
    """
    Crea un nuevo servicio en el catálogo.
    """
    db_servicio = model_servicio.Servicio(
        se_nombre=servicio_in.se_nombre,
        se_descripcion=servicio_in.se_descripcion,
        se_precio=servicio_in.se_precio,
        se_estatus=servicio_in.se_estatus,
        se_duracion_minutos=servicio_in.se_duracion_minutos,
        us_id=servicio_in.us_id
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


def update_servicio(
    db: Session,
    se_id: int,
    servicio_in: schema_servicio.ServicioUpdate
):
    """
    Actualiza los datos de un servicio existente.
    Utiliza model_dump de Pydantic V2.
    """
    db_servicio = db.query(model_servicio.Servicio).filter(
        model_servicio.Servicio.se_id == se_id
    ).first()

    if db_servicio:
        update_data = servicio_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_servicio, key, value)
        db.commit()
        db.refresh(db_servicio)
    return db_servicio


def delete_servicio(db: Session, se_id: int):
    """
    Elimina un servicio del catálogo por su ID.
    """
    db_servicio = db.query(model_servicio.Servicio).filter(
        model_servicio.Servicio.se_id == se_id
    ).first()

    if db_servicio:
        db.delete(db_servicio)
        db.commit()
    return db_servicio
