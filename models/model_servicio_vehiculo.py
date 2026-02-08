"""
Este módulo define el modelo Autoservicio para la base de datos (r_auto_servicio).
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, Float, Time
from sqlalchemy.sql import func
from config.db import Base


class Autoservicio(Base):
    """
    Clase que representa la tabla tbd_servicio_vehiculo en la base de datos.
    """
    __tablename__ = "tbd_servicio_vehiculo"

    as_id = Column(Integer, primary_key=True, index=True)
    au_id = Column(Integer, ForeignKey("tbc_auto.au_id"))
    se_id = Column(Integer, ForeignKey("tbc_servicio.se_id"))
    us_id = Column(Integer, ForeignKey("tbc_usuario.us_id"))

    # pylint: disable=not-callable
    as_fecha = Column(DateTime, default=func.now())
    as_pagado = Column(Boolean, default=False, nullable=False)
    as_monto = Column(Float, nullable=False)
    as_aprobado = Column(Boolean, default=False, nullable=False)
    as_hora = Column(Time, default=func.now())
