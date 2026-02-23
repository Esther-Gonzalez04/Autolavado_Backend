"""
Módulo de seguridad para la autenticación y generación de tokens JWT.
"""
import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

load_dotenv()

# ESTA ES LA MAGIA PARA SWAGGER:
# tokenUrl="login" le dice al candadito a qué ruta debe enviar los datos para loguearse
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un JSON Web Token (JWT) firmado con un tiempo de expiración.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Pylint prefiere variables manejadas de forma segura si el .env falla
        expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)

    to_encode.update({"exp": expire})

    secret_key = os.getenv("SECRET_KEY", "mi_clave_secreta_por_defecto")
    algorithm = os.getenv("ALGORITHM", "HS256")

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Valida el token JWT enviado en la cabecera de la petición.
    Retorna el nombre de usuario si es válido, o lanza HTTPException si no.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        secret_key = os.getenv("SECRET_KEY", "mi_clave_secreta_por_defecto")
        algorithm = os.getenv("ALGORITHM", "HS256")

        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        return username

    except JWTError as exc:
        raise credentials_exception from exc
