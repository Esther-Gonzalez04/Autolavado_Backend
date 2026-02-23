"""
Módulo de rutas para la gestión de catálogo de servicios generales.
Incluye las operaciones CRUD protegidas para los tipos de servicios.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# pylint: disable=import-error
from config import db as config_db
from config.security import get_current_user
from models import model_servicio
from schemas import schema_servicio
from crud import crud_servicio
# pylint: enable=import-error

servicio = APIRouter(
    dependencies=[Depends(get_current_user)]
)

model_servicio.Base.metadata.create_all(bind=config_db.engine)


def get_db():
    """
    Generador de la sesión de base de datos.
    """
    db = config_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@servicio.get(
    "/servicios/",
    response_model=List[schema_servicio.ServicioBase],
    tags=["Servicio"]
)
async def read_servicio(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los servicios del catálogo disponibles.
    """
    return crud_servicio.get_servicio(db=db, skip=skip, limit=limit)


@servicio.post(
    "/servicios/",
    response_model=schema_servicio.ServicioBase,
    tags=["Servicio"]
)
async def create_servicio(
    serv_in: schema_servicio.ServicioCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo servicio verificando que el nombre no exista previamente.
    """
    db_servicio = crud_servicio.get_servicio_by_nombre(
        db, se_nombre=serv_in.se_nombre
    )
    if db_servicio:
        raise HTTPException(
            status_code=400,
            detail="El nombre del servicio ya existe"
        )
    return crud_servicio.create_servicio(db=db, servicio_in=serv_in)


@servicio.put(
    "/servicios/{se_id}",
    response_model=schema_servicio.ServicioBase,
    tags=["Servicio"]
)
async def update_servicio(
    se_id: int,
    serv_in: schema_servicio.ServicioUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos y costos de un servicio específico.
    """
    db_servicio = crud_servicio.update_servicio(db=db, se_id=se_id, servicio_in=serv_in)
    if db_servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado, no se pudo actualizar"
        )
    return db_servicio


@servicio.delete(
    "/servicios/{se_id}",
    response_model=schema_servicio.ServicioBase,
    tags=["Servicio"]
)
async def delete_servicio(se_id: int, db: Session = Depends(get_db)):
    """
    Elimina un servicio del catálogo de la base de datos.
    """
    db_servicio = crud_servicio.delete_servicio(db=db, se_id=se_id)
    if db_servicio is None:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado, no se pudo eliminar"
        )
    return db_servicio
