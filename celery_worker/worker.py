from celery import Celery
from fastapi import FastAPI
from pydantic import BaseModel
from jose import jwt,JWTError
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app= Celery('worker',broker="redis://redis:6379/0")


client= MongoClient("mongodb://mongodb:27017/")
db = client["PRODUCT_APIS"]
products = db["products"]

@app.task
def bulk_create_products(n):
    for i in range(n):
        products.insert_one({"name":f'product {i}',"price":10.0,"category_id":"dummy"})


api = FastAPI()

class BulkRequest(BaseModel):
    n:int
@api.post("/bulk_create")
def trigger_bulk(req:BulkRequest):
    bulk_create_products.delay(req.n)
    return {"status":"started"}

