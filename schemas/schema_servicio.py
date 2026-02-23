"""
Módulo de esquemas Pydantic para el modelo Servicio.
Define las estructuras de datos para la validación y respuesta
del catálogo de servicios del autolavado.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Deshabilitamos la advertencia de pocos métodos públicos para clases de datos
# pylint: disable=too-few-public-methods


class ServicioBase(BaseModel):
    """
    Atributos base para un servicio.
    """
    se_nombre: str
    se_descripcion: Optional[str] = None
    se_precio: float
    se_estatus: bool = True
    se_duracion_minutos: int
    us_id: int
    fecha_registro: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None

    # Configuración para permitir lectura desde objetos de base de datos (ORM)
    model_config = ConfigDict(from_attributes=True)


class ServicioCreate(ServicioBase):
    """
    Esquema utilizado para la creación de un nuevo servicio.
    """


class ServicioUpdate(BaseModel):
    """
    Esquema para actualizaciones. Todos los campos son opcionales
    para permitir la modificación de atributos específicos (PATCH).
    """
    se_nombre: Optional[str] = None
    se_descripcion: Optional[str] = None
    se_precio: Optional[float] = None
    se_estatus: Optional[bool] = None
    se_duracion_minutos: Optional[int] = None
    us_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Servicio(ServicioBase):
    """
    Esquema de respuesta que incluye el ID único del servicio.
    """
    se_id: int
