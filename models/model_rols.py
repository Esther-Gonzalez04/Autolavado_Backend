"""
Esta clase se encarga de crear la tabla de roles en la base de datos,
con sus respectivos campos y tipos de datos.
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base


class Rol(Base):
    """
    Clase que representa la tabla de roles en la base de datos.
    """
    __tablename__ = "tbc_roles"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(60), nullable=True)
    estatus = Column(Boolean, default=True)
