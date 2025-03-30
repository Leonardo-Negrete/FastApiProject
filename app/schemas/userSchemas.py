from datetime import datetime
from typing import Optional
from pydantic import BaseModel
"""Pydantic es una bibliioteca de validación de datos y configuración para Python
Permite definir modelos de datos que aseguran que las entradas y salidas cumplan 
con los tipos y restricciones especificados, facilitando así la validación automática 
y la transformación de datos en aplicaciones Python."""


class User(BaseModel): #schema
    id: int
    name: str
    lastname: str
    address: Optional[str] = None
    phone: int
    email: str
    create_user: datetime = datetime.now()
    status: bool = True #status es un booleano y por defecto es True

class CreateUser(BaseModel): #schema
    name: str
    lastname: str
    address: Optional[str] = None
    phone: int
    email: str
    status: bool = True

class UpdateUser(BaseModel): #schema
    name: str
    lastname: str
    address: Optional[str] = None #Optional[str]: La variable puede ser una cadena o None.
                                  # None: Si no se proporciona un valor, se asume que es None.
    email: str
    phone: int
    status: bool = True