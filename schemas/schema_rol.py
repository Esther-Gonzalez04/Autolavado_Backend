"""
Esquemas Pydantic para Rol.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class RolBase(BaseModel):
    """
    Esquema base de Rol.
    """
    nombre_rol: str
    estatus: bool
    fecha_registro: datetime
    fecha_modificacion: datetime


class RolCreate(RolBase):
    """
    Esquema para crear rol.
    """


class RolUpdate(RolBase):
    """
    Esquema para actualizar rol.
    """


class Rol(RolBase):
    """
    Esquema de respuesta de rol.
    """
    id: int

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True
