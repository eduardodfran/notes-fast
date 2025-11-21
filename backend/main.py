from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import hashlib


app = FastAPI()

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
    user.password = hash_object.hexdigest()
    user_dict = user.model_dump()
    print(user_dict)
    data = []
    with open("./data/users.json", "r") as f:
        data = json.load(f)
    data["users"].append(user_dict)
    
    # auto id
    new_id = len(data["users"]) + 1
    user_dict["id"] = new_id

    # append
    data["users"].append(user_dict)
    
    with open("./data/users.json", "w") as f:
        json.dump(data, f, indent=4)
