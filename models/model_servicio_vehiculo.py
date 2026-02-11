"""
Modelo ServicioVehiculo para la base de datos.
"""

# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
    DateTime,
    Float,
    Time,
)
from sqlalchemy.sql import func
from config.db import Base


class ServicioVehiculo(Base):
    """
    Representa la tabla tbd_servicio_vehiculo.
    """
    __tablename__ = "tbd_servicio_vehiculo"

    as_id = Column(Integer, primary_key=True, index=True)

    au_id = Column(Integer, ForeignKey("tbb_vehiculo.au_id"), nullable=False)
    se_id = Column(Integer, ForeignKey("tbc_servicio.se_id"), nullable=False)
    us_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)

    as_fecha = Column(DateTime, default=func.now)
    as_hora = Column(Time, default=func.now)
    as_pagado = Column(Boolean, default=False)
    as_aprobado = Column(Boolean, default=False)
    as_monto = Column(Float, nullable=False)
