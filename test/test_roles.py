"""
Pruebas integrales para el módulo de Roles usando MySQL.
Cubre endpoints, integración, base de datos, autenticación y validación.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Importamos la app y dependencias necesarias
from main import app
from routes.routes_rol import get_db
from config.security import get_current_user
from models.model_rols import Base

# ==========================================
# 1. PRUEBAS DE BASE DE DATOS (Configuración MySQL con .env)
# ==========================================
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "autolavado_test_db") 

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribimos la BD real por la de pruebas
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Creamos un usuario "fantasma" para saltarnos el candado en las pruebas
def override_get_current_user():
    return "admin_tester"

# Aplicamos las sobrescrituras a la aplicación
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


# ==========================================
# SETUP MODULE: Aísla la base de datos para este archivo
# ==========================================
def setup_module(module):
    """
    Esta función mágica de Pytest se ejecuta UNA SOLA VEZ justo antes 
    de que comiencen las pruebas de este archivo en específico.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# Variables globales para guardar IDs durante la prueba de integración
rol_test_id = None


# ==========================================
# 2. PRUEBAS DE AUTENTICACIÓN Y AUTORIZACIÓN
# ==========================================
def test_acceso_denegado_sin_token():
    """Prueba que el candado global del router funcione correctamente."""
    app.dependency_overrides.pop(get_current_user, None)
    
    response = client.get("/rol/")
    assert response.status_code == 401
    
    app.dependency_overrides[get_current_user] = override_get_current_user


# ==========================================
# 3. PRUEBAS DE VALIDACIÓN DE DATOS
# ==========================================
def test_crear_rol_validacion_datos():
    """Prueba que Pydantic rechace un rol si le falta el nombre."""
    payload_invalido = {
        "estatus": True
    }
    response = client.post("/rol/", json=payload_invalido)
    assert response.status_code == 422


# ==========================================
# 4. PRUEBAS DE ENDPOINTS E INTEGRACIÓN (Flujo CRUD Completo)
# ==========================================
def test_crear_rol_exitoso():
    """Prueba el endpoint POST para crear un rol en la BD."""
    global rol_test_id
    payload = {
        "nombre_rol": "RolDePrueba",
        "estatus": True
    }
    response = client.post("/rol/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_rol"] == "RolDePrueba"
    assert "id" in data
    
    rol_test_id = data["id"]

def test_crear_rol_duplicado():
    """Prueba la lógica de negocio: no se pueden repetir nombres de rol."""
    payload = {
        "nombre_rol": "RolDePrueba",
        "estatus": True
    }
    response = client.post("/rol/", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Rol existente, intenta nuevamente"

def test_leer_roles_y_buscar():
    """Prueba los endpoints GET general y de búsqueda por nombre."""
    response_lista = client.get("/rol/")
    assert response_lista.status_code == 200
    assert len(response_lista.json()) > 0
    
    response_buscar = client.get("/rols/buscar/RolDePrueba")
    assert response_buscar.status_code == 200
    assert response_buscar.json()["nombre_rol"] == "RolDePrueba"

def test_actualizar_rol():
    """Prueba el endpoint PUT para modificar un registro existente."""
    global rol_test_id
    payload_update = {
        "nombre_rol": "RolActualizado",
        "estatus": False
    }
    response = client.put(f"/rol/{rol_test_id}", json=payload_update)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_rol"] == "RolActualizado"
    assert data["estatus"] is False

def test_eliminar_rol():
    """Prueba el endpoint DELETE y verifica que el registro ya no exista."""
    global rol_test_id
    response_del = client.delete(f"/rol/{rol_test_id}")
    assert response_del.status_code == 200
    
    response_buscar = client.get("/rols/buscar/RolActualizado")
    assert response_buscar.status_code == 404
    assert response_buscar.json()["detail"] == "Rol no encontrado"
