from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from core.services.auth import schemas, auth
from core.models.user import User
from config.settings import Config
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DATABASE_URL = Config.URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Такое имя пользователя уже существует")
    
    hash_password = auth.create_hashed_password(user.password)
    db_user = User(username=user.username, hash_password=hash_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "id": db_user.id,
        "username": db_user.username
    }


@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not auth.verify_password(user.password, db_user.hash_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    access_token_expires = timedelta(minutes=1440 * 7) 
    access_token = auth.create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/change")
def change_password(change_password: schemas.ChangePassword, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = auth.decode_access_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_user = db.query(User).filter(User.username == username).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth.verify_password(change_password.current_password, db_user.hash_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    hash_new_password = auth.create_hash_password(change_password.new_password)
    
    db_user.hash_password = hash_new_password
    db.commit()
    
    return {"detail": "Пароль успешно сменён"}