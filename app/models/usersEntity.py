from app.db.session import Base
from sqlalchemy import Boolean, Column, Integer, String, DateTime #importamos las clases necesarias para crear la tabla
from datetime import datetime #importamos la clase datetime para crear la fecha y hora actual

class Users(Base):
    __tablename__ = "Users" #nombre de la tabla en la base de datos
    #Con un índice, accede directamente a los datos, haciendo la consulta más rápida.
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) #id es la clave primaria y es un entero
    name = Column(String(50), nullable=False) #name es un string de 50 caracteres y no puede ser nulo
    lastname = Column(String(50), nullable=False) #lastname es un string de 50 caracteres y no puede ser nulo
    address = Column(String(100), nullable=True) #address es un string de 100 caracteres y puede ser nulo
    phone = Column(Integer, nullable=False) #phone es un entero y no puede ser nulo
    email = Column(String(100), nullable=False) #email es un string de 100 caracteres y no puede ser nulo
    create_user = Column(DateTime, default=datetime.now,onupdate=datetime.now) #create_user es un DateTime con la fecha y hora actual y se actualiza cada vez que se modifica el registro
    #onupdate: Actualiza la fecha y hora cada vez que se modifica el registro.
    status = Column(Boolean, nullable=False) #status es un booleano
