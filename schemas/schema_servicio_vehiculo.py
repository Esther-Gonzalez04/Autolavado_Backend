"""
Esquemas Pydantic para ServicioVehiculo.
"""

from datetime import datetime, time
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class ServicioVehiculoBase(BaseModel):
    """
    Esquema base de ServicioVehiculo.
    """
    au_id: int
    cajero_id: int
    operativo_id: int
    se_id: int
    as_fecha: datetime
    as_hora: time
    as_estatus: str
    as_estado: bool
    fecha_registro: datetime
    fecha_modificacion: datetime


class ServicioVehiculoCreate(ServicioVehiculoBase):
    """
    Esquema para crear servicio de vehiculo.
    """


class ServicioVehiculoResponse(ServicioVehiculoBase):
    """
    Esquema de respuesta de servicio de vehiculo.
    """
    as_id: int
    as_fecha: datetime
    as_hora: time

    class Config:
        '''
        Configuración para permitir la conversión de objetos ORM a modelos Pydantic.
        '''
        orm_mode = True
