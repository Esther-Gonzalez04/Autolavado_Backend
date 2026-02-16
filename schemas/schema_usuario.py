"""
    Esquemas Pydantic para Usuario.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class UsuarioBase(BaseModel):
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
    fecha_modificacion: datetime

class UsuarioCreate(UsuarioBase):
    """
    Esquema para crear usuario.
    """
    pass


class UsuarioUpdate(UsuarioBase):
    """
    Esquema para actualizar usuario.
    """


class Usuario(UsuarioBase):
    """
    Esquema de respuesta de usuario.
    """
    id: int
    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True


class UsuarioLogin(BaseModel):
    """
    Esquema para login.
    """
    correo: Optional[str] = None
    telefono: Optional[str] = None
    password: str
