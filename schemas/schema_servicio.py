"""
Esquemas Pydantic para Servicio.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class ServicioBase(BaseModel):
    """
    Esquema base de Servicio.
    """
    se_nombre: str
    se_descripcion: Optional[str]
    se_precio: float
    se_estatus: bool
    se_duracion_minutos: int
    us_id: int
    fecha_registro: datetime
    fecha_modificacion: datetime


class ServicioCreate(ServicioBase):
    """
    Esquema para crear servicio.
    """


class ServicioUpdate(ServicioBase):
    """
    Esquema para actualizar servicio.
    """


class ServicioResponse(ServicioBase):
    """
    Esquema de respuesta de servicio.
    """
    se_id: int

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True
