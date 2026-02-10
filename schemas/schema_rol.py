"""
Esquema para el rol de usuario
"""

from datetime import datetime
from pydantic import BaseModel

# pylint: disable=too-few-public-methods


class RolBase(BaseModel):
    """Clase base para el esquema de rol"""

    nombre: str
    estatus: bool
    fecha_registro: datetime
    fecha_modificacion: datetime


class RolCreate(RolBase):
    """Se utiliza para crear un nuevo rol"""


class RolUpdate(RolBase):
    """Se utiliza para actualizar un rol existente"""


class Rol(RolBase):
    """Representa un rol en la respuesta de la API"""

    id: int

    class Config:
        """Permite convertir objetos ORM a modelos Pydantic"""

        orm_mode = True
