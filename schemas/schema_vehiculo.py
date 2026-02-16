"""
Esquemas Pydantic para Vehiculo.
"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# pylint: disable=too-few-public-methods
class VehiculoBase(BaseModel):
    """
    Esquema base de Vehiculo.
    """
    au_placa: str
    au_modelo: str
    au_serie: str
    au_color: str
    au_tipo: str
    au_anio: int
    estatus: bool
    fecha_registro: datetime
    fecha_modificacion: datetime


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
