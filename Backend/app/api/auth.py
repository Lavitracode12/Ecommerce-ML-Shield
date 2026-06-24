from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db, UserModel
from app.core.security import hash_password, verify_password, create_access_token

auth_router = APIRouter(prefix="/auth", tags=["User Security Management"])

class UserAuthSchema(BaseModel):
    username: str
    password: str

@auth_router.post("/register")
def register_user(payload: UserAuthSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username identity parameter already registered inside matrix.")
    
    new_user = UserModel(
        username=payload.username,
        password_hash=hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "User account created successfully inside database", "username": new_user.username}

@auth_router.post("/login")
def login_user(payload: UserAuthSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credential combination tokens verified.")
    
    token = create_access_token(data={"sub": user.username, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id, "username": user.username}