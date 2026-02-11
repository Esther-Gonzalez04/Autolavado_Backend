"""
Modelo Servicio para la base de datos.
"""

# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from config.db import Base


class Servicio(Base):
    """
    Representa la tabla tbc_servicio.
    """
    __tablename__ = "tbc_servicio"

    se_id = Column(Integer, primary_key=True, index=True)
    se_nombre = Column(String(80), nullable=False)
    se_descripcion = Column(String(850), nullable=True)
    se_precio = Column(Float, nullable=False)
    se_estatus = Column(Boolean, default=True)

    us_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)

    fecha_registro = Column(DateTime, default=func.now)
    fecha_modificacion = Column(DateTime, onupdate=func.now)
