from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt 
import os
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY","secret")
ALGORITHM = "HS256"
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "admin" and form_data.password == "admin":
        token = jwt.encode(
            {"sub": form_data.username},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials")