"""
Módulo de rutas para la gestión de servicios de vehículos.
Proporciona endpoints protegidos para el CRUD del historial de servicios.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# pylint: disable=import-error
from config import db as config_db
from config.security import get_current_user
from models import model_servicio_vehiculo
from schemas import schema_servicio_vehiculo
from crud import crud_servicio_vehiculo
# pylint: enable=import-error

servicios_vehiculo = APIRouter(
    dependencies=[Depends(get_current_user)]
)

model_servicio_vehiculo.Base.metadata.create_all(bind=config_db.engine)


def get_db():
    """
    Generador para obtener la sesión de la base de datos.
    """
    db = config_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@servicios_vehiculo.get(
    "/servicios-vehiculo/",
    response_model=List[schema_servicio_vehiculo.ServicioVehiculoBase],
    tags=["ServicioVehiculo"]
)
async def read_servicio_vehiculo(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada de los servicios aplicados a los vehículos.
    """
    return crud_servicio_vehiculo.get_servicio_vehiculo(
        db=db, skip=skip, limit=limit
    )


@servicios_vehiculo.post(
    "/servicios-vehiculo/",
    response_model=schema_servicio_vehiculo.ServicioVehiculoBase,
    tags=["ServicioVehiculo"]
)
async def create_servicio(
    servicio_in: schema_servicio_vehiculo.ServicioVehiculoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo registro de servicio para un vehículo específico.
    """
    return crud_servicio_vehiculo.create_servicio_vehiculo(db=db, servicio_in=servicio_in)


@servicios_vehiculo.put(
    "/servicios-vehiculo/{as_id}",
    response_model=schema_servicio_vehiculo.ServicioVehiculoBase,
    tags=["ServicioVehiculo"]
)
async def update_servicio(
    as_id: int,
    servicio_in: schema_servicio_vehiculo.ServicioVehiculoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un servicio de vehículo existente mediante su ID.
    """
    db_servicio = crud_servicio_vehiculo.update_servicio_vehiculo(
        db=db, as_id=as_id, servicio_in=servicio_in
    )
    if db_servicio is None:
        raise HTTPException(
            status_code=404,
            detail="El registro de servicio no existe, no se pudo actualizar"
        )
    return db_servicio


@servicios_vehiculo.delete(
    "/servicios-vehiculo/{as_id}",
    response_model=schema_servicio_vehiculo.ServicioVehiculoBase,
    tags=["ServicioVehiculo"]
)
async def delete_servicio(
    as_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un registro de servicio de vehículo por su ID.
    """
    db_servicio = crud_servicio_vehiculo.delete_servicio_vehiculo(
        db=db, as_id=as_id
    )
    if db_servicio is None:
        raise HTTPException(
            status_code=404,
            detail="El registro de servicio no existe, no se pudo eliminar"
        )
    return db_servicio
