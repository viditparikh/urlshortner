import pymongo
from fastapi import FastAPI,Header,Depends,HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse,FileResponse
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from database import urls
from pymongo import MongoClient
from qrcode import qr_code


connection_string = "mongodb+srv://vidit321:Vidit87410@cluster0.dqgtxe1.mongodb.net/"
mongo_db = pymongo.MongoClient(connection_string)
databsae = mongo_db.UrlShortner
collection = databsae.urls

qr_obj = qr_code()
base_url = "http://127.0.0.1:8000/"
url_obj = urls(collection)
class addURL(BaseModel):
    special_key : str
    url : str

app = FastAPI()

@app.get("/") #http://127.0.0.1:8000/
def hello():
    return "HELLO FAST API WORLD"

@app.get("/{specialKey}")
async def new(specialKey:str):
    url = url_obj.fetch_url(specialKey)
    return RedirectResponse(url,status_code=302)

@app.post("/addURL")
async def addurl(json:addURL):
    insert = url_obj.insert_url(json.special_key,json.url)
    if insert:
        return {"shortened URL":base_url+json.special_key}
    return {"Shortening of URL":insert}

@app.get("/count/{specialKey}")
async def count_clicks(specialKey:str):
    return url_obj.count(specialKey)

@app.get("/qrcode/{specialKey}")
async def make_qr(specialKey:str):
    qr_obj.make_qr(base_url+specialKey, specialKey)
    return FileResponse(specialKey+".png")