"""
Módulo CRUD para la gestión del modelo de Vehiculo.
Contiene las operaciones de base de datos para crear, leer,
actualizar y eliminar vehículos asociados a los usuarios.
"""

from datetime import datetime
from sqlalchemy.orm import Session

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from models import model_vehiculo
from schemas import schema_vehiculo
# pylint: enable=import-error


def get_vehiculo(db: Session, skip: int = 0, limit: int = 10):
    """
    Obtiene una lista paginada de vehículos desde la base de datos.
    """
    return db.query(model_vehiculo.Vehiculo).offset(skip).limit(limit).all()


def get_vehiculo_by_id(db: Session, au_id: int):
    """
    Busca y retorna un vehículo específico por su ID (au_id).
    """
    return db.query(model_vehiculo.Vehiculo).filter(
        model_vehiculo.Vehiculo.au_id == au_id
    ).first()


def get_vehiculo_by_placa(db: Session, au_placa: str):
    """
    Busca y retorna un vehículo por su número de placa.
    """
    return db.query(model_vehiculo.Vehiculo).filter(
        model_vehiculo.Vehiculo.au_placa == au_placa
    ).first()


def create_vehiculo(
    db: Session,
    vehiculo_in: schema_vehiculo.VehiculoCreate,
    us_id: int
):
    """
    Crea un nuevo vehículo en la base de datos.
    Convierte el formato datetime a string según los requisitos del modelo.
    """
    # Convertir datetime a string como pide el modelo antes de asignarlo
    fecha_str = vehiculo_in.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")

    db_vehiculo = model_vehiculo.Vehiculo(
        us_id=us_id,
        au_placa=vehiculo_in.au_placa,
        au_modelo=vehiculo_in.au_modelo,
        au_serie=vehiculo_in.au_serie,
        au_color=vehiculo_in.au_color,
        au_tipo=vehiculo_in.au_tipo,
        au_anio=vehiculo_in.au_anio,
        estatus=vehiculo_in.estatus,
        fecha_registro=fecha_str
    )
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo


def update_vehiculo(
    db: Session,
    au_id: int,
    vehiculo_in: schema_vehiculo.VehiculoUpdate
):
    """
    Actualiza los datos de un vehículo existente.
    Utiliza model_dump de Pydantic V2 e incluye parseo de datetime.
    """
    db_vehiculo = db.query(model_vehiculo.Vehiculo).filter(
        model_vehiculo.Vehiculo.au_id == au_id
    ).first()

    if db_vehiculo:
        update_data = vehiculo_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Si el valor es datetime, convertir a string para el modelo
            if isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            setattr(db_vehiculo, key, value)
        db.commit()
        db.refresh(db_vehiculo)
    return db_vehiculo


def delete_vehiculo(db: Session, au_id: int):
    """
    Elimina un vehículo de la base de datos por su ID.
    """
    db_vehiculo = db.query(model_vehiculo.Vehiculo).filter(
        model_vehiculo.Vehiculo.au_id == au_id
    ).first()

    if db_vehiculo:
        db.delete(db_vehiculo)
        db.commit()
    return db_vehiculo
