"""
Esquemas Pydantic para Vehiculo.
"""

from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class VehiculoBase(BaseModel):
    """
    Esquema base de Vehiculo.
    """
    au_modelo: str
    au_matricula: str
    au_color: Optional[str]
    au_tipo: Optional[str]
    cl_id: int


class VehiculoCreate(VehiculoBase):
    """
    Esquema para crear vehiculo.
    """


class VehiculoUpdate(VehiculoBase):
    """
    Esquema para actualizar vehiculo.
    """


class VehiculoResponse(VehiculoBase):
    """
    Esquema de respuesta de vehiculo.
    """
    au_id: int

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True
