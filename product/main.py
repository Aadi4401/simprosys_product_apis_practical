from fastapi import FastAPI, Depends,HTTPException,Header,Query,Response
from pydantic import BaseModel
from jose import jwt,JWTError
from pymongo import MongoClient
from Crypto.Cipher import AES
import base64
import os
import requests
from dotenv import load_dotenv
import openpyxl
from fastapi.responses import StreamingResponse
from bson.objectid import ObjectId
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY= os.getenv("SECRET_KEY","secret")
ALGORITHM= "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/token")
AES_KEY=os.getenv("AES_KEY","mysecretkey12345").encode()

client= MongoClient("mongodb://mongodb:27017/")
db = client["PRODUCT_APIS"]
products = db["products"]

app = FastAPI()


def encrypt_response(data: str):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + ciphertext).decode()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
class Product(BaseModel):
    name:str
    price:float
    category_id:str


@app.post("/products")
def create_product(product:Product, user=Depends(verify_token)):
    prod=product.dict()
    result = products.insert_one(prod)
    return {"message": encrypt_response("Product Created"),"id":str(result.inserted_id)}

@app.get("/products/search")
def search_products(name:str=Query(...),user=Depends(verify_token)):
    prod_list= list(products.find({"name":{"regex": name,"$options":"i"}},{"_id":0}))
    return {"data":encrypt_response(str(prod_list))}


@app.put("/products/{product_id}")
def update_product(product_id:str,product:Product,user= Depends(verify_token)):
    result = products.update_one({"_id":ObjectId(product_id)},{"$set":product.dict()})
    if result.matched_count==0:
        raise HTTPException(status_code=404,detail="product not found")
    return {"message":encrypt_response("product updated")}

@app.delete("/products/{product_id}")
def delete_product(product_id:str, user= Depends(verify_token)):
    result= products.delete_one({"_id":ObjectId(product_id)})
    if result.deleted_count==0:
        raise HTTPException(status_code=404,detail="product not found")
    return {"message":encrypt_response("Product deleted")}

@app.get("/products")
def list_products(user=Depends(verify_token)):
    prod_list= list(products.find({},{"_id":0}))
    return {"data": encrypt_response(str(prod_list))}


@app.post("/products/bulk")
def bulk_create_products(n:int = 1000,user= Depends(verify_token)):
    requests.post("http://celery_worker:8000/bulk_create", json={"n": n})
    return {"message":encrypt_response(f"Bulk creation started for {n} products")}

@app.get("/products/export")
def export_products(user=Depends(verify_token)):
    prod_list = list(products.find({},{"_id":0}))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["name","price","category_id"])
    for prod in prod_list:
        ws.append([prod["name"], prod["price"], prod["category_id"]])
    from io import BytesIO
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    headers={"Content-Disposition":"attachment;filename=products.xlsx"}
    return StreamingResponse(stream,media_type="application/vnd.openxmlformats-officedocument.spreadsheet.sheet",headers=headers)
                 