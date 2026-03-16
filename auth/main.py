from fastapi import FastApi, HTTPException
from pydantic import BaseModel
from jose import jwt 
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY","secret")
ALGORITHM = "HS256"

app = FastApi()

class User(BaseModel):
    username:str
    password:str

@app.post("/token")
def login(user:User):
    if user.username == "admin" and user.password == "admin":
        token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token":token, "token_type": "bearer"}
    
    raise HTTPException(status_code=400,detail= "Invalid credentials")

