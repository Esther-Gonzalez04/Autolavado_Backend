"""
Este módulo define el modelo Servicio para la base de datos (c_servicio).
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.db import Base


class Servicio(Base):
    """
    Clase que representa la tabla tbc_servicio en la base de datos.
    """
    __tablename__ = "tbc_servicio"

    se_id = Column(Integer, primary_key=True, index=True)
    se_nombre = Column(String(80), nullable=False)
    se_descripcion = Column(String(850), nullable=True)
    se_precio = Column(Float, nullable=False)
    se_estatus = Column(String(45), nullable=False)
    us_id = Column(Integer, ForeignKey("tbb_usuario.us_id"))
