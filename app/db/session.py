import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Obtiene las variables de entorno o usa valores por defecto
DB_USER = os.getenv("DB_USER", "user")  # Si no se encuentra, usa "user"
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "host.docker.internal")  # "db" es el nombre del servicio MySQL en Docker Compose
DB_PORT = os.getenv("DB_PORT", "3307")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")

#Una f-string permite insertar variables dentro de una cadena de manera sencilla y legible.
#Por ejemplo, sin cuerdas f tendrías que hacer esto: "mysql+pymysql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#create_engine() es una función de SQLAlchemy que se encarga de establecer una conexión con la base de datos, permitiendo ejecutar consultas SQL desde Python.
engine = create_engine(SQLALCHEMY_DATABASE_URL) 
"""sessionmaker() es una función de SQLAlchemy que crea una clase de sesión que se puede utilizar para interactuar con la base de datos.
autocommit=False significa que las transacciones no se confirmarán automáticamente después de cada operación.
autoflush=False significa que los cambios no se enviarán automáticamente a la base de datos después de cada operación.
bind=engine significa que la sesión estará vinculada al motor de base de datos creado anteriormente."""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base es una clase base para los modelos de SQLAlchemy. Los modelos de SQLAlchemy deben heredar de esta clase para funcionar correctamente.
#A partir de esta clase, se pueden definir modelos que representarán las tablas de la base de datos.
Base = declarative_base()

"""
get_db() es una función generadora que se utiliza para obtener una sesión de base de datos.
SessionLocal() es una instancia de sessionmaker, que se encarga de crear una sesión de base de datos para ejecutar consultas.
yield hace que get_db() se comporte como un generador en lugar de una función normal.
Cuando una función llama a get_db(), recibe la sesión db y la usa mientras se ejecuta.
finally asegura que, pase lo que pase (incluso si hay un error), la sesión se cerrará correctamente para evitar fugas de memoria o conexiones abiertas."""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()