"""
Modelo Cliente para la base de datos.
"""

# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from config.db import Base


class Cliente(Base):
    """
    Representa la tabla tbc_cliente.
    """
    __tablename__ = "tbc_cliente"

    cl_id = Column(Integer, primary_key=True, index=True)
    cl_nombre = Column(String(60), nullable=False)
    cl_apellido_paterno = Column(String(60), nullable=False)
    cl_apellido_materno = Column(String(60), nullable=True)
    cl_direccion = Column(String(255), nullable=True)
    cl_email = Column(String(100), nullable=True, unique=True)
    cl_telefono = Column(String(15), nullable=True)
    cl_password = Column(String(255), nullable=False)
    cl_estatus = Column(Boolean, default=True)
    cl_fecha_registro = Column(DateTime, default=func.now)
    cl_fecha_modificacion = Column(DateTime, onupdate=func.now)
