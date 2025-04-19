from fastapi import FastAPI, Depends
from app.routes.userRoutes import router 
from app.db.session import engine, Base
from app.dependencies.auth import require_scope

# Crear la base de datos (en un entorno de desarrollo)
def create_database():
    Base.metadata.create_all(bind=engine)

# Ejecutar la creación de la base de datos
create_database()

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir las rutas del enrutador de usuarios
app.include_router(router)

