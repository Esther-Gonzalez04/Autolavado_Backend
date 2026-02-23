"""
Módulo del modelo ServicioVehiculo para la base de datos.
Define la estructura de la tabla tbd_servicio_vehiculo y sus relaciones.
"""

from enum import Enum as PyEnum

from sqlalchemy import (
    Column, Integer, Boolean, ForeignKey, DateTime, Time, Enum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from config.db import Base
# pylint: enable=import-error


class Solicitud(PyEnum):
    """
    Enum para definir los estados de la solicitud de servicio.
    Pylint prefiere que las constantes de clase estén en MAYÚSCULAS.
    """
    PROGRAMADA = "Programada"
    PROCESO = "Proceso"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"


# Apagamos la advertencia de "muy pocos métodos públicos" para modelos ORM
# pylint: disable=too-few-public-methods
class ServicioVehiculo(Base):
    """
    Representa la tabla 'tbd_servicio_vehiculo' en la base de datos.
    Registra las asignaciones de servicios a vehículos, operativos y cajeros.
    """
    __tablename__ = "tbd_servicio_vehiculo"

    as_id = Column(Integer, primary_key=True, index=True)

    au_id = Column(Integer, ForeignKey("tbb_vehiculo.au_id"), nullable=False)
    cajero_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)
    operativo_id = Column(
        Integer, ForeignKey("tbb_usuario.id"), nullable=False
    )
    se_id = Column(Integer, ForeignKey("tbc_servicio.se_id"), nullable=False)
    # pylint: disable=not-callable
    as_fecha = Column(DateTime, default=func.now())
    as_hora = Column(Time, default=func.current_time())
    as_estatus = Column(Enum(Solicitud), default=Solicitud.PROGRAMADA)
    as_estado = Column(Boolean)
    fecha_registro = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    # pylint: enable=not-callable
    # Relaciones (divididas en múltiples líneas para respetar los 100 caracteres)
    cajero = relationship(
        "Usuario",
        foreign_keys=[cajero_id],
        back_populates="servicios_cajero"
    )
    operativo = relationship(
        "Usuario",
        foreign_keys=[operativo_id],
        back_populates="servicios_operativo"
    )
    servicio = relationship(
        "Servicio",
        back_populates="servicios_vehiculo"
    )
    vehiculo = relationship(
        "Vehiculo",
        back_populates="servicios_vehiculo"
    )
