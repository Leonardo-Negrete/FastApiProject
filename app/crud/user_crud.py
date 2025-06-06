from sqlalchemy.orm import Session
from app.models.usersEntity import Users
from app.schemas.userSchemas import CreateUser, UpdateUser
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
# Obtener un usuario por ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id == user_id).first()

# Obtener usuarios por nombre con paginación
def get_users_by_name(db: Session, name: str, page: int, limit: int = 2):
    offset = (page - 1) * limit
    return db.query(Users).filter(Users.name.ilike(f"%{name}%")).offset(offset).limit(limit).all()

# Crear un nuevo usuario
def create_user(db: Session, user: CreateUser):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
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

# Actualizar un usuario
def update_user(db: Session, user_id: int, user_data: UpdateUser):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        return None

    # Validar manualmente si el nuevo email ya está registrado por otro usuario
    if user_data.email:
        existing_user = db.query(Users).filter(Users.email == user_data.email, Users.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="Email already registered by another user")

    # Actualizar solo los campos proporcionados
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# Eliminar un usuario por ID
def delete_user(db: Session, user_id: int):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
