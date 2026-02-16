"""
Modelo ServicioVehiculo para la base de datos.
"""

# pylint: disable=import-error
# pylint: disable=too-few-public-methods

from sqlalchemy import (Column,Integer,Boolean,ForeignKey,DateTime,Time,Enum)
from sqlalchemy.sql import func
from config.db import Base
from enum import Enum as PyEnum


class Solicitud(PyEnum):
    ''' Enum para definir los estados de la solicitud de servicio. '''
    Programada = "Programada"
    Proceso = "Proceso"
    Realizada = "Realizada"
    Cancelada = "Cancelada"


class ServicioVehiculo(Base):
    """
    Representa la tabla tbd_servicio_vehiculo.
    """
    __tablename__ = "tbd_servicio_vehiculo"

    as_id = Column(Integer, primary_key=True, index=True)

    au_id = Column(Integer, ForeignKey("tbb_vehiculo.au_id"), nullable=False)
    cajero_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)
    operativo_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)
    se_id = Column(Integer, ForeignKey("tbc_servicio.se_id"), nullable=False)
    as_fecha = Column(DateTime, default=func.now())
    as_hora = Column(Time, default=func.now())
    as_estatus = Column(Enum(Solicitud), default=Solicitud.Programada)
    as_estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_modificacion = Column(DateTime)
