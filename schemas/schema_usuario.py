'''
    Docstring for the schema_user module.
'''
from datetime import datetime as datatime
from typing import Optional as optional

from pydantic import BaseModel

class UserBase(BaseModel):
    '''Clase base para el esquema de usuario'''
    nombre: str
    papellido: str
    sapellido: str
    direccion: str
    correo: str
    telefono: str
    contrasena: str
    estatus: bool
    fecha_registro: datatime
    fecha_modificacion: datatime

#pylint: disable=too-few-public-methods
class UserCreate(UserBase):
    '''Esta clase se utiliza para crear un nuevo usuario'''

class UserUpdate(UserBase):
    '''Esta clase se utiliza para actualizar un usuario existente'''

class User(UserBase):
    '''Esta clase se utiliza para representar un usuario en la respuesta de la API'''
    id: int
    class Config:
        '''Configuración para permitir la conversión de objetos ORM a modelos Pydantic'''
        orm_mode = True

class UserLogin(BaseModel):
    '''Clase para el esquema de inicio de sesión de usuario'''
    telefono: optional[str] = None
    correo: optional[str] = None
    contrasena: str
