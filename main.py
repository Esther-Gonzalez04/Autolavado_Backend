"""
Punto de entrada principal para la API del backend de Autolavado.
Configura la aplicación FastAPI, inicializa la base de datos y registra las rutas.
"""

from fastapi import FastAPI

# Apagamos las advertencias de importaciones locales
# pylint: disable=import-error
import config.db

# Importamos los modelos para que SQLAlchemy registre las tablas.
# Apagamos la advertencia de 'unused-import' porque Pylint no detecta
# que SQLAlchemy los necesita en memoria para el create_all().
# pylint: disable=unused-import
import models.model_rols
import models.model_usuario
import models.model_servicio
import models.model_vehiculo
import models.model_servicio_vehiculo
# pylint: enable=unused-import

# Importar rutas
from routes.routes_rol import rol
from routes.routes_servicio import servicio
from routes.routes_servicio_vehiculo import servicios_vehiculo
from routes.routes_usuario import usuario
from routes.routes_vehiculo import vehiculo
# pylint: enable=import-error


app = FastAPI(
    title="Sistema de Control de Autolavado",
    description="Sistema de creación y almacenamiento de información y ventas en un autolavado",
    version="1.0.0"
)

# Crear todas las tablas en la base de datos.
# Al usar la Base del modelo de roles, se crearán todas las tablas
# de los modelos que fueron importados previamente.
models.model_rols.Base.metadata.create_all(bind=config.db.engine)

# Incluir routers
app.include_router(usuario)
app.include_router(rol)
app.include_router(vehiculo)
app.include_router(servicio)
app.include_router(servicios_vehiculo)

@app.get("/", tags=["Inicio"])
def read_root():
    """
    Ruta raíz para verificar que la API está levantada correctamente.
    """
    return {"mensaje": "Bienvenido a la API de Autolavado. Visita /docs para ver Swagger."}
