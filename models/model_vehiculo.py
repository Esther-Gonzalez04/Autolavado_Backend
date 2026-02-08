"""
Este módulo define el modelo Vehiculo para la base de datos.
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base


class Vehiculo(Base):
    """
    Clase que representa la tabla tbb_vehiculo en la base de datos.
    """
    __tablename__ = "tbb_vehiculo"

    au_id = Column(Integer, primary_key=True, index=True)
    au_modelo = Column(String(45), nullable=False)
    au_matricula = Column(String(45), nullable=False, unique=True)
    au_color = Column(String(45), nullable=True)
    # Se corrige a minúsculas para cumplir con PEP 8 (snake_case)
    au_tipo = Column(String(45), nullable=True)

    # Asegúrate de que 'tbc_cliente' sea el nombre correcto de la tabla Cliente
    cl_id = Column(Integer, ForeignKey("tbc_cliente.cl_id"))
