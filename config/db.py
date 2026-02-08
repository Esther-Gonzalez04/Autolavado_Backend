"""
Este archivo permite conectar con la base de datos.
"""
# pylint: disable=invalid-name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Se recomienda usar el driver explícito (mysql+pymysql)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3307/autolavadoDB"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Se usa PascalCase (SessionLocal) porque es una "fábrica" de sesiones (Clase)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
