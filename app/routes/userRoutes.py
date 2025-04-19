from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.userSchemas import User, CreateUser, UpdateUser
from app.db.session import get_db
from app.crud.user_crud import get_user_by_id, get_users_by_name, create_user, update_user, delete_user
from app.dependencies.auth import require_scope

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)

@router.get("/{id}", response_model=User)
def GetUserById(
    id: int, 
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_scope("read"))) -> User:

    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[User])
def GetUserByName(
    name: str = Query(..., description="Nombre a buscar"),
    page: int = Query(1, ge=1, description="Número de página (inicia en 1)"),
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_scope("read"))) -> List[User]:

    matching_users = get_users_by_name(db, name, page)
    return matching_users

@router.post("/", response_model=User, status_code=201)
def create_user_endpoint(
    user: CreateUser, 
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_scope("write"))) -> User:

    return create_user(db, user)

@router.put("/{id}", status_code=204)
def update_user_by_id(
    id: int, 
    user: UpdateUser, 
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_scope("write"))) -> None:
    updated_user = update_user(db, id, user)
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {id} not found"
        )
    return None

@router.delete("/{id}", status_code=204)
def DeleteUserById(
    id: int, 
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_scope("write"))
):
    deleted_user = delete_user(db, id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return None
