"""
Módulo de esquemas Pydantic para el modelo Usuario.
Gestiona la validación de datos para registro, actualización, 
autenticación y visualización de perfiles, garantizando la seguridad
al no exponer credenciales en las respuestas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Deshabilitamos la advertencia de pocos métodos públicos para clases de datos
# pylint: disable=too-few-public-methods


class UsuarioBase(BaseModel):
    """
    Atributos básicos del usuario compartidos en la mayoría de los esquemas.
    """
    rol_id: int
    nombre: str
    papellido: str
    sapellido: Optional[str] = None
    usuario: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    estatus: bool = True

    # Configuración para permitir lectura desde objetos ORM
    model_config = ConfigDict(from_attributes=True)


class UsuarioCreate(UsuarioBase):
    """
    Esquema para el registro de nuevos usuarios.
    Incluye el campo password, el cual será hasheado en el CRUD.
    """
    password: str


class UsuarioUpdate(BaseModel):
    """
    Esquema para actualizaciones parciales. 
    Todos los campos son opcionales para permitir cambios específicos.
    """
    rol_id: Optional[int] = None
    nombre: Optional[str] = None
    papellido: Optional[str] = None
    sapellido: Optional[str] = None
    usuario: Optional[str] = None
    password: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    estatus: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class Usuario(UsuarioBase):
    """
    Esquema de respuesta principal. 
    IMPORTANTE: No hereda ni incluye el campo 'password' por seguridad.
    """
    id: int
    fecha_registro: Optional[datetime] = None
    fecha_modificacion: Optional[datetime] = None


class UsuarioLogin(BaseModel):
    """
    Esquema simplificado para el proceso de inicio de sesión.
    """
    correo: Optional[str] = None
    telefono: Optional[str] = None
    password: str
