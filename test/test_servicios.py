"""
Pruebas integrales para el módulo de Vehículos usando MySQL.
Cubre endpoints, integración, base de datos, validación, fechas y llaves foráneas.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from main import app
from routes.routes_vehiculo import get_db
from config.security import get_current_user

# Importamos modelos para recrear las tablas y el Paso Cero
from models.model_vehiculo import Base
from models.model_usuario import Usuario
from models.model_rols import Rol

# ==========================================
# 1. PRUEBAS DE BASE DE DATOS (Configuración Segura)
# ==========================================
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "autolavado_test_db")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return "admin_tester"

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# Variables globales para rastrear IDs en las pruebas
vehiculo_test_id = None


# ==========================================
# SETUP MODULE: Aísla la base de datos para este archivo
# ==========================================
def setup_module(module):
    """Prepara la BD vacía e inyecta los datos foráneos antes de correr las pruebas."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    preparar_datos_falsos()

def preparar_datos_falsos():
    """Inyecta un Rol y un Usuario (Dueño) para satisfacer la llave foránea us_id"""
    db = TestingSessionLocal()
    
    rol_test = Rol(id=1, nombre_rol="ClienteTest", estatus=True)
    db.add(rol_test)
    db.commit()

    usuario_dueno = Usuario(
        id=1, rol_id=1, nombre="Dueño", papellido="Coche", 
        usuario="dueno1", password="123"
    )
    db.add(usuario_dueno)
    db.commit()
    db.close()


# ==========================================
# 2. PRUEBAS DE AUTENTICACIÓN
# ==========================================
def test_acceso_denegado_sin_token():
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get("/vehiculo/")
    assert response.status_code == 401
    app.dependency_overrides[get_current_user] = override_get_current_user


# ==========================================
# 3. PRUEBAS DE VALIDACIÓN DE DATOS
# ==========================================
def test_crear_vehiculo_validacion_datos():
    """Prueba que Pydantic rechace el registro si faltan campos obligatorios."""
    payload_incompleto = {
        "au_placa": "FALTA-INFO"
        # Faltan modelo, serie y fecha_registro
    }
    # Mandamos us_id por query parameter
    response = client.post("/vehiculo/?us_id=1", json=payload_incompleto)
    assert response.status_code == 422


# ==========================================
# 4. PRUEBAS DE ENDPOINTS E INTEGRACIÓN
# ==========================================
def test_crear_vehiculo_exitoso():
    global vehiculo_test_id
    payload = {
        "au_placa": "ABC-1234",
        "au_modelo": "Mazda 3",
        "au_serie": "MZ3XYZ987654321",
        "au_color": "Rojo",
        "au_tipo": "Sedán",
        "au_anio": 2023,
        "estatus": True,
        "fecha_registro": "2026-03-01T14:30:00" # Formato ISO requerido por Pydantic
    }
    # OJO: La ruta pide el us_id como query param en la URL
    response = client.post("/vehiculo/?us_id=1", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["au_placa"] == "ABC-1234"
    assert data["us_id"] == 1
    
    vehiculo_test_id = data["au_id"]

def test_crear_vehiculo_duplicado():
    """Prueba la regla de negocio: no se puede registrar una placa existente."""
    payload = {
        "au_placa": "ABC-1234", # Placa duplicada
        "au_modelo": "Otro Modelo",
        "au_serie": "OTRASERIE123",
        "fecha_registro": "2026-03-01T14:30:00"
    }
    response = client.post("/vehiculo/?us_id=1", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "La placa ya está registrada"

def test_leer_vehiculos():
    response = client.get("/vehiculo/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_actualizar_vehiculo():
    global vehiculo_test_id
    payload_update = {
        "au_color": "Negro", # Le cambiamos el color
        "fecha_modificacion": "2026-03-02T10:00:00"
    }
    response = client.put(f"/vehiculo/{vehiculo_test_id}", json=payload_update)
    
    assert response.status_code == 200
    assert response.json()["au_color"] == "Negro"

def test_eliminar_vehiculo():
    global vehiculo_test_id
    response_del = client.delete(f"/vehiculo/{vehiculo_test_id}")
    assert response_del.status_code == 200
