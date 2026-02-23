"""
Módulo CRUD para la gestión del modelo de Rol.
Contiene las operaciones de base de datos para crear, leer,
actualizar y eliminar roles en el sistema.
"""

from sqlalchemy.orm import Session

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from models import model_rols
from schemas import schema_rol
# pylint: enable=import-error


def get_rol(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene una lista paginada de roles desde la base de datos.
    """
    return db.query(model_rols.Rol).offset(skip).limit(limit).all()


def get_rol_by_nombre(db: Session, nombre_rol: str):
    """
    Busca y retorna un rol específico por su nombre exacto.
    """
    return db.query(model_rols.Rol).filter(
        model_rols.Rol.nombre_rol == nombre_rol
    ).first()


def create_rol(db: Session, rol_in: schema_rol.RolCreate):
    """
    Crea un nuevo rol en la base de datos.
    """
    db_rol = model_rols.Rol(
        nombre_rol=rol_in.nombre_rol,
        estatus=rol_in.estatus,
        fecha_registro=rol_in.fecha_registro,
        fecha_modificacion=rol_in.fecha_modificacion
    )
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol


def update_rol(db: Session, rol_id: int, rol_in: schema_rol.RolUpdate):
    """
    Actualiza los datos de un rol existente mediante su ID.
    Utiliza model_dump de Pydantic V2.
    """
    db_rol = db.query(model_rols.Rol).filter(
        model_rols.Rol.id == rol_id
    ).first()

    if db_rol:
        update_data = rol_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_rol, key, value)

        db.commit()
        db.refresh(db_rol)
    return db_rol


def delete_rol(db: Session, rol_id: int):
    """
    Elimina un rol de la base de datos por su ID.
    """
    db_rol = db.query(model_rols.Rol).filter(
        model_rols.Rol.id == rol_id
    ).first()

    if db_rol:
        db.delete(db_rol)
        db.commit()
    return db_rol
