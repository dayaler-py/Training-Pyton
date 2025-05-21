from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from . import models, schemas, auth, utils
from .database import Base, engine
from .models import User

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=schemas.UserCreate)
def register(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = auth.hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    return user

@app.post("/login", response_model=schemas.Token)
def login(form: schemas.UserLogin, db: Session = Depends(utils.get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not auth.verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user.username})
    refresh_token = auth.create_refresh_token(data={"sub": user.username})
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)

@app.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str = Header(...)):
    payload = auth.decode_token(refresh_token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = auth.create_access_token(data={"sub": username})
    new_refresh_token = auth.create_refresh_token(data={"sub": username})
    return schemas.Token(access_token=new_access_token, refresh_token=new_refresh_token)

@app.get("/me", response_model=schemas.UserCreate)
def get_user(token: str = Header(...), db: Session = Depends(utils.get_db)):
    user = utils.get_current_user(token, db)
    return schemas.UserCreate(username=user.username, email=user.email, password="hidden")

@app.put("/me", response_model=schemas.UserCreate)
def update_user(data: schemas.UserCreate, token: str = Header(...), db: Session = Depends(utils.get_db)):
    user = utils.get_current_user(token, db)
    user.username = data.username
    user.email = data.email
    user.password = auth.hash_password(data.password)
    db.commit()
    return data

@app.delete("/me")
def delete_user(token: str = Header(...), db: Session = Depends(utils.get_db)):
    user = utils.get_current_user(token, db)
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}
