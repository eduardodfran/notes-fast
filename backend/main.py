import os
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import hashlib 

app = FastAPI()

postgres_host = os.getenv("DB_HOST", "localhost")
DATABASE_URL = f"postgresql://myuser:mypassword@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)

origins = [
        "http://localhost:5500",  # Example for a local frontend development server
        "http://localhost:8000",
    ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  # Allow cookies and credentials to be sent
        allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],     # Allow all headers in the request
    )

class User(BaseModel):
    username: str
    email: str
    password: str
    
    
# SQLModel for database
class UserModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str

# Pydantic model for request validation
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

  
@app.post("/signup")
async def signup(user: UserCreate):
    hash_object = hashlib.sha256()
    hash_object.update(user.password.encode())
    hashed_password = hash_object.hexdigest()
    db_user = UserModel(username=user.username, email=user.email, password=hashed_password)
    with Session(engine) as session:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return {"message": "User created successfully", "id": db_user.id}

@app.post("/login")
async def login(user: UserLogin):
    hash_object = hashlib.sha256()
    hash_object.update(user.password.encode())
    hashed_password = hash_object.hexdigest()
    with Session(engine) as session:
        statement = select(UserModel).where(
            UserModel.username == user.username,
            UserModel.password == hashed_password
        )
        results = session.exec(statement)
        user_record = results.first()
        print("Queried user:", user_record)
    if user_record:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid username or password"}
    
