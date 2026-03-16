from fastapi import FastAPI , Depends,HTTPException,Header,Query,Response
from pydantic import BaseModel
from jose import jwt,JWTError
from pymongo import MongoClient
from Crypto.Cipher import AES
import base64
import os
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY","secret")
ALGORITHM = "HS256"

client= MongoClient("mongodb://mongodb:27017/")
db = client["PRODUCT_APIS"]
categories = db["categories"]

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/token")

client = MongoClient("mongodb://mongodb:27017/")
db = client["PRODUCT_APIS"]
categories = db["categories"]

AES_KEY = os.getenv("AES_KEY", "mysecretkey12345").encode()


def encrypt_response(data: str):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + ciphertext).decode()

def verify_token(token: str = Depends(oauth2_scheme)):
    print("TOKEN RECEIVED:", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", payload)
        return payload
    except JWTError as e:
        print("JWT ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid token")
class Category(BaseModel):
    name: str


@app.post("/categories")
def create_category(category: Category, user=Depends(verify_token)):
    categories.insert_one(category.dict())
    return {"message": encrypt_response("Category created")}