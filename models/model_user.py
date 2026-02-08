"""
Esta clase se encarga de crear la tabla de usuarios en la base de datos,
con sus respectivos campos y tipos de datos.
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base


class User(Base):
    """
    Clase que representa la tabla de usuarios en la base de datos.
    """
    __tablename__ = "tbb_usuario"

    id = Column(Integer, primary_key=True, index=True)
    # Asegúrate de que la tabla 'tbc_roles' exista y tenga un campo 'id'
    rol_id = Column(Integer, ForeignKey("tbc_roles.id"))
    nombre = Column(String(60), nullable=True)
    papellido = Column(String(60), nullable=True)
    sapellido = Column(String(60), nullable=True)
    usuario = Column(String(60), nullable=True, unique=True)
    password = Column(String(100), nullable=True)
    direccion = Column(String(100), nullable=True)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    estatus = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, nullable=True)
    fecha_modificacion = Column(DateTime, nullable=True)
