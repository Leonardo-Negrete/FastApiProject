from fastapi import FastAPI
import uvicorn
from app.routes.userRoutes import router 
from app.db.session import engine, Base

def create_database():
    # Crea todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)

create_database()

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)