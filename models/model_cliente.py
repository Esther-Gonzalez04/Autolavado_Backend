"""
Este modulo define el modelo Cliente para la base de datos (c_cliente).
"""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String
from config.db import Base


class Cliente(Base):
    """
    Clase que representa la tabla tbc_cliente en la base de datos.
    """
    __tablename__ = "tbc_cliente"

    cl_id = Column(Integer, primary_key=True, index=True)
    cl_nombre = Column(String(60), nullable=False)
    cl_apellidoPaterno = Column(String(60), nullable=False)
    cl_apellidoMaterno = Column(String(60), nullable=True)
    cl_direccion = Column(String(255), nullable=True)
    cl_email = Column(String(55), nullable=True)
    cl_telefono = Column(String(15), nullable=True)
    cl_password = Column(String(750), nullable=False)

    def __repr__(self):
        """Representacion en string del objeto Cliente"""
        return f"<Cliente(nombre={self.cl_nombre}, email={self.cl_email})>"
