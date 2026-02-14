"""
Modelo Rol para la base de datos.
"""

# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from config.db import Base


class Rol(Base):
    """
    Representa la tabla tbc_roles.
    """
    __tablename__ = "tbc_roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(60), nullable=False, unique=True)
    estatus = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=func.now)
    fecha_modificacion = Column(DateTime, onupdate=func.now)
