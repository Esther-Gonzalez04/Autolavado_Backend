"""
Módulo del modelo Usuario para la base de datos.
Define la estructura de la tabla tbb_usuario, gestionando
credenciales, información personal y roles de los usuarios del autolavado.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# pylint: disable=import-error
from config.db import Base
# pylint: enable=import-error


# pylint: disable=too-few-public-methods
class Usuario(Base):
    """
    Representa la tabla 'tbb_usuario' en la base de datos.
    Contiene la información del personal y clientes registrados en el sistema.
    """
    __tablename__ = "tbb_usuario"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("tbc_roles.id"), nullable=False)

    nombre = Column(String(60), nullable=False)
    papellido = Column(String(60), nullable=False)
    sapellido = Column(String(60), nullable=True)
    usuario = Column(String(60), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    direccion = Column(String(100), nullable=True)
    telefono = Column(String(15), nullable=True, unique=True)
    correo = Column(String(100), nullable=True, unique=True)

    estatus = Column(Boolean, default=True)
    # pylint: disable=not-callable
    # Se agregó el espacio faltante después de DateTime
    fecha_registro = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(DateTime, onupdate=func.now())
    # pylint: enable=not-callable
    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    vehiculos = relationship("Vehiculo", back_populates="usuario")
    # Relaciones con ServicioVehiculo (divididas para respetar los 100 caracteres)
    servicios_cajero = relationship(
        "ServicioVehiculo",
        foreign_keys="[ServicioVehiculo.cajero_id]",
        back_populates="cajero"
    )
    servicios_operativo = relationship(
        "ServicioVehiculo",
        foreign_keys="[ServicioVehiculo.operativo_id]",
        back_populates="operativo"
    )
