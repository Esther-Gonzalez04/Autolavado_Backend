"""
Módulo del modelo Servicio para la base de datos.
Define la estructura de la tabla tbc_servicio en el catálogo del autolavado.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from config.db import Base
# pylint: enable=import-error


# Apagamos la advertencia de "muy pocos métodos públicos" para modelos ORM
# pylint: disable=too-few-public-methods
class Servicio(Base):
    """
    Representa la tabla 'tbc_servicio' en la base de datos.
    Almacena el catálogo de servicios ofrecidos, precios y duraciones.
    """
    __tablename__ = "tbc_servicio"

    se_id = Column(Integer, primary_key=True, index=True)
    se_nombre = Column(String(80), nullable=False)
    se_descripcion = Column(String(850), nullable=True)
    se_precio = Column(Float, nullable=False)
    se_estatus = Column(Boolean, default=True)
    se_duracion_minutos = Column(Integer, nullable=False)
    # Llave foránea hacia el usuario que registró el servicio
    us_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)
    # pylint: disable=not-callable
    fecha_registro = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    # pylint: enable=not-callable
    # Relaciones
    servicios_vehiculo = relationship(
        "ServicioVehiculo",
        back_populates="servicio"
    )
