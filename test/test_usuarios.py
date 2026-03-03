"""
Pruebas integrales para el módulo de Usuarios y Autenticación.
Cubre registro, validaciones, duplicados y el flujo completo de Login con JWT.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from main import app
from routes.routes_usuario import get_db

# Importamos modelos para la base de datos temporal
from models.model_usuario import Base
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

# Sobrescribimos la BD real por la de pruebas
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# ==========================================
# SETUP MODULE: Aísla la base de datos para este archivo
# ==========================================
def setup_module(module):
    """Prepara la BD vacía e inyecta los datos foráneos antes de correr las pruebas."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    preparar_datos_falsos()

def preparar_datos_falsos():
    """Inyectamos un rol base directamente a MySQL para poder registrar usuarios."""
    db = TestingSessionLocal()
    rol_admin = Rol(id=1, nombre_rol="Administrador", estatus=True)
    db.add(rol_admin)
    db.commit()
    db.close()


# ==========================================
# 2. PRUEBAS DE ENDPOINTS Y LÓGICA DE NEGOCIO
# ==========================================
def test_crear_usuario_exitoso():
    nuevo_usuario = {
        "rol_id": 1, # Usamos el rol que creamos en el Paso Cero
        "nombre": "Test",
        "papellido": "PaTest",
        "sapellido": "SaTest",
        "usuario": "testusuario",
        "password": "ContrasenaSegura123",
        "direccion": "Calle Falsa 123",
        "telefono": "555123412",
        "correo": "test.usuario@example.com",
        "estatus": True
    }

    response = client.post("/usuario/", json=nuevo_usuario)
    
    assert response.status_code == 200 # Tu API retorna 200 en el POST
    data = response.json()
    assert data["usuario"] == nuevo_usuario["usuario"]
    assert data["nombre"] == nuevo_usuario["nombre"]
    # Seguridad: confirmamos que el hash/password no viaje en la respuesta
    assert "password" not in data 

def test_crear_usuario_datos_invalidos():
    """Prueba que Pydantic rechace tipos de datos incorrectos."""
    payload_invalido = {"rol_id": "no_es_un_entero", "nombre": "Error"}
    response = client.post("/usuario/", json=payload_invalido)
    assert response.status_code == 422

def test_usuario_duplicado_rechazado():
    """Prueba tu regla de negocio de no permitir dos 'usernames' iguales."""
    payload = {
        "rol_id": 1,
        "nombre": "TestDup",
        "papellido": "User",
        "usuario": "dupuser", # Este es el username clave
        "password": "dupPass",
        "estatus": True
    }

    # Primer registro debe pasar
    res1 = client.post("/usuario/", json=payload)
    assert res1.status_code == 200

    # Segundo registro con el mismo 'username' debe rebotar
    res2 = client.post("/usuario/", json=payload)
    assert res2.status_code == 400
    assert res2.json()["detail"] == "El nombre de usuario ya está registrado"

def test_login_y_endpoint_protegido():
    """Prueba el flujo completo: Registrar -> Loguear -> Leer usuarios con Token."""
    # 1. Registrar usuario exclusivo para login
    nuevo_usuario = {
        "rol_id": 1,
        "nombre": "TestLogin",
        "papellido": "Login",
        "usuario": "loginuser",
        "password": "LoginPass123",
        "estatus": True
    }
    client.post("/usuario/", json=nuevo_usuario)

    # 2. Hacer Login (Nota: OAuth2PasswordRequestForm usa 'username' y 'password' por defecto)
    login_data = {"username": "loginuser", "password": "LoginPass123"}
    res = client.post("/login/", data=login_data) # Va con 'data=', no con 'json='
    
    assert res.status_code == 200
    token = res.json().get("access_token")
    assert token is not None

    # 3. Usar el token para abrir el candado de una ruta protegida
    headers = {"Authorization": f"Bearer {token}"}
    res2 = client.get("/usuario/", headers=headers)
    
    assert res2.status_code == 200
    usuarios = res2.json()
    # Verificamos que nuestro usuario esté en la lista devuelta
    assert any(u["usuario"] == "loginuser" for u in usuarios)

def test_actualizar_y_eliminar_usuario_protegido():
    """Prueba las rutas PUT y DELETE usando el token de seguridad."""
    
    # 1. Hacemos login con nuestro usuario maestro para obtener la "llave"
    login_data = {"username": "loginuser", "password": "LoginPass123"}
    res_login = client.post("/login/", data=login_data)
    token = res_login.json().get("access_token")
    
    # Preparamos nuestra cabecera con el token para abrir los candados
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Leemos la lista de usuarios y agarramos el ID del usuario "testusuario"
    res_get = client.get("/usuario/", headers=headers)
    usuarios = res_get.json()
    id_a_modificar = next(u["id"] for u in usuarios if u["usuario"] == "testusuario")

    # 3. PRUEBA PUT: Le cambiamos el nombre
    payload_update = {
        "nombre": "AngelModificado"
    }
    res_put = client.put(f"/usuario/{id_a_modificar}", json=payload_update, headers=headers)
    
    assert res_put.status_code == 200
    assert res_put.json()["nombre"] == "AngelModificado"

    # 4. PRUEBA DELETE: Eliminamos al usuario
    res_del = client.delete(f"/usuario/{id_a_modificar}", headers=headers)
    assert res_del.status_code == 200
    
    # 5. Verificamos que ya no aparezca en la lista
    res_get_final = client.get("/usuario/", headers=headers)
    usuarios_finales = res_get_final.json()
    assert no_existe(id_a_modificar, usuarios_finales)

# Función auxiliar rápida para la validación final
def no_existe(id_buscado, lista_usuarios):
    for u in lista_usuarios:
        if u["id"] == id_buscado:
            return False
    return True
