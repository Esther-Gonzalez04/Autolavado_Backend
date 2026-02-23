"""
Módulo de rutas para la gestión de Vehículos.
Todos los endpoints están protegidos por autenticación JWT para evitar accesos no autorizados.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# pylint: disable=import-error
from config import db as config_db
from config.security import get_current_user
from models import model_vehiculo
from schemas import schema_vehiculo
from crud import crud_vehiculo
# pylint: enable=import-error

vehiculo = APIRouter(
    dependencies=[Depends(get_current_user)]
)

model_vehiculo.Base.metadata.create_all(bind=config_db.engine)


def get_db():
    """
    Generador de la sesión de la base de datos.
    """
    db = config_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@vehiculo.get(
    "/vehiculo/",
    response_model=List[schema_vehiculo.Vehiculo],
    tags=["Vehiculo"]
)
async def read_vehiculos(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada de todos los vehículos registrados.
    """
    return crud_vehiculo.get_vehiculo(db=db, skip=skip, limit=limit)


@vehiculo.post(
    "/vehiculo/",
    response_model=schema_vehiculo.Vehiculo,
    tags=["Vehiculo"]
)
async def create_vehiculo(
    veh_in: schema_vehiculo.VehiculoCreate,
    us_id: int,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo vehículo asociado a un usuario y verifica que la placa no exista.
    """
    db_veh = crud_vehiculo.get_vehiculo_by_placa(
        db, au_placa=veh_in.au_placa
    )
    if db_veh:
        raise HTTPException(
            status_code=400, detail="La placa ya está registrada"
        )
    return crud_vehiculo.create_vehiculo(db=db, vehiculo_in=veh_in, us_id=us_id)


@vehiculo.put(
    "/vehiculo/{au_id}",
    response_model=schema_vehiculo.Vehiculo,
    tags=["Vehiculo"]
)
async def update_vehiculo(
    au_id: int,
    veh_in: schema_vehiculo.VehiculoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un vehículo existente.
    """
    db_veh = crud_vehiculo.update_vehiculo(
        db=db, au_id=au_id, vehiculo_in=veh_in
    )
    if not db_veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_veh


@vehiculo.delete(
    "/vehiculo/{au_id}",
    response_model=schema_vehiculo.Vehiculo,
    tags=["Vehiculo"]
)
async def delete_vehiculo(au_id: int, db: Session = Depends(get_db)):
    """
    Elimina un vehículo de la base de datos mediante su ID.
    """
    db_veh = crud_vehiculo.delete_vehiculo(db=db, au_id=au_id)
    if not db_veh:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_veh
