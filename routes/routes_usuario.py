"""
Módulo de rutas para la gestión de Usuarios y Autenticación.
Contiene endpoints públicos (login, registro) y privados (lectura, edición, eliminación).
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# pylint: disable=import-error
from config import db as config_db
from config.security import create_access_token, get_current_user
from models import model_usuario
from schemas import schema_usuario
from crud import crud_usuario
# pylint: enable=import-error

usuario = APIRouter()

model_usuario.Base.metadata.create_all(bind=config_db.engine)


def get_db():
    """
    Generador de la sesión de la base de datos.
    """
    db = config_db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@usuario.get(
    "/usuario/",
    response_model=List[schema_usuario.Usuario],
    tags=["Usuario"]
)
async def read_usuario(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user)
):
    """
    Obtiene la lista de usuarios. Requiere token de autenticación.
    """
    return crud_usuario.get_usuario(db=db, skip=skip, limit=limit)


@usuario.post(
    "/usuario/",
    response_model=schema_usuario.Usuario,
    tags=["Usuario"]
)
async def create_usuario(
    user_in: schema_usuario.UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo usuario (Registro). Endpoint público sin candado.
    """
    db_user = crud_usuario.get_usuario_by_username(
        db, usuario=user_in.usuario
    )
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está registrado"
        )
    return crud_usuario.create_usuario(db=db, usuario_in=user_in)


@usuario.put(
    "/usuario/{usuario_id}",
    response_model=schema_usuario.Usuario,
    tags=["Usuario"]
)
async def update_usuario(
    usuario_id: int,
    user_in: schema_usuario.UsuarioUpdate,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user)
):
    """
    Actualiza un usuario existente. Requiere token de autenticación.
    """
    db_user = crud_usuario.update_usuario(
        db=db, usuario_id=usuario_id, usuario_in=user_in
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@usuario.delete(
    "/usuario/{usuario_id}",
    response_model=schema_usuario.Usuario,
    tags=["Usuario"]
)
async def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _current_user: str = Depends(get_current_user)
):
    """
    Elimina un usuario de la base de datos. Requiere token de autenticación.
    """
    db_user = crud_usuario.delete_usuario(db=db, usuario_id=usuario_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


@usuario.post("/login/", tags=["Login"])
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Autentica a un usuario y devuelve un token JWT. Endpoint público.
    """
    usuario_auth = crud_usuario.authenticate_user(
        db, form_data.username, form_data.password
    )

    if not usuario_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # CORRECCIÓN: Usar el nombre de usuario para el token
    access_token = create_access_token(
        data={"sub": usuario_auth.usuario}
    )
    return {"access_token": access_token, "token_type": "bearer"}
