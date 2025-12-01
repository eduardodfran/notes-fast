from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import hashlib
import db

app = FastAPI()

db.check_table()


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
    
  
@app.post("/signup")
async def signup(user: User):
    hash_object = hashlib.sha256()
    hash_object.update(user.password.encode())
    hashed_password = hash_object.hexdigest()
    db.insert_user(user.username, user.email, hashed_password)
        
    return {"message": "User created successfully"}


@app.post("/login")
async def login(user: User):
    hash_object = hashlib.sha256()
    hash_object.update(user.password.encode())
    hashed_password = hash_object.hexdigest()
    # check if user exists in db with hashed password
    con = db.connect_db()
    cur = con.cursor()
    res = cur.execute("""
    SELECT * FROM user WHERE username = ? AND password = ?
    """, (user.username, hashed_password))
    user_record = res.fetchone()
    con.close()
    # if user exists, return success message
    if user_record:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid username or password"}
    