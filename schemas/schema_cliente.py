"""
Esquemas Pydantic para Cliente.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class ClienteBase(BaseModel):
    """
    Esquema base de Cliente.
    """
    cl_nombre: str
    cl_apellido_paterno: str
    cl_apellido_materno: Optional[str]
    cl_direccion: Optional[str]
    cl_email: Optional[str]
    cl_telefono: Optional[str]
    cl_estatus: bool


class ClienteCreate(ClienteBase):
    """
    Esquema para crear cliente.
    """
    cl_password: str


class ClienteUpdate(ClienteBase):
    """
    Esquema para actualizar cliente.
    """


class ClienteResponse(ClienteBase):
    """
    Esquema de respuesta de cliente.
    """
    cl_id: int
    cl_fecha_registro: datetime
    cl_fecha_modificacion: Optional[datetime]

    class Config:
        """
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        """
        orm_mode = True
