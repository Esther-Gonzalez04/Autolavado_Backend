"""
Módulo de esquemas Pydantic para el modelo ServicioVehiculo.
Define las estructuras de datos para la validación de entrada y salida
en la asignación de servicios a vehículos.
"""

from datetime import datetime, time
from typing import Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict

# Apagamos la advertencia de "muy pocos métodos públicos"
# pylint: disable=too-few-public-methods


class Solicitud(str, Enum):
    """
    Enum para definir los estados de la solicitud de servicio.
    Se definen en MAYÚSCULAS por convención de constantes y para 
    coincidir con el modelo ORM.
    """
    PROGRAMADA = "Programada"
    PROCESO = "Proceso"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"


class ServicioVehiculoBase(BaseModel):
    """
    Esquema base con los atributos comunes de un ServicioVehiculo.
    """
    au_id: int
    cajero_id: int
    operativo_id: int
    se_id: int
    as_fecha: Optional[datetime] = None
    as_hora: Optional[time] = None
    as_estatus: Optional[Solicitud] = Solicitud.PROGRAMADA
    as_estado: Optional[bool] = True
    fecha_registro: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    # Configuración para permitir la conversión de objetos ORM
    model_config = ConfigDict(from_attributes=True)


class ServicioVehiculoCreate(ServicioVehiculoBase):
    """
    Esquema para la creación de un nuevo registro de ServicioVehiculo.
    (El docstring reemplaza al 'pass' para evitar la advertencia de Pylint)
    """


class ServicioVehiculoUpdate(BaseModel):
    """
    Esquema para la actualización de un registro de ServicioVehiculo.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    au_id: Optional[int] = None
    cajero_id: Optional[int] = None
    operativo_id: Optional[int] = None
    se_id: Optional[int] = None
    as_fecha: Optional[datetime] = None
    as_hora: Optional[time] = None
    as_estatus: Optional[Solicitud] = None
    as_estado: Optional[bool] = None
    fecha_modificacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ServicioVehiculo(ServicioVehiculoBase):
    """
    Esquema de respuesta que representa un ServicioVehiculo desde la BD.
    Incluye el ID autogenerado.
    """
    as_id: int
