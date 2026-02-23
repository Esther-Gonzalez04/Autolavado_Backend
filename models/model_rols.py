"""
Módulo del modelo Rol para la base de datos.
Define la estructura de la tabla tbc_roles.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Apagamos la advertencia de importación para las carpetas locales
# pylint: disable=import-error
from config.db import Base
# pylint: enable=import-error


# Apagamos la advertencia de "muy pocos métodos públicos" porque
# los modelos ORM actúan como estructuras de datos, no como clases lógicas.
# pylint: disable=too-few-public-methods
class Rol(Base):
    """
    Representa la tabla 'tbc_roles' en la base de datos.
    Contiene la definición de los diferentes roles del sistema.
    """
    __tablename__ = "tbc_roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(60), nullable=False, unique=True)
    estatus = Column(Boolean, default=True)
    # Se recomienda usar func.now() con paréntesis en SQLAlchemy
    # pylint: disable=not-callable
    fecha_registro = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, onupdate=func.now())
    # pylint: enable=not-callable
    usuarios = relationship("Usuario", back_populates="rol")
