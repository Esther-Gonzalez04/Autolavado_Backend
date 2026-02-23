"""
Módulo CRUD para la gestión del modelo de ServicioVehiculo.
Contiene las operaciones de base de datos para crear, leer,
actualizar y eliminar el registro de servicios aplicados a vehículos.
"""

from sqlalchemy.orm import Session

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from models import model_servicio_vehiculo
from schemas import schema_servicio_vehiculo
# pylint: enable=import-error


def get_servicio_vehiculo(db: Session, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista paginada del historial de servicios de vehículos.
    """
    return db.query(
        model_servicio_vehiculo.ServicioVehiculo
    ).offset(skip).limit(limit).all()


def get_servicio_vehiculo_by_id(db: Session, as_id: int):
    """
    Busca y retorna un registro de servicio de vehículo por su ID (as_id).
    """
    return db.query(model_servicio_vehiculo.ServicioVehiculo).filter(
        model_servicio_vehiculo.ServicioVehiculo.as_id == as_id
    ).first()


def create_servicio_vehiculo(
    db: Session,
    servicio_in: schema_servicio_vehiculo.ServicioVehiculoCreate
):
    """
    Crea un nuevo registro de servicio de vehículo en la base de datos.
    """
    db_servicio = model_servicio_vehiculo.ServicioVehiculo(
        au_id=servicio_in.au_id,
        cajero_id=servicio_in.cajero_id,
        operativo_id=servicio_in.operativo_id,
        se_id=servicio_in.se_id,
        as_fecha=servicio_in.as_fecha,
        as_hora=servicio_in.as_hora,
        as_estatus=servicio_in.as_estatus,
        as_estado=servicio_in.as_estado
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


def update_servicio_vehiculo(
    db: Session,
    as_id: int,
    servicio_in: schema_servicio_vehiculo.ServicioVehiculoUpdate
):
    """
    Actualiza los datos de un registro de servicio de vehículo.
    Utiliza model_dump de Pydantic V2 para la extracción de datos.
    """
    db_servicio = db.query(model_servicio_vehiculo.ServicioVehiculo).filter(
        model_servicio_vehiculo.ServicioVehiculo.as_id == as_id
    ).first()

    if db_servicio:
        update_data = servicio_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_servicio, key, value)
        db.commit()
        db.refresh(db_servicio)
    return db_servicio


def delete_servicio_vehiculo(db: Session, as_id: int):
    """
    Elimina un registro de servicio de vehículo por su ID.
    """
    db_servicio = db.query(model_servicio_vehiculo.ServicioVehiculo).filter(
        model_servicio_vehiculo.ServicioVehiculo.as_id == as_id
    ).first()

    if db_servicio:
        db.delete(db_servicio)
        db.commit()
    return db_servicio
