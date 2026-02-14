from fastapi import FastAPI
from routes.routes_rol import rol

app = FastAPI(
    title="Sistema de control de autolavado",
    description="Sistema de creación y almacenamiento de información y ventas en autolavado"
)

app.include_router(rol)