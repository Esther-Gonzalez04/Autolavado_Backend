"""
Módulo de esquemas Pydantic para el modelo Rol.
Define las estructuras de datos para la validación de entrada y salida
en los endpoints de la API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# En los esquemas de Pydantic es normal no tener métodos públicos,
# ya que actúan únicamente como estructuras de validación de datos.
# pylint: disable=too-few-public-methods


class RolBase(BaseModel):
    """
    Esquema base con los atributos comunes de un Rol.
    """
    nombre_rol: str
    estatus: bool
    fecha_registro: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None


class RolCreate(RolBase):
    """
    Esquema para la creación de un nuevo rol.
    Hereda de RolBase sin añadir campos obligatorios extra.
    """


class RolUpdate(RolBase):
    """
    Esquema para la actualización de un rol existente.
    """


class Rol(RolBase):
    """
    Esquema de respuesta que representa un rol proveniente de la base de datos.
    Incluye el ID autogenerado.
    """
    id: int

    # Configuración de Pydantic V2 para leer objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
