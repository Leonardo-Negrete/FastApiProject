from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List

from pymysql import IntegrityError
from app.schemas.userSchemas import User, CreateUser, UpdateUser
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.models.usersEntity import Users

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)

@router.get("/{id}", response_model=User) #response_model: Indica el modelo de respuesta esperado para esta ruta.
def GetUserById(id: int, db: Session = Depends(get_db)) -> User: #La flecha -> List[User] es una anotación de tipo que se utiliza para indicar que la función devuelve una lista de objetos del tipo User.
    user = db.query(Users).filter(Users.id == id).first() #db es la sesión de la base de datos, y se utiliza para realizar consultas a la base de datos.
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[User])
def GetUserByName(name: str = Query(..., description="Nombre a buscar"),
                  page: int = Query(1, ge=1, description="Número de página (inicia en 1)") #Se agrega la pagina para que se pueda testear la paginación
                  , db: Session = Depends(get_db)) -> List[User]:
    # Se define el número máximo de usuarios por página
    limit = 2
    # Calcula el desplazamiento (offset) para la consulta según el número de página y para que no se repitan los usuarios
    offset = (page - 1) * limit
    # Realiza la consulta a la base de datos usando 'ilike' para una búsqueda insensible a mayúsculas/minúsculas
    matching_users = (
        db.query(Users)
        .filter(Users.name.ilike(f"%{name}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )
    return matching_users

@router.post("/", response_model=User, status_code=201)
def create_user(user: CreateUser, db: Session = Depends(get_db)) -> User:
    # Verificar si el correo ya existe
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = Users(
        name=user.name,
        lastname=user.lastname,
        address=user.address,
        phone=user.phone,
        email=user.email,
        status=user.status
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A database integrity error occurred."
        )

    return new_user

@router.put("/{id}", status_code=204)
def update_user_by_id(id: int, user: UpdateUser, db: Session = Depends(get_db)) -> None:
     # Buscar el usuario por su ID
    db_user = db.query(Users).filter(Users.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {id} not found"
        )
    
    # Convertir los datos recibidos en un diccionario, excluyendo los campos no enviados
    user_data = user.model_dump(exclude_unset=True)
    
    # Si se envía el email, verificar que no exista en otro usuario
    if "email" in user_data:
        email = user_data["email"]
        other_user = db.query(Users).filter(Users.email == email, Users.id != id).first()
        if other_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered to another user"
            )
    
    # Actualizar los atributos del usuario existente con los nuevos datos
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    # Al retornar None, FastAPI enviará un 204 No Content.
    return None

@router.delete("/{id}", status_code=204)
def DeleteUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return 