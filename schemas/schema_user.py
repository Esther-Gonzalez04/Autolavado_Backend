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
    password: Optional[str]
    direccion: Optional[str]
    telefono: Optional[str]
    correo: Optional[str]
    estatus: bool
    fecha_registro: datetime
    fecha_modificacion: datatime

class UserCreate(UserBase):
    """
    Esquema para crear usuario.
    """
    pass


class UserUpdate(UserBase):
    """
    Esquema para actualizar usuario.
    """


class UserResponse(UserBase):
    """
    Esquema de respuesta de usuario.
    """
    id: int
    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True


class UserLogin(BaseModel):
    """
    Esquema para login.
    """
    correo: Optional[str] = None
    telefono: Optional[str] = None
    password: str
