"""
Módulo de esquemas Pydantic para el modelo Vehículo.
Define las reglas de validación para el registro, actualización
y consulta de los automóviles en el sistema de autolavado.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Deshabilitamos la advertencia de pocos métodos públicos para clases de datos
# pylint: disable=too-few-public-methods


class VehiculoBase(BaseModel):
    """
    Atributos base compartidos para la gestión de vehículos.
    """
    au_placa: str
    au_modelo: str
    au_serie: str
    au_color: Optional[str] = None
    au_tipo: Optional[str] = None
    au_anio: Optional[int] = None
    estatus: bool = True
    fecha_registro: datetime
    fecha_modificacion: Optional[datetime] = None

    # Configuración de Pydantic V2 para compatibilidad con SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class VehiculoCreate(VehiculoBase):
    """
    Esquema utilizado para el registro de un nuevo vehículo.
    """


class VehiculoUpdate(BaseModel):
    """
    Campos opcionales para permitir la actualización parcial (PATCH)
    de la información de un vehículo.
    """
    au_placa: Optional[str] = None
    au_modelo: Optional[str] = None
    au_serie: Optional[str] = None
    au_color: Optional[str] = None
    au_tipo: Optional[str] = None
    au_anio: Optional[int] = None
    estatus: Optional[bool] = None
    fecha_modificacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Vehiculo(VehiculoBase):
    """
    Esquema de respuesta final que incluye los IDs relacionales.
    Coincide con la referencia usada en Rutas y CRUD.
    """
    au_id: int
    us_id: int
