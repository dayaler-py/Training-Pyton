from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .auth import decode_token
from .database import SessionLocal
from .models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db: Session):
    payload = decode_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
