import pytest
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_crear_usuario():

    correo = f"test{uuid.uuid4()}@test.com"

    payload = {

        "rol_id": 2,
        "nombre": "Test",
        "papellido": "Test",
        "sapellido": "Test",
        "usuario": f"user{uuid.uuid4()}",
        "direccion": "Test direccion",
        "telefono": "1234567890",
        "correo": correo,
        "password": "password123",
        "estatus": True
    }

    response = client.post("/usuario", json=payload)

    print(response.status_code)
    print(response.json())

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["correo"] == correo

    # seguridad
    assert "password" not in data

def test_crear_usuario_datos_invalidos():
    # Prueba enviando un tipo de dato incorrecto ( ej. rol_Id comom Strin)
    payload_invalido = {"rol_id": "no-es-un-numero", "nombre": "Error"} 

    response = client.post("/usuario", json=payload_invalido)

    #FastAPI/Pydantic deben retornar 422 Unprocessable Entity automáticamente
    assert response.status_code == 422  # Código de error esperado para datos inválidos
