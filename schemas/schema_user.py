"""
    Esquemas Pydantic para Usuario.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class UserBase(BaseModel):
    """
    Esquema base de Usuario.
    """
    rol_id: int
    nombre: str
    papellido: str
    sapellido: Optional[str]
    usuario: str
    direccion: Optional[str]
    telefono: Optional[str]
    correo: Optional[str]
    estatus: bool


class UserCreate(UserBase):
    """
    Esquema para crear usuario.
    """
    password: str


class UserUpdate(UserBase):
    """
    Esquema para actualizar usuario.
    """


class UserResponse(UserBase):
    """
    Esquema de respuesta de usuario.
    """
    id: int
    fecha_registro: datetime
    fecha_modificacion: Optional[datetime]

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True


class UserLogin(BaseModel):
    """
    Esquema para login.
    """
    correo: Optional[str]
    telefono: Optional[str]
    password: str
