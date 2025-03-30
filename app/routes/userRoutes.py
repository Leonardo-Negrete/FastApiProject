from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
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
def GetUserByName(name: str = Query(...), db: Session = Depends(get_db)) -> List[User]:
    matchingUsers = db.query(Users).filter(Users.name.ilike(f"%{name}%")).all()
    return matchingUsers

@router.post("/", response_model=User)
def CreateUsers(user: CreateUser, db: Session = Depends(get_db)) -> User: #user es el modelo de datos que se espera recibir
    new_user = Users(
        name=user.name,
        lastname=user.lastname,
        address=user.address,
        phone=user.phone,
        email=user.email,
        status=user.status
    )  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  
    return new_user 

@router.put("/{id}", response_model=User)
def UpdateUserById(id: int, user: UpdateUser, db: Session = Depends(get_db)) -> User:
    db_user = db.query(Users).filter(Users.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)  

    db.commit()
    db.refresh(db_user)  
    return db_user

@router.delete("/{id}")
def DeleteUserById(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}