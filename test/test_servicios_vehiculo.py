"""
Pruebas integrales para el módulo de Servicios-Vehículos usando MySQL.
Cubre endpoints, relaciones de llaves foráneas, base de datos y validación.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from main import app
from routes.routes_servicio_vehiculo import get_db
from config.security import get_current_user

# Importamos todos los modelos para asegurar la integridad referencial
from models.model_servicio_vehiculo import Base
from models.model_usuario import Usuario
from models.model_vehiculo import Vehiculo
from models.model_servicio import Servicio
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

# Variable global para rastrear el ID creado
servicio_vehiculo_test_id = None


# ==========================================
# SETUP MODULE: Aísla la base de datos para este archivo
# ==========================================
def setup_module(module):
    """Limpia la BD y prepara el entorno relacional complejo antes de los tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    preparar_datos_falsos()

def preparar_datos_falsos():
    """Inyecta dependencias para satisfacer todas las Llaves Foráneas."""
    db = TestingSessionLocal()
    
    # 1. Rol base
    rol_test = Rol(id=1, nombre_rol="RolTest", estatus=True)
    db.add(rol_test)
    db.commit()

    # 2. Usuarios (Cajero id=1 y Operativo id=2)
    cajero = Usuario(id=1, rol_id=1, nombre="Cajero", papellido="Test", usuario="cajero", password="123")
    operativo = Usuario(id=2, rol_id=1, nombre="Operativo", papellido="Test", usuario="operativo", password="123")
    db.add_all([cajero, operativo])
    db.commit()
    
    # 3. Vehículo (ID=1) - Con campos obligatorios según tus modelos
    vehiculo = Vehiculo(
        au_id=1, us_id=1, au_placa="XYZ-123", au_modelo="2020",
        au_serie="SERIE-TEST-123", fecha_registro="2026-03-01"
    ) 
    db.add(vehiculo)
    
    # 4. Servicio (ID=1) - Con campos obligatorios según tus modelos
    servicio = Servicio(
        se_id=1, se_nombre="Lavado Pro", se_precio=150.0,
        se_duracion_minutos=40, us_id=1
    )
    db.add(servicio)

    db.commit()
    db.close()


# ==========================================
# 2. PRUEBAS DE AUTENTICACIÓN
# ==========================================
def test_acceso_denegado_sin_token():
    """Prueba que no se pueda entrar sin estar logueado."""
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get("/servicios-vehiculo/")
    assert response.status_code == 401
    app.dependency_overrides[get_current_user] = override_get_current_user


# ==========================================
# 3. PRUEBAS DE VALIDACIÓN DE DATOS
# ==========================================
def test_crear_servicio_vehiculo_validacion_datos():
    """Prueba que el sistema rechace JSONs incompletos (Faltan IDs)."""
    payload_incompleto = {
        "as_estatus": "Programada" # No mandamos au_id, se_id, etc.
    }
    response = client.post("/servicios-vehiculo/", json=payload_incompleto)
    assert response.status_code == 422


# ==========================================
# 4. PRUEBAS DE ENDPOINTS E INTEGRACIÓN
# ==========================================
def test_crear_servicio_vehiculo_exitoso():
    """Prueba la creación exitosa vinculando todas las tablas."""
    global servicio_vehiculo_test_id
    payload = {
        "au_id": 1,
        "cajero_id": 1,
        "operativo_id": 2,
        "se_id": 1,
        "as_fecha": "2026-03-01T10:00:00",
        "as_hora": "10:00:00",
        "as_estatus": "Programada",
        "as_estado": True
    }
    response = client.post("/servicios-vehiculo/", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Verificamos que se guardó el ID para las siguientes pruebas
    assert "as_id" in data
    servicio_vehiculo_test_id = data["as_id"]

def test_leer_servicios_vehiculo():
    """Prueba que el registro creado aparezca en la lista."""
    response = client.get("/servicios-vehiculo/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_actualizar_servicio_vehiculo():
    """Prueba el cambio de estatus del servicio."""
    global servicio_vehiculo_test_id
    payload_update = {"as_estatus": "Proceso"}
    response = client.put(f"/servicios-vehiculo/{servicio_vehiculo_test_id}", json=payload_update)
    assert response.status_code == 200
    assert response.json()["as_estatus"] == "Proceso"

def test_eliminar_servicio_vehiculo():
    """Prueba el borrado final del registro de servicio."""
    global servicio_vehiculo_test_id
    response_del = client.delete(f"/servicios-vehiculo/{servicio_vehiculo_test_id}")
    assert response_del.status_code == 200
