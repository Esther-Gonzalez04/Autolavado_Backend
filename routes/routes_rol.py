"""
Módulo de rutas para la gestión de roles.
Contiene los endpoints de la API para crear, leer, actualizar y eliminar roles.
Todos los endpoints están protegidos y requieren autenticación JWT.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# pylint: disable=import-error
from config import db as config_db
from config.security import get_current_user
from models import model_rols
from schemas import schema_rol
from crud import crud_rol

# El candado se aplica a todo el router
rol = APIRouter(
    dependencies=[Depends(get_current_user)]
)

model_rols.Base.metadata.create_all(bind=config_db.engine)


def get_db():
    """
    Generador de dependencias para obtener la sesión de la base de datos.
    """
    db = config_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@rol.get("/rol/", response_model=List[schema_rol.Rol], tags=["Roles"])
async def read_rols(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista paginada de todos los roles.
    """
    db_rol = crud_rol.get_rol(db=db, skip=skip, limit=limit)
    return db_rol


@rol.get("/rols/buscar/{nombre}", response_model=schema_rol.Rol, tags=["Roles"])
def buscar_rol_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """
    Busca un rol específico por su nombre exacto.
    """
    rol_encontrado = crud_rol.get_rol_by_nombre(db, nombre_rol=nombre)
    if not rol_encontrado:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol_encontrado


@rol.post("/rol/", response_model=schema_rol.Rol, tags=["Roles"])
def create_rol(rol_in: schema_rol.RolCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo rol verificando previamente que no exista.
    """
    db_rol = crud_rol.get_rol_by_nombre(db, nombre_rol=rol_in.nombre_rol)
    if db_rol:
        raise HTTPException(status_code=400, detail="Rol existente, intenta nuevamente")
    return crud_rol.create_rol(db=db, rol_in=rol_in)


@rol.put("/rol/{rol_id}", response_model=schema_rol.Rol, tags=["Roles"])
async def update_rol(rol_id: int, rol_in: schema_rol.RolUpdate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un rol existente mediante su ID.
    """
    db_rol = crud_rol.update_rol(db=db, rol_id=rol_id, rol_in=rol_in)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no existe, no actualizado")
    return db_rol


@rol.delete("/rol/{rol_id}", response_model=schema_rol.Rol, tags=["Roles"])
async def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    """
    Elimina un rol existente de la base de datos mediante su ID.
    """
    db_rol = crud_rol.delete_rol(db=db, rol_id=rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="El Rol no existe, no se pudo eliminar")
    return db_rol
