"""
Módulo del modelo Vehiculo para la base de datos.
Define la estructura de la tabla tbb_vehiculo para almacenar 
los automóviles registrados en el sistema del autolavado.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Apagamos temporalmente la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from config.db import Base
# pylint: enable=import-error


# Apagamos la advertencia de "muy pocos métodos públicos" para modelos ORM
# pylint: disable=too-few-public-methods
class Vehiculo(Base):
    """
    Representa la tabla 'tbb_vehiculo' en la base de datos.
    Contiene la información de los vehículos, sus placas, modelos y dueños.
    """
    __tablename__ = "tbb_vehiculo"

    au_id = Column(Integer, primary_key=True, index=True)
    us_id = Column(Integer, ForeignKey("tbb_usuario.id"), nullable=False)
    au_placa = Column(String(15), nullable=False, unique=True)
    au_modelo = Column(String(45), nullable=False)
    au_serie = Column(String(45), nullable=False, unique=True)
    au_color = Column(String(45), nullable=True)
    au_tipo = Column(String(45), nullable=True)
    au_anio = Column(Integer, nullable=True)
    estatus = Column(Boolean, default=True)
    # Manejadas como String según tu lógica del CRUD
    fecha_registro = Column(String(45), nullable=False)
    fecha_modificacion = Column(String(45), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="vehiculos")
    servicios_vehiculo = relationship(
        "ServicioVehiculo", back_populates="vehiculo"
    )
