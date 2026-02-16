from fastapi import FastAPI
import config.db

# importar modelos
import models.model_rols
import models.model_usuario
import models.model_servicio
import models.model_vehiculo
import models.model_servicio_vehiculo

# importar rutas
from routes.routes_rol import rol
from routes.routes_servicio import servicio
from routes.routes_servicio_vehiculo import servicios_vehiculo
from routes.routes_usuario import usuario
from routes.routes_vehiculo import vehiculo

app = FastAPI(
    title="Sistema de Control de Autolavado",
    description="Sistema de creación y almacenamiento de información y ventas en un autolavado",
)

# crear tablas
models.model_rols.Base.metadata.create_all(bind=config.db.engine)

# incluir routers
app.include_router(rol)
app.include_router(servicio)
app.include_router(servicios_vehiculo)
app.include_router(usuario)
app.include_router(vehiculo)
