from fastapi import FastApi , Depends,HTTPException,Header,Query,Response
from pydantic import BaseModel
from jose import jwt,JWTError
from pymongo import MongoClient
from Crypto.Cipher import AES
import base64
import os

from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY","secret")
ALGORITHM = "HS256"


client= MongoClient("mongodb://mongodb:27017/")
db = client["PRODUCT_APIS"]
categories = db["categories"]

app = FastApi()

AES_KEY=os.getenv("AES_KEY")

def encrypt_response(data:str):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext,tag =cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + ciphertext.decode())

def verify_token(authorization: str=Header(...)):
    try:
        scheme,token =authorization.split()
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid token")

class Category(BaseModel):
    name:str

@app.post("/categories")
def create_category(category:Category,user=Depends(verify_token)):
    cat = category.dict()
    categories.insert_one(cat)
    return{"message": encrypt_response("Category created")}
